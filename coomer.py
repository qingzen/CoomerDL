#!/usr/bin/env python3
"""Coomer image scraper. Download semua gambar dari satu creator.

Usage:
  python3 coomer_img.py onlyfans username [--dir OUT] [--limit N] [--skip-existing]

Endpoint: GET /api/v1/{service}/user/{user}/posts?o={offset}&c={count}
Image URL: https://img.coomer.st/thumbnail/data{path}
"""
import argparse, json, os, sys, time, urllib.request

BASE = "https://coomer.st"
DATA = "https://img.coomer.st/thumbnail/data"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")
IMG_EXT = (".jpg", ".jpeg", ".png", ".webp", ".gif")
CHUNK = 50

def api(path):
    req = urllib.request.Request(BASE + path, headers={
        "Accept": "text/css",  # anti-scrape bypass
        "User-Agent": UA,
        "Referer": BASE + "/",
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

def download(url, dst):
    req = urllib.request.Request(url, headers={
        "Accept": "image/*",
        "User-Agent": UA,
        "Referer": BASE + "/",
    })
    # CDN (n*.coomer.st) sometimes blocks origin IPs; short timeout so a
    # dead route fails fast instead of hanging the run.
    with urllib.request.urlopen(req, timeout=25) as r, open(dst, "wb") as f:
        f.write(r.read())

def collect(paths, outdir, skip):
    todo = []
    for p in paths:
        if not p or not p.lower().endswith(IMG_EXT):
            continue  # lo lewatin video + non-gambar
        fname = os.path.basename(p)
        if skip and os.path.exists(os.path.join(outdir, fname)):
            continue
        todo.append(p)
    if not todo:
        return 0
    for i, p in enumerate(todo, 1):
        url = DATA + p
        dst = os.path.join(outdir, os.path.basename(p))
        try:
            download(url, dst)
            print(f"  [{i}/{len(todo)}] {os.path.basename(p)} ({os.path.getsize(dst)//1024} KB)")
        except Exception as e:
            print(f"  [!] fail {os.path.basename(p)}: {e}")
        time.sleep(0.2)
    return len(todo)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("service", help="onlyfans|fansly|fansdb|candifans")
    ap.add_argument("user", help="creator username/id")
    ap.add_argument("--dir", default="images", help="output dir")
    ap.add_argument("--limit", type=int, default=0, help="max images, 0=all")
    ap.add_argument("--skip-existing", action="store_true", help="skip files already downloaded")
    args = ap.parse_args()

    # default dir = username; --dir overrides
    if args.dir == "images":
        args.dir = args.user
    os.makedirs(args.dir, exist_ok=True)
    n_img = total = 0
    offset = 0

    while True:
        data = api(f"/api/v1/{args.service}/user/{args.user}/posts?o={offset}&c={CHUNK}")
        if not data:
            break
        total += len(data)
        for post in data:
            got = collect([post.get("file", {}).get("path"),
                           *[a.get("path") for a in post.get("attachments", [])]],
                          args.dir, args.skip_existing)
            n_img += got
            if args.limit and n_img >= args.limit:
                print(f"limit {args.limit} reached"); sys.exit(0)
            # ponytail: no dup-check; same image across posts redownloads. add --skip-existing handles it.
        print(f"scanned {total} posts, {n_img} images so far (offset {offset})")
        if len(data) < CHUNK:
            break
        offset += CHUNK
        time.sleep(0.5)

    print(f"done: {n_img} images from {total} posts -> {args.dir}")

if __name__ == "__main__":
    main()
