# Changelog

All notable changes to this project will be documented in this file.

## [1.1] - 2025-10-27

### Added
- Policy setting: `HKLM\SOFTWARE\Policies\Microsoft\Windows\CloudContent\DisableWindowsSpotlightOnLockScreen` to disable Spotlight on lock screen.
- `update-task.ps1`: configured to run at user level to set `HKCU` keys.
- `uninstall.bat`: batch script to run uninstall function with admin elevation and remove scheduled task.
- `run-tasks.ps1`: orchestration script invoked during installation to execute `SpotlightNow-Download` and `SpotlightNow-UpdateLockscreen` in order on first run.

### Changed
- Uninstall function now removes registry policies set by the script:
  - `HKLM\SOFTWARE\Policies\Microsoft\Windows\CloudContent\DisableWindowsSpotlightOnLockScreen`
  - `HKLM\SOFTWARE\Policies\Microsoft\Windows\Personalization\LockScreenImage`
  - `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\PersonalizationCSP\LockScreenImagePath`, `LockScreenImageStatus`, `LockScreenImageUrl`
- Uninstall function resets `HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\ContentDeliveryManager` values back to `1`:
  - `RotatingLockScreenEnabled`, `RotatingLockScreenOverlayEnabled`, `SubscribedContent-338387Enabled`
- Uninstall function refreshes group policy after removal.
- Uninstall function now also clears application data directory:
  - `C:\ProgramData\SpotlightNow`
- Build process updated: rebuilt with PyInstaller `--noconsole` so scheduled tasks run silently in the user session.
  - This was required because the update task now runs under the current user (to correctly target HKCU), and a console build would otherwise show a visible window.
- `update-task.ps1`: switch to `-AtLogon` trigger to align with per-user context (startup trigger requires SYSTEM)
- `update-task.ps1`: added `$Trigger2` to run every 8 hours indefinitely, ensuring lock screen updates on always‑on systems.
- `download-task.ps1`: attempt to grab spotlight images every 1 hour indefinitely.

### Documentation
- Refined README Quick Start and Python sections to include uninstall instructions and clarify admin requirements.

## [1.0] - 2025-10-26

### Added

- Initial release of `spotlight-now.py`
- Fetch latest Windows Spotlight images from configurable feed URLs
- Override lock screen via Personalization & CSP registry keys
- Hash images to prevent duplicate saves
- Track usage in `image_cache.json`
- Random selection favors least-used images for variety
- Basic error handling and validation
- PowerShell scripts for daily scheduled task + archival
- Installer (`install.bat`) with admin elevation, ProgramData setup, and scheduled task registration

[1.0]: https://github.com/chazix/SpotlightNow/releases/tag/v1.0
[1.1]: https://github.com/chazix/SpotlightNow/releases/tag/v1.1
