## spotlight-now.py

[![Release](https://img.shields.io/github/v/release/chazix/SpotlightNow)](https://github.com/chazix/SpotlightNow/releases)
[![License](https://img.shields.io/github/license/chazix/SpotlightNow)](./LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/chazix/SpotlightNow)](https://github.com/chazix/SpotlightNow/commits/main)
[![Issues](https://img.shields.io/github/issues/chazix/SpotlightNow)](https://github.com/chazix/SpotlightNow/issues)

A reproducible ritual for keeping your Windows lock screen fresh with the latest Spotlight images.  
Fetches new images daily, archives them, and updates the lock screen using the *Personalization* and *PersonalizationCSP* registry keys.  
Includes deduplication (via hashing) and fair rotation (least‑used image selection tracked in `image_cache.json`).

---

## Quick Start (no Python required)

1. Download the latest release zip from [Releases](https://github.com/chazix/SpotlightNow/releases/latest)
2. Extract and run `install.bat` (requires admin elevation)
3. Enjoy daily Spotlight lock screen refreshes 🎉

### Uninstall
If you’d like to remove SpotlightNow completely:
- Run `uninstall.bat` (requires admin elevation)
- This will remove the scheduled tasks and revert registry settings back to defaults

---

## Requirements
- Windows 10/11 (Pro/Enterprise recommended, but works standalone)
- Python 3.8+
- Administrator rights (to write registry keys under `HKLM`)
- Directory: `C:\ProgramData\SpotlightNow`
- All images and cache files are stored here
- Ensure this folder is readable by SYSTEM and Users

---

## Python (developer mode)

If you prefer to run SpotlightNow directly from source instead of using the packaged release:

1. Clone this repository:
```
git clone https://github.com/chazix/spotlight-now.git
cd spotlight-now
```

2. Install dependencies (Python 3.9+ recommended):
```
pip install -r requirements.txt
```

3. Run SpotlightNow commands:
```
# Download the latest Spotlight images (no elevation required)
python spotlight-now.py download

# Update the lock screen image (on first run requires admin for writing HKLM policies)
python spotlight-now.py update-lockscreen

# Remove registry policies and scheduled tasks (requires admin)
python spotlight-now.py uninstall
```

4. Output locations:
- Images are saved to: `spotlight_images/*.jpg`
- Metadata/cache is saved to: `image_cache.json`

---

## Build from Source (PyInstaller)

If you prefer not to use the prebuilt executable, you can generate your own
binary directly from the source.

1. Install [PyInstaller](https://pyinstaller.org/) into your Python environment (included in `requirements.txt`):
```
pip install pyinstaller
```

2. From the project root, run:
```
pyinstaller --clean --noconsole --onefile spotlight-now.py
```

3. The resulting executable will be placed in the `dist/` directory.

---

## False Positives (Antivirus / VirusTotal)

SpotlightNow executables built with [PyInstaller](https://pyinstaller.org/) may
be flagged by some antivirus engines or show a poor score on VirusTotal.
This is a **known false positive** pattern that affects many PyInstaller
applications.

**Why this happens:**
- PyInstaller bundles Python code into a self‑extracting EXE. The unpacking
  behavior resembles how some malware hides payloads.
- SpotlightNow modifies a small set of Windows registry keys and scheduled
  tasks to control the lock screen. Heuristic scanners often flag any unsigned
  binary that touches `HKLM` or `HKCU` keys.
- Most detections are labeled as *“Generic Trojan”* or *“Heur.ML”*, which are
  machine‑learning guesses, not signatures of real malware.

**How to verify safety:**
- Review the [source code](./spotlight-now.py) — everything is published and auditable.
- Build your own binary using the documented PyInstaller command:
```
pyinstaller --clean --noconsole --onefile spotlight-now.py
```
- Check the SHA256 checksum of the release binary against the one published in the release notes.
- Optionally upload your build to: [VirusTotal](https://www.virustotal.com/) to confirm results.

SpotlightNow is transparent, reversible, and documented. The flagged behavior is expected given the registry and task modifications, but the code is clean and open for inspection.

---

## Usage

```
usage: spotlight-now.py [-h] {download,update-lockscreen,uninstall} ...

Downloads Windows Spotlight images. Updates lockscreen images with random least used images.

positional arguments:
  {download,update-lockscreen,uninstall}
    download            Download the latest Windows Spotlight images.
    update-lockscreen   Update the Windows lockscreen with a random least used image.
    uninstall           Uninstall the lockscreen image policy set by this script.

optional arguments:
  -h, --help            show this help message and exit
```

## How It Works

- *Download*: Fetches the latest Spotlight feed (configurable via `config.json`), saves images to `C:\ProgramData\SpotlightNow`, and hashes them to avoid duplicates.
  - Scheduled task runs **once every hour** to attempt fetching a new image.
- *Cache*: Tracks usage in `image_cache.json` so random selection favors the least‑used images.
- *Registry*:
  - Writes all three **PersonalizationCSP** values under:
    - `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\PersonalizationCSP\LockScreenImagePath`
    - `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\PersonalizationCSP\LockScreenImageUrl`
    - `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\PersonalizationCSP\LockScreenImageStatus`
  - Writes **Policy\Personalization** value:
    - `HKLM\SOFTWARE\Policies\Microsoft\Windows\Personalization\LockScreenImage`
  - Writes **Policy\CloudContent** value:
    - `HKLM\SOFTWARE\Policies\Microsoft\Windows\CloudContent\DisableWindowsSpotlightOnLockScreen`
  - On uninstall, removes those same five machine‑level values:
    - `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\PersonalizationCSP\LockScreenImagePath`
    - `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\PersonalizationCSP\LockScreenImageUrl`
    - `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\PersonalizationCSP\LockScreenImageStatus`
    - `HKLM\SOFTWARE\Policies\Microsoft\Windows\Personalization\LockScreenImage`
    - `HKLM\SOFTWARE\Policies\Microsoft\Windows\CloudContent\DisableWindowsSpotlightOnLockScreen`
  - On uninstall, resets **ContentDeliveryManager** values to `1` under:
    - `HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\ContentDeliveryManager\RotatingLockScreenEnabled`
    - `HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\ContentDeliveryManager\RotatingLockScreenOverlayEnabled`
    - `HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\ContentDeliveryManager\SubscribedContent-338387Enabled`
- *Update*: Applies a new lock screen image from the cache.
  - Scheduled task runs **at startup** to refresh the lock screen from a randomly selected least used image.
- *Filesystem*:
  - On uninstall, deletes the application data directory:
    - `C:\ProgramData\SpotlightNow`

## Backstory

This project was born out of a detour through Windows' opaque personalization stack.
What should have been a simple "new image every day" turned into a deep dive into registry keys, CSP values, and refresh rituals.
The result: a simple, reproducible tool that makes Spotlight behave — now