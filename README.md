\# spotlight-now.py 🌅



A reproducible ritual for keeping your Windows lock screen fresh with the latest Spotlight images.  

Fetches new images daily, archives them, and updates the lock screen using the \*\*Personalization\*\* and \*\*PersonalizationCSP\*\* registry keys.  

Includes deduplication (via hashing) and fair rotation (least‑used image selection tracked in `image\_cache.json`).



---



\## 📦 Requirements



\- Windows 10/11 (Pro/Enterprise recommended, but works standalone)

\- Python 3.8+

\- Administrator rights (to write registry keys under `HKLM`)

\- Directory: \*\*`C:\\ProgramData\\SpotlightNow`\*\*  

&nbsp; - All images and cache files are stored here

&nbsp; - Ensure this folder is readable by SYSTEM and Users



---



\## ⚙️ Installation



1\. Clone this repository:

&nbsp;  ```git clone https://github.com/ChazixLLC/spotlight-now.git

&nbsp;  cd spotlight-now```



2\. Create the working directory:

&nbsp;  ```mkdir C:\\ProgramData\\SpotlightNow```



3\. Install dependencies:

&nbsp;  ```pip install -r requirements.txt```



\## 🚀 Usage



```

usage: spotlight-now.py \[-h] {download,update-lockscreen} ...



Downloads Windows Spotlight images. Updates lockscreen images with random least used images.



positional arguments:

&nbsp; {download,update-lockscreen}

&nbsp;   download            Download the latest Windows Spotlight images.

&nbsp;   update-lockscreen   Update the Windows lockscreen with a random least used image.



optional arguments:

&nbsp; -h, --help            show this help message and exit

```



\## 🔑 How It Works



\- \*Download\*: Fetches the latest Spotlight feed (configurable via `config.json`), saves images to `C:\\ProgramData\\SpotlightNow`, and hashes them to avoid duplicates.

\- \*Cache\*: Tracks usage in `image\_cache.json` so random selection favors the least‑used images.

\- \*Registry\*:

&nbsp; - Writes all three `PersonalizationCSP` values:

&nbsp;   - `LockScreenImagePath`

&nbsp;   - `LockScreenImageUrl`

&nbsp;   - `LockScreenImageStatus`

&nbsp; - Writes Policy `Personalization` values:

&nbsp;   - `LockScreenImage`



\## 📖 Backstory



This project was born out of a detour through Windows' opaque personalization stack.

What should have been a simple "new image every day" turned into a deep dive into registry keys, CSP values, and refresh rituals.

The result: a simple, reproducible tool that makes Spotlight behave — now



