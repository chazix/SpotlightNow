import subprocess
import winreg
import requests
import time
import os
import urllib.parse
import json
import hashlib
import argparse
import shutil

# Headers to mimic Windows Spotlight client
headers = {
    "User-Agent": "WindowsShellClient/0",
    "Accept": "application/json"
}

out_dir = "spotlight_images"
cache_file = "image_cache.json"
config_file = "config.json"

class Config:
    def __init__(self, url: str):
        self.url = url

class ImageCacheEntry:
    def __init__(self, hash_value: str):
        self.hash_value = hash_value
        self.usage_count = 0

    def to_dict(self):
        return {
            "hash_value": self.hash_value,
            "usage_count": self.usage_count
        }

def hashed_data(img_data):
    return hashlib.md5(img_data).hexdigest()

def in_image_cache(img_data):
    if not os.path.exists(cache_file):
        return None
    try:
        with open(cache_file, 'r') as f:
            data: dict[str, ImageCacheEntry] = json.load(f)
    except json.JSONDecodeError:
        data: dict[str, ImageCacheEntry] = {}
    hashed = hashed_data(img_data)
    for entry in data.values():
        if entry["hash_value"] == hashed:
            return entry
    return None

def update_image_cache(img_data, filename):
    data: dict[str, ImageCacheEntry] = {}
    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'r') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            data = {}
    hashed = hashed_data(img_data)
    data[filename] = ImageCacheEntry(hashed).to_dict()
    with open(cache_file, "w") as f:
        f.write(json.dumps(data, indent=2))

# Download and save images
def download_image(image_url, filename):
    if image_url:
        img_data = requests.get(image_url).content
        if in_image_cache(img_data):
            print(f"Image already downloaded: {filename}")
            return
        with open(filename, "wb") as f:
            f.write(img_data)
        update_image_cache(img_data, filename)
        print(f"Saved: {filename}")
    else:
        print(f"No URL found for {filename}")

def choose_random_least_used_image():
    if not os.path.exists(cache_file):
        print("No image cache found.")
        return None
    try:
        with open(cache_file, 'r') as f:
            data: dict[str, ImageCacheEntry] = json.load(f)
    except json.JSONDecodeError:
        print("Image cache is corrupted.")
        return None
    if not data:
        print("Image cache is empty.")
        return None
    least_used_count = min(entry["usage_count"] for entry in data.values())
    least_used_images = [filename for filename, entry in data.items() if entry["usage_count"] == least_used_count]
    if not least_used_images:
        print("No images found in cache.")
        return None
    import random
    chosen_image = random.choice(least_used_images)
    data[chosen_image]["usage_count"] += 1
    with open(cache_file, "w") as f:
        f.write(json.dumps(data, indent=2))
    return chosen_image

def check_and_set_personalization(path_to_latest:str) -> bool:
    # first check if HKLM\SOFTWARE\Policies\Microsoft\Windows\Personalization has been set to latest.jpg
    has_personalization_policy = False
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                            r"SOFTWARE\Policies\Microsoft\Windows\Personalization", 0,
                            winreg.KEY_READ)
        current_value, _ = winreg.QueryValueEx(key, "LockScreenImage")
        winreg.CloseKey(key)
        if current_value == path_to_latest:
            has_personalization_policy = True
    except FileNotFoundError:
        pass

    if has_personalization_policy:
        return False

    # Create HKLM\SOFTWARE\Policies\Microsoft\Windows\Personalization if missing and set the path
    try:
        key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,
                               r"SOFTWARE\Policies\Microsoft\Windows\Personalization")
        winreg.SetValueEx(key, "LockScreenImage", 0, winreg.REG_SZ, path_to_latest)
        # Optional: prevent user from changing it
        # winreg.SetValueEx(key, "NoChangingLockScreen", 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(key)
        return True
    except PermissionError:
        print("Run VS Code/terminal as Administrator to set the policy (HKLM).")
        return False

