#!/usr/bin/env python3
"""
File Uploads & Binary Streaming - Synchronous Version

Two related capabilities:

* **Chat files** - ``client.files`` uploads binary content as multipart form
  data, then hands back metadata, a signed download URL, and quota usage.
* **Audio memories** - ``client.memories.create_with_audio`` uploads audio,
  and ``stream_audio_chunks`` streams the bytes back without buffering the
  whole file in memory.

The example writes throwaway files to a temp directory so it runs end to end.

Run: python main.py
"""

import shutil
import tempfile
from pathlib import Path

from trix import Trix


def main() -> None:
    """Upload files and audio, then fetch and stream them back."""

    with Trix.from_env() as client:
        print("=" * 60)
        print("FILE UPLOADS & BINARY STREAMING")
        print("=" * 60)

        workdir = Path(tempfile.mkdtemp(prefix="trix_files_"))
        try:
            # ==================================================================
            # UPLOAD A FILE (multipart form data)
            # ==================================================================
            print("\n1. Uploading a file (multipart)...")
            report = workdir / "report.txt"
            report.write_text("Quarterly revenue is up 42% YoY.\n")
            uploaded = client.files.upload(report, filename="report.txt", content_type="text/plain")
            print(f"   Uploaded {uploaded.id}: {uploaded.filename} ({uploaded.size_bytes} bytes)")

            # ==================================================================
            # FETCH METADATA + SIGNED DOWNLOAD URL
            # ==================================================================
            print("\n2. Fetching file metadata...")
            meta = client.files.get(uploaded.id)
            print(f"   {meta.filename} (status={meta.status})")

            print("\n3. Requesting a signed download URL...")
            download = client.files.get_download_url(uploaded.id)
            print(f"   Expires in {download.expires_in}s: {download.url}")

            print("\n4. Checking storage quota...")
            quota = client.files.get_quota()
            print(f"   {quota.file_count} file(s), {quota.usage_percent}% of quota used")

            # ==================================================================
            # AUDIO MEMORY + BINARY STREAMING
            # ==================================================================
            print("\n5. Creating an audio memory (multipart upload)...")
            clip = workdir / "clip.mp3"
            clip.write_bytes(b"ID3\x03\x00\x00\x00" + b"\x00" * 256)
            audio = client.memories.create_with_audio(
                clip, filename="clip.mp3", content_type="audio/mpeg", transcribe=False
            )
            print(f"   Audio memory: {audio.id}")

            print("\n6. Streaming the audio back in chunks (binary)...")
            streamed = 0
            for chunk in client.memories.stream_audio_chunks(audio.id, chunk_size=64):
                streamed += len(chunk)
            print(f"   Streamed {streamed} bytes back")
        finally:
            shutil.rmtree(workdir, ignore_errors=True)

        print("\n" + "=" * 60)
        print("File uploads & streaming complete!")
        print("=" * 60)


if __name__ == "__main__":
    main()
