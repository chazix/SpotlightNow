# Changelog

All notable changes to this project will be documented in this file.

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

