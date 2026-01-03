# ytdown

A minimal, privacy-focused YouTube media downloader that converts videos to multiple formats (MP3, MP4, WebM, etc.) with thumbnail and metadata support.

## Features

- Multiple formats: MP3, MP4, WebM, M4A, FLAC, WAV, OGG

- Thumbnail embedding: Optional thumbnail embedding in audio files

- Metadata support: Include title, artist, and album information

- Customizable quality: 64-320 kbps audio quality control

- Privacy-focused: No OAuth required, no account linking

- Detailed output: Clear progress reporting and summaries

- Simple API: Easy-to-use Python functions and CLI

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/ytdown.git
cd ytdown
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Install FFmpeg (Required)

**Ubuntu/Debian:**

```bash
sudo apt update && sudo apt install ffmpeg
```

**macOS:**

```zsh
brew install ffmpeg
```

**Windows:**

Download from `ffmpeg.org` and add to `PATH`, or use:

```cmd
choco install ffmpeg
```

**Verify FFmpeg installation:**

```bash
ffmpeg -version
```

## Usage

### Command Line Interface

```bash
# Basic MP3 download
python main.py --url "https://youtube.com/watch?v=..."

# Multiple formats
python main.py --url "https://youtube.com/watch?v=..." --formats mp3 mp4

# With thumbnail and metadata
python main.py --url "https://youtube.com/watch?v=..." --include-thumbnail --include-metadata

# High quality audio
python main.py --url "https://youtube.com/watch?v=..." --quality 320

# Custom output directory
python main.py --url "https://youtube.com/watch?v=..." --output-dir "./music"

# All options
python main.py --url "https://youtube.com/watch?v=..." \
               --formats mp3 wav \
               --include-thumbnail \
               --include-metadata \
               --quality 256 \
               --output-dir "./high_quality" \
               --quiet
```

### Python API

```python
from ytdown import download_youtube_media, download_as_mp3

# Download as MP3 with thumbnail and metadata
result = download_as_mp3(
    url="https://youtube.com/watch?v=...",
    include_thumbnail=True,
    include_metadata=True,
    quality="320",
    output_dir="./music"
)

# Download multiple formats
result = download_youtube_media(
    url="https://youtube.com/watch?v=...",
    formats=["mp3", "mp4", "flac"],
    include_thumbnail=True,
    include_metadata=True,
    quality="192",
    output_dir="./downloads"
)
```

### API Reference

`
download_youtube_media(url, formats, include_thumbnail, include_metadata, quality, output_dir, keep_original, quiet)
`

**Main function for downloading YouTube media.**

Parameters:

- `url` (str): YouTube video URL
- `formats` (list): List of formats ['mp3', 'mp4', 'webm', 'm4a', 'flac', 'wav', 'ogg'] (default: -['mp3'])
- `include_thumbnail` (bool): Embed thumbnail in audio files (default: False)
- `include_metadata` (bool): Include metadata in files (default: False)
- `quality` (str): Audio quality for MP3: '64', '128', '192', '256', '320' (default: '192')
- `output_dir` (str): Output directory (default: '`./audio`')
- `keep_original` (bool): Keep original downloaded file (default: False)
- `quiet` (bool): Suppress yt-dlp output (default: False)

**Returns:** Dictionary with download results and file paths.

`
download_as_mp3(url, include_thumbnail, include_metadata, quality, output_dir)
`

Convenience function for MP3 downloads.

`
download_as_mp4(url, output_dir, quiet)
`

Convenience function for MP4 downloads.

`
download_multiple_formats(url, formats, output_dir, **kwargs)
`

Convenience function for multiple format downloads.

## Examples

### Example 1: High-quality MP3 with thumbnail

```bash
python main.py --url "https://youtube.com/watch?v=mCRibm4kOaE" \
               --quality 320 \
               --include-thumbnail \
               --include-metadata \
               --output-dir "./music"
```

### Example 2: Multiple audio formats

```bash
python main.py --url "https://youtube.com/watch?v=mCRibm4kOaE" \
               --formats mp3 flac wav \
               --include-thumbnail \
               --quality 256
```

### Example 3: Video download

```bash
python main.py --url "https://youtube.com/watch?v=mCRibm4kOaE" \
               --formats mp4 \
               --output-dir "./videos"
```

## Project Structure

```bash
ytdown/
├── __init__.py         # Package initialization
├── main.py             # Command-line interface
├── ytdown.py           # Core downloading logic
├── requirements.txt    # Python dependencies
├── README.md           # This file
└── .gitignore          # Git ignore rules
```

## Requirements

### Python Dependencies

See `requirements.txt`.

### System Requirements

- Python 3.8+

- FFmpeg installed and in `PATH`

- Internet connection

- ~100MB free space per video

## Privacy & Legal

- $\checkmark$ No OAuth required - Your Google account is never accessed

- $\checkmark$ No telemetry - Tool doesn't send any data externally

- $\checkmark$ Local processing - All conversions happen on your machine

⚠ **Important**: Only download content that:

- You own the rights to

- Is in the public domain

- You have explicit permission to download

- Is for personal use under fair use principles

Respect copyright laws and YouTube's Terms of Service.

## Troubleshooting

### Common Issues

### 1. "FFmpeg not found"

Verify FFmpeg is installed and in `PATH`:

```bash
ffmpeg -version
```

### 2. "Invalid URL"

- Ensure the URL is a valid YouTube link

- Check if video is age-restricted (may require cookies)

### 3. "Format not available"

- Some formats may not be available for all videos

- Try alternative formats like 'm4a' instead of 'mp3'

### 4. "Network error"

- Check your internet connection

- Try using --quiet flag to reduce output

## Debug Mode

Remove --quiet flag for detailed logs:

```bash
python main.py --url "https://youtube.com/watch?v=..." --formats mp3
```

## Contributing

- Fork the repository

- Create a feature branch (git checkout -b feature/AmazingFeature)

- Commit changes (git commit -m 'Add AmazingFeature')

- Push to branch (git push origin feature/AmazingFeature)

- Open a Pull Request

## License

MIT License - see `LICENSE` file for details.

## Acknowledgments

- [yt-dlp]("https://github.com/yt-dlp/yt-dlp") - The backbone of this tool

- [FFmpeg]("https://ffmpeg.org/") - For audio/video conversion

---

**Note**: This tool is for educational purposes. Download content responsibly and respect copyright holders.

