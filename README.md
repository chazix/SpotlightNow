## spotlight-now.py

A reproducible ritual for keeping your Windows lock screen fresh with the latest Spotlight images.  
Fetches new images daily, archives them, and updates the lock screen using the *Personalization* and *PersonalizationCSP* registry keys.  
Includes deduplication (via hashing) and fair rotation (least‑used image selection tracked in `image_cache.json`).

---

## Requirements
- Windows 10/11 (Pro/Enterprise recommended, but works standalone)
- Python 3.8+
- Administrator rights (to write registry keys under `HKLM`)
- Directory: `C:\ProgramData\SpotlightNow`  
- All images and cache files are stored here
- Ensure this folder is readable by SYSTEM and Users

---

## Python

1. Clone this repository:
```
git clone https://github.com/ChazixLLC/spotlight-now.git
cd spotlight-now
```

2. Install dependencies:
```
pip install -r requirements.txt
```

3. Run commands:
```
python spotlight-now.py download
python spotlight-now.py update-lockscreen
```

4. Saves images to: `spotlight_images/*.jpg`

5. Saves cache to: `image_cache.json`

## Installation
1. Download latest release

2. Extract & Run: `install.bat`

## Usage

```
usage: spotlight-now.py [-h] {download,update-lockscreen} ...

Downloads Windows Spotlight images. Updates lockscreen images with random least used images.

positional arguments:
  {download,update-lockscreen}
    download            Download the latest Windows Spotlight images.
    update-lockscreen   Update the Windows lockscreen with a random least used image.

optional arguments:
  -h, --help            show this help message and exit
```

## How It Works

- *Download*: Fetches the latest Spotlight feed (configurable via `config.json`), saves images to `C:\ProgramData\SpotlightNow`, and hashes them to avoid duplicates.
- *Cache*: Tracks usage in `image_cache.json` so random selection favors the least‑used images.
- *Registry*:
 - Writes all three `PersonalizationCSP` values:
   - `LockScreenImagePath`
   - `LockScreenImageUrl`
   - `LockScreenImageStatus`
 - Writes Policy `Personalization` values:
   - `LockScreenImage`

## Backstory

This project was born out of a detour through Windows' opaque personalization stack.
What should have been a simple "new image every day" turned into a deep dive into registry keys, CSP values, and refresh rituals.
The result: a simple, reproducible tool that makes Spotlight behave — now