def check_and_set_personalizationcsp(path_to_latest:str) -> bool:
    # first check if HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\PersonalizationCSP has been set to latest.jpg
    has_personalization_policy = False
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                            r"SOFTWARE\Microsoft\Windows\CurrentVersion\PersonalizationCSP", 0,
                            winreg.KEY_READ)
        correct_count = 0
        current_value, _ = winreg.QueryValueEx(key, "LockScreenImagePath")
        if current_value == path_to_latest:
            correct_count += 1
        current_value, _ = winreg.QueryValueEx(key, "LockScreenImageUrl")
        if current_value == path_to_latest:
            correct_count += 1
        current_value, _ = winreg.QueryValueEx(key, "LockScreenImageStatus")
        if current_value == 1:
            correct_count += 1
        winreg.CloseKey(key)
        if correct_count == 3:
            has_personalization_policy = True
    except FileNotFoundError:
        pass

    if has_personalization_policy:
        return False

    # Create HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\PersonalizationCSP if missing and set the path
    try:
        key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,
                               r"SOFTWARE\Microsoft\Windows\CurrentVersion\PersonalizationCSP")
        winreg.SetValueEx(key, "LockScreenImagePath", 0, winreg.REG_SZ, path_to_latest)
        winreg.SetValueEx(key, "LockScreenImageUrl", 0, winreg.REG_SZ, path_to_latest)
        winreg.SetValueEx(key, "LockScreenImageStatus", 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(key)
        return True
    except PermissionError:
        print("Run VS Code/terminal as Administrator to set the policy (HKLM).")
        return False

def set_lock_screen_image(image_path: str) -> bool:
    image_path = os.path.abspath(image_path)
    if not os.path.exists(image_path):
        print(f"Lock screen image not found: {image_path}")
        return False

    # copy image to latest.jpg
    path_to_latest = os.path.abspath(os.path.join(os.getcwd(), "latest.jpg"))
    shutil.copyfile(image_path, path_to_latest)

    # Disable Spotlight for current user so policy takes effect
    try:
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER,
                               r"SOFTWARE\Microsoft\Windows\CurrentVersion\ContentDeliveryManager")
        for name in ("RotatingLockScreenEnabled",
                     "RotatingLockScreenOverlayEnabled",
                     "SubscribedContent-338387Enabled"):
            try:
                winreg.SetValueEx(key, name, 0, winreg.REG_DWORD, 0)
            except OSError:
                pass
        winreg.CloseKey(key)
    except OSError:
        pass

    # first check if HKLM\SOFTWARE\Policies\Microsoft\Windows\Personalization has been set to latest.jpg
    set_personalization_policy = check_and_set_personalization(path_to_latest)
    set_personalizationcsp_policy = check_and_set_personalizationcsp(path_to_latest)

    # Refresh group policy (best-effort)
    if set_personalization_policy or set_personalizationcsp_policy:
        try:
            subprocess.run(["gpupdate", "/target:computer", "/force"], check=False)
        except Exception:
            pass

        print("Lock screen image policy set. You may need to sign out or lock (Win+L) to see it.")
    return True

def parse_args() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Downloads Windows Spotlight images. Updates lockscreen images with random least used images."
    )
    # we want a parser to call download_spotlight_images
    # another for updating lockscreen
    commands = parser.add_subparsers(dest="command", required=True)
    download = commands.add_parser(
        "download",
        help="Download the latest Windows Spotlight images.",
    )
    download.set_defaults(func=lambda args: download_spotlight_images())
    update =commands.add_parser(
        "update-lockscreen",
        help="Update the Windows lockscreen with a random least used image.",
    )
    update.set_defaults(func=lambda args: update_lockscreen_image())
    return parser.parse_args()

def download_spotlight_images(args: argparse.Namespace = None):
    # Retrieve url from config.json
    if not os.path.exists(config_file):
        print(f"Config file not found: {config_file}")
        exit(1)

    config_data: Config = None
    try:
        with open(config_file, 'r') as f:
            data = json.load(f)
            config_data = Config(**data)
            if not config_data.url:
                print("Config file is missing 'url' field.")
                exit(1)
    except json.JSONDecodeError:
        print("Config file is corrupted.")
        exit(1)

    # Fetch JSON data
    response = requests.get(config_data.url, headers=headers)
    response.raise_for_status()
    data: dict = response.json()

    # Navigate to the 'ad' field
    ad_data: dict = data.get("ad", {})
    properties: dict = ad_data.get("properties", {})

    # Extract image URLs
    landscape_url = urllib.parse.unquote(properties.get("landscapeImage", {}).get("image", ""))
    #portrait_url = urllib.parse.unquote(properties.get("portraitImage", {}).get("image", ""))

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    time_now_pst = time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime(time.time() - 8 * 3600))

    download_image(landscape_url, f"{out_dir}/{time_now_pst}_spotlight_landscape.jpg")
    #download_image(portrait_url, f"{out_dir}/{time_now_pst}_spotlight_portrait.jpg")

def update_lockscreen_image(args: argparse.Namespace = None):
    print("Updating lockscreen image...")
    chosen_image = choose_random_least_used_image()
    if not chosen_image:
        print("No image selected for lockscreen update.")
        return
    set_lock_screen_image(chosen_image)

if __name__ == "__main__":
    args = parse_args()
    args.func(args)