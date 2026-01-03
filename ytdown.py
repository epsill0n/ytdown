import yt_dlp
import os
from typing import List, Optional

def download_youtube_media(
    url: str,
    formats: List[str] = None,
    include_thumbnail: bool = False,
    include_metadata: bool = False,
    output_dir: str = "downloads",
    quality: str = "192",
    keep_original: bool = False,
    quiet: bool = False
) -> dict:
    """
    Download YouTube media in specified formats with customizable options.
    
    Args:
        url: YouTube URL (video or playlist)
        formats: List of desired formats ['mp3', 'mp4', 'webm', 'm4a', etc.]
        include_thumbnail: Whether to embed thumbnail in audio files
        include_metadata: Whether to include metadata (title, artist, etc.)
        output_dir: Directory to save downloads
        quality: Audio quality for MP3 (64, 128, 192, 256, 320)
        keep_original: Keep original downloaded file before conversion
        quiet: Suppress yt-dlp output
        
    Returns:
        Dictionary with download information
        
    Example:
        # Download as MP3 with thumbnail and metadata
        download_youtube_media(
            url="https://youtube.com/watch?v=...",
            formats=["mp3"],
            include_thumbnail=True,
            include_metadata=True
        )
        
        # Download as both MP3 and MP4
        download_youtube_media(
            url="https://youtube.com/watch?v=...",
            formats=["mp3", "mp4"]
        )
        
        # Download only MP4 (video)
        download_youtube_media(
            url="https://youtube.com/watch?v=...",
            formats=["mp4"]
        )
    """
    
    if formats is None:
        formats = ["mp3"]
    
    os.makedirs(output_dir, exist_ok=True)
    
    format_configs = {
        'mp3': {
            'format': 'bestaudio/best',
            'postprocessors': [],
            'ext': 'mp3'
        },
        'mp4': {
            'format': 'best[ext=mp4]/best',
            'postprocessors': [],
            'ext': 'mp4'
        },
        'webm': {
            'format': 'best[ext=webm]/best',
            'postprocessors': [],
            'ext': 'webm'
        },
        'm4a': {
            'format': 'bestaudio[ext=m4a]/bestaudio',
            'postprocessors': [],
            'ext': 'm4a'
        },
        'flac': {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'flac',
            }],
            'ext': 'flac'
        },
        'wav': {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
            }],
            'ext': 'wav'
        },
        'ogg': {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'vorbis',
            }],
            'ext': 'ogg'
        }
    }
    
    results = {
        'url': url,
        'formats_requested': formats,
        'downloads': [],
        'errors': []
    }
    
    for fmt in formats:
        if fmt not in format_configs:
            results['errors'].append(f"Unsupported format: {fmt}")
            continue
        
        config = format_configs[fmt]
        ydl_opts = {
            'format': config['format'],
            'outtmpl': os.path.join(output_dir, f'%(title)s_{fmt}.%(ext)s'),
            'quiet': quiet,
            'no_warnings': quiet,
            'no_color': True,
            'ignoreerrors': False,
        }
        
        postprocessors = config['postprocessors'].copy()
        
        if fmt in ['mp3', 'flac', 'wav', 'ogg']:
            if fmt == 'mp3':
                postprocessors.append({
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': fmt,
                    'preferredquality': quality,
                })
            
            if include_thumbnail and fmt in ['mp3', 'flac', 'm4a']:
                ydl_opts['writethumbnail'] = True
                postprocessors.append({
                    'key': 'EmbedThumbnail',
                })
            
            if include_metadata:
                postprocessors.append({
                    'key': 'FFmpegMetadata',
                })
        
        if keep_original:
            ydl_opts['keepvideo'] = True
        
        if postprocessors:
            ydl_opts['postprocessors'] = postprocessors
        
        try:
            print(f"\n{'='*60}")
            print(f"Downloading as {fmt.upper()}...")
            print(f"{'='*60}")
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                print(f"Title: {info.get('title', 'Unknown')}")
                print(f"Channel: {info.get('uploader', 'Unknown')}")
                print(f"Duration: {info.get('duration', 0)} seconds")
                
                ydl.download([url])
                
                base_filename = ydl.prepare_filename(info)
                final_filename = base_filename.rsplit('.', 1)[0] + f'.{fmt}'
                
                if os.path.exists(final_filename):
                    file_size = os.path.getsize(final_filename) / (1024 * 1024)
                    print(f"\nSuccessfully downloaded: {os.path.basename(final_filename)}")
                    print(f"\tLocation: {final_filename}")
                    print(f"\tSize: {file_size:.2f} MB")
                    print(f"\tFormat: {fmt.upper()}")
                    
                    results['downloads'].append({
                        'format': fmt,
                        'filename': final_filename,
                        'size_mb': round(file_size, 2),
                        'with_thumbnail': include_thumbnail if fmt in ['mp3', 'flac', 'm4a'] else False,
                        'with_metadata': include_metadata,
                        'success': True
                    })
                else:
                    error_msg = f"File not found after download: {final_filename}"
                    print(f"{error_msg}")
                    results['errors'].append(error_msg)
                    
        except Exception as e:
            error_msg = f"Error downloading {fmt}: {str(e)}"
            print(f"\t{error_msg}")
            results['errors'].append(error_msg)
    
    print(f"\n{'='*60}")
    print("DOWNLOAD SUMMARY")
    print(f"{'='*60}")
    print(f"URL: {url}")
    print(f"Requested formats: {', '.join(formats)}")
    print(f"Successful downloads: {len(results['downloads'])}/{len(formats)}")
    
    for download in results['downloads']:
        print(f"\t{download['format'].upper()}: {os.path.basename(download['filename'])}")
    
    if results['errors']:
        print(f"\nErrors ({len(results['errors'])}):")
        for error in results['errors']:
            print(f"\t{error}")
    
    return results

def download_as_mp3(
    url: str,
    include_thumbnail: bool = True,
    include_metadata: bool = True,
    quality: str = "192",
    output_dir: str = "downloads"
) -> dict:
    """Convenience function to download as MP3 with common defaults"""
    return download_youtube_media(
        url=url,
        formats=["mp3"],
        include_thumbnail=include_thumbnail,
        include_metadata=include_metadata,
        output_dir=output_dir,
        quality=quality
    )

def download_as_mp4(
    url: str,
    output_dir: str = "downloads",
    quiet: bool = True
) -> dict:
    """Convenience function to download as MP4"""
    return download_youtube_media(
        url=url,
        formats=["mp4"],
        include_thumbnail=False,
        include_metadata=False,
        output_dir=output_dir,
        quiet=quiet
    )

def download_multiple_formats(
    url: str,
    formats: List[str],
    output_dir: str = "downloads",
    **kwargs
) -> dict:
    """Download in multiple formats simultaneously"""
    return download_youtube_media(
        url=url,
        formats=formats,
        output_dir=output_dir,
        **kwargs
    )