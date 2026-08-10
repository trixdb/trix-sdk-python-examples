#!/usr/bin/env python3
"""
File Uploads & Binary Streaming - Asynchronous Version

The async client uploads with ``await`` and streams binary content with
``async for`` over ``stream_audio_chunks`` - the bytes arrive a chunk at a
time, never fully buffered.

Run: python async_example.py
"""

import asyncio
import shutil
import tempfile
from pathlib import Path

from trix import AsyncTrix


async def main() -> None:
    """Upload a file and an audio clip, then stream the audio back."""

    async with AsyncTrix.from_env() as client:
        print("=" * 60)
        print("ASYNC FILE UPLOADS & BINARY STREAMING")
        print("=" * 60)

        workdir = Path(tempfile.mkdtemp(prefix="trix_files_"))
        try:
            # ==================================================================
            # UPLOAD + SIGNED URL (concurrent metadata + quota fetch)
            # ==================================================================
            print("\n1. Uploading a file...")
            report = workdir / "notes.md"
            report.write_text("# Meeting notes\n\n- Ship the SDK examples.\n")
            uploaded = await client.files.upload(
                report, filename="notes.md", content_type="text/markdown"
            )
            print(f"   Uploaded {uploaded.id}: {uploaded.filename}")

            print("\n2. Fetching download URL and quota concurrently...")
            download, quota = await asyncio.gather(
                client.files.get_download_url(uploaded.id),
                client.files.get_quota(),
            )
            print(f"   URL expires in {download.expires_in}s; {quota.file_count} file(s) stored")

            # ==================================================================
            # AUDIO MEMORY + ASYNC BINARY STREAMING
            # ==================================================================
            print("\n3. Creating an audio memory...")
            clip = workdir / "clip.mp3"
            clip.write_bytes(b"ID3\x03\x00\x00\x00" + b"\x00" * 256)
            audio = await client.memories.create_with_audio(
                clip, filename="clip.mp3", content_type="audio/mpeg", transcribe=False
            )
            print(f"   Audio memory: {audio.id}")

            print("\n4. Streaming the audio back with `async for`...")
            streamed = 0
            async for chunk in client.memories.stream_audio_chunks(audio.id, chunk_size=64):
                streamed += len(chunk)
            print(f"   Streamed {streamed} bytes back")
        finally:
            shutil.rmtree(workdir, ignore_errors=True)

        print("\n" + "=" * 60)
        print("Async file uploads & streaming complete!")
        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
