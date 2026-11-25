# 2006Scape Plugins & Scripts Repository

Official online repository for 2006Scape Mobile & Desktop `.script` / `.bsh` / `.java` plugins and automation scripts.

## Repository URL
- Manifest: `https://raw.githubusercontent.com/dark98/2006scape-plugins/main/index.json`

## Adding a Plugin or Script
1. Place your `.script`, `.bsh`, or `.java` file in `scripts/` (or `plugins/`).
2. Include metadata headers (`@name`, `@version`, `@minApi`, `@author`, `@desc`, `@type`).
3. Add an entry to `index.json` with a matching `version`, `minApi`, `fileName`, and `downloadUrl`.
4. Commit and push to `main` — clients will detect new entries and `UPDATE_AVAILABLE` versions automatically via SemVer.
