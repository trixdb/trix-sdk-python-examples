"""Tests for the File Uploads & Binary Streaming example.

Covers the multipart ``files`` API (upload / metadata / signed URL / quota) and
binary audio streaming (``create_with_audio`` + ``stream_audio_chunks``). The
audio bytes are mocked as a raw response body; the SDK yields them in chunks.
"""

import io

import pytest
import respx
from httpx import Response
from trix import AsyncTrix, Trix

CHAT_FILE = {
    "id": "file_1",
    "filename": "report.txt",
    "content_type": "text/plain",
    "size_bytes": 31,
    "status": "ready",
    "created_at": "2026-01-01T00:00:00Z",
}
DOWNLOAD_INFO = {
    "url": "https://cdn.trixdb.com/signed/report.txt?sig=abc",
    "expires_in": 3600,
    "filename": "report.txt",
    "content_type": "text/plain",
    "size_bytes": 31,
}
QUOTA = {
    "total_bytes": 2048,
    "file_count": 3,
    "max_bytes": 1_048_576,
    "max_file_size": 10_485_760,
    "usage_percent": 0,
}
AUDIO_MEMORY = {
    "id": "mem_audio",
    "content": "clip.mp3",
    "type": "audio",
    "tags": [],
    "metadata": {},
    "created_at": "2026-01-01T00:00:00Z",
    "updated_at": "2026-01-01T00:00:00Z",
}
AUDIO_BYTES = b"ID3\x03\x00\x00\x00" + b"BINARYAUDIOPAYLOAD" * 8


def _mock_endpoints() -> None:
    respx.post("https://api.trixdb.com/v1/files/upload").mock(
        return_value=Response(200, json=CHAT_FILE)
    )
    respx.get("https://api.trixdb.com/v1/files/file_1").mock(
        return_value=Response(200, json=CHAT_FILE)
    )
    respx.get("https://api.trixdb.com/v1/files/file_1/url").mock(
        return_value=Response(200, json=DOWNLOAD_INFO)
    )
    respx.get("https://api.trixdb.com/v1/files/quota").mock(return_value=Response(200, json=QUOTA))
    respx.post("https://api.trixdb.com/v1/memories").mock(
        return_value=Response(200, json=AUDIO_MEMORY)
    )
    respx.get("https://api.trixdb.com/v1/memories/mem_audio/audio").mock(
        return_value=Response(200, content=AUDIO_BYTES)
    )


# =============================================================================
# Synchronous Tests
# =============================================================================


@respx.mock
def test_file_upload_and_retrieval_sync():
    """Upload a file, then fetch its metadata, signed URL, and quota."""
    _mock_endpoints()

    with Trix(api_key="test") as client:
        uploaded = client.files.upload(
            io.BytesIO(b"Quarterly revenue is up 42% YoY."),
            filename="report.txt",
            content_type="text/plain",
        )
        assert uploaded.id == "file_1"
        assert uploaded.size_bytes == 31

        meta = client.files.get(uploaded.id)
        assert meta.filename == "report.txt"

        download = client.files.get_download_url(uploaded.id)
        assert download.url.startswith("https://")
        assert download.expires_in == 3600

        quota = client.files.get_quota()
        assert quota.file_count == 3


@respx.mock
def test_audio_upload_and_stream_back_sync():
    """Create an audio memory, then stream the bytes back in chunks."""
    _mock_endpoints()

    with Trix(api_key="test") as client:
        audio = client.memories.create_with_audio(
            io.BytesIO(AUDIO_BYTES),
            filename="clip.mp3",
            content_type="audio/mpeg",
            transcribe=False,
        )
        assert audio.id == "mem_audio"

        chunks = list(client.memories.stream_audio_chunks(audio.id, chunk_size=16))
        assert len(chunks) > 1  # streamed in multiple pieces, not one blob
        assert b"".join(chunks) == AUDIO_BYTES

        # The convenience method returns the whole payload at once.
        assert client.memories.stream_audio(audio.id) == AUDIO_BYTES


# =============================================================================
# Asynchronous Tests
# =============================================================================


@respx.mock
@pytest.mark.asyncio
async def test_file_upload_async():
    """The async client uploads and fetches a signed URL."""
    _mock_endpoints()

    async with AsyncTrix(api_key="test") as client:
        uploaded = await client.files.upload(
            io.BytesIO(b"hello"), filename="report.txt", content_type="text/plain"
        )
        assert uploaded.id == "file_1"

        download = await client.files.get_download_url(uploaded.id)
        assert download.content_type == "text/plain"


@respx.mock
@pytest.mark.asyncio
async def test_audio_stream_back_async():
    """Async binary streaming reassembles the same payload."""
    _mock_endpoints()

    async with AsyncTrix(api_key="test") as client:
        audio = await client.memories.create_with_audio(
            io.BytesIO(AUDIO_BYTES),
            filename="clip.mp3",
            content_type="audio/mpeg",
            transcribe=False,
        )
        chunks = [
            chunk async for chunk in client.memories.stream_audio_chunks(audio.id, chunk_size=16)
        ]

    assert b"".join(chunks) == AUDIO_BYTES
