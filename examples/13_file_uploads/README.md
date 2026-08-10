# File Uploads & Binary Streaming

## Goal

Upload binary content as multipart form data, then fetch it back - either as a
signed URL or streamed a chunk at a time so large files never sit fully in
memory.

## Prerequisites

- Completed [01_memories_basics](../01_memories_basics/)

## Concepts Covered

### 1. Multipart file upload

`client.files.upload` accepts a path, a `Path`, or any binary file object and
sends it as `multipart/form-data`:

```python
uploaded = client.files.upload("report.txt", filename="report.txt", content_type="text/plain")
# or a file object:
uploaded = client.files.upload(open("photo.jpg", "rb"), filename="photo.jpg")
```

There is also `client.files.upload_base64(...)` for JSON-body uploads.

### 2. Retrieval: metadata, signed URL, quota

```python
meta = client.files.get(uploaded.id)                 # ChatFile metadata
download = client.files.get_download_url(uploaded.id)  # signed URL, 1hr TTL
print(download.url, download.expires_in)
quota = client.files.get_quota()                     # storage usage
```

### 3. Binary streaming for audio memories

Audio is uploaded with `create_with_audio` (also multipart) and streamed back
without buffering the whole file:

```python
audio = client.memories.create_with_audio("clip.mp3", content_type="audio/mpeg")

# Stream in chunks (memory-efficient) ...
for chunk in client.memories.stream_audio_chunks(audio.id, chunk_size=8192):
    sink.write(chunk)

# ... or grab the whole payload at once:
data = client.memories.stream_audio(audio.id)
```

The async client streams with `async for`:

```python
async for chunk in client.memories.stream_audio_chunks(audio.id):
    await sink.write(chunk)
```

> Pass `transcribe=True` (the default) to `create_with_audio` to kick off
> transcription, then read it back with `client.memories.get_transcript(id)`.

## Walkthrough

### Sync Version (`main.py`)

1. Uploads a text file and prints its size
2. Fetches metadata, a signed download URL, and the storage quota
3. Uploads an audio clip and streams the bytes back in chunks

### Async Version (`async_example.py`)

Same flow; fetches the download URL and quota concurrently with
`asyncio.gather` and streams the audio with `async for`.

## Running the Examples

```bash
python main.py           # Synchronous
python async_example.py  # Asynchronous
```

## Next Steps

- [14_agent_orchestration](../14_agent_orchestration/) - Bots, crews, and workflows
