import argparse
import sys
import os
from ytdown import download_youtube_media

def main():
    parser = argparse.ArgumentParser(
        description='Download YouTube videos in specified formats',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        '--url',
        type=str,
        required=True,
        help='YouTube video URL'
    )
    
    parser.add_argument(
        '--formats',
        nargs='+',
        default=['mp3'],
        choices=['mp3', 'mp4', 'webm', 'm4a', 'flac', 'wav', 'ogg'],
        help='Output formats'
    )
    
    parser.add_argument(
        '--include-thumbnail',
        action='store_true',
        default=False,
        help='Embed thumbnail in audio files'
    )
    
    parser.add_argument(
        '--include-metadata',
        action='store_true',
        default=False,
        help='Include metadata in files'
    )
    
    parser.add_argument(
        '--quality',
        type=str,
        default='192',
        choices=['64', '128', '192', '256', '320'],
        help='Audio quality for MP3'
    )
    
    parser.add_argument(
        '--output-dir',
        type=str,
        default='./audio',
        help='Output directory'
    )
    
    parser.add_argument(
        '--keep-original',
        action='store_true',
        default=False,
        help='Keep original downloaded file before conversion'
    )
    
    parser.add_argument(
        '--quiet',
        action='store_true',
        default=False,
        help='Suppress yt-dlp output'
    )
    
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    print("YouTube Media Downloader")
    print("=" * 50)
    print(f"URL: {args.url}")
    print(f"Formats: {', '.join(args.formats)}")
    print(f"Output directory: {args.output_dir}")
    print(f"Quality: {args.quality} kbps")
    print(f"Thumbnail: {'Yes' if args.include_thumbnail else 'No'}")
    print(f"Metadata: {'Yes' if args.include_metadata else 'No'}")
    print(f"Keep original: {'Yes' if args.keep_original else 'No'}")
    print("=" * 50)

    result = download_youtube_media(
        url=args.url,
        formats=args.formats,
        include_thumbnail=args.include_thumbnail,
        include_metadata=args.include_metadata,
        quality=args.quality,
        output_dir=args.output_dir,
        keep_original=args.keep_original,
        quiet=args.quiet
    )

    print("\nDownload Results:")
    print("-" * 30)
    
    if result.get('downloads'):
        print(f"Successfully downloaded {len(result['downloads'])} format(s):")
        for dl in result['downloads']:
            print(f"  • {dl['format'].upper()}: {os.path.basename(dl['filename'])}")
    
    if result.get('errors'):
        print(f"\nErrors ({len(result['errors'])}):")
        for error in result['errors']:
            print(f"  • {error}")
        sys.exit(1)
    
    if not result.get('downloads') and not result.get('errors'):
        print("No files were downloaded.")
        sys.exit(1)
    
    print("\nDownload complete!")
    return result

if __name__=='__main__':
    main()