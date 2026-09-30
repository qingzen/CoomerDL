# Coomer Image Scraper

## Requirements
Python 3, no extra dependencies. Just `python` or `python3`.

## Usage

Double-click `coomer_download.bat` for an interactive menu (recommended).

Or run from terminal:
```
python coomer_img.py onlyfans tabycatxoxo                  # all images from creator
python coomer_img.py fansly <username> --dir ./myfolder    # custom output folder
python coomer_img.py onlyfans <username> --limit 200       # stop after 200 images
python coomer_img.py onlyfans <username> --skip-existing   # resume, skip already downloaded
```

Arguments:
  service           onlyfans | fansly | fansdb | candifans
  user              creator username or ID

Options:
  --dir OUT         output folder (default: username)
  --limit N         max images to download, 0 = all
  --skip-existing   skip files that already exist (use to resume)

## How it works
- Fetches all creator posts via GET /api/v1/{service}/user/{user}/posts (paginated)
- Bypasses DDoS-Guard anti-scrape using the Accept: text/css header trick
- Collects image paths from post.file and post.attachments
- Downloads only image extensions: .jpg .jpeg .png .webp .gif (videos are skipped)

## Image quality note
> Downloads are THUMBNAILS only (via img.coomer.st/thumbnail/data).
> Full-size images are blocked on this network/IP range.
> For full quality, use a different connection or VPN.

## Notes
- If downloads hang or fail, the CDN may be blocking your IP/subnet. Switch network or use a VPN.
- The same image appearing in multiple posts will be re-downloaded unless --skip-existing is used.
