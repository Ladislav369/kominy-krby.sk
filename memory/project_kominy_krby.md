---
name: kominy-krby.sk web project
description: Deploy state, hosting, repo location, and FTP layout for the kominy-krby.sk website
type: project
---

Website **kominy-krby.sk** — Slovak chimneys/fireplaces site, hosted on **Websupport.sk**.

**Why:** As of 2026-04-27 the production site is in development; only a placeholder/test page is live. The user wants the FTP pipeline ready so the production build can be deployed when finished.

**How to apply:**
- Local repo: `/Users/macbook/Documents/kominy-krby-web/` (git, branch `main`).
- FTP host: `agentftp.kominy-krby.sk`. Username equals the host. Credentials live in the repo's `.env` (gitignored). Do NOT paste them into chat or commit them.
- Document root on server: `/kominy-krby.sk/web/`. Sibling dirs at the FTP root: `.fpm`, `.tmp`, `kominy-krby.sk/{web,sub,logs}`.
- Deployment is plain FTPS via `curl` driven by `./deploy.sh` (reads `.env`).
- The Websupport default `index.php` parking page is preserved at `/kominy-krby.sk/web/index.php` and a backup is at `.backups/index.php.original` in the repo (gitignored). A small `.htaccess` (`DirectoryIndex index.html index.php`) makes our `index.html` win — don't delete `index.php`, the .htaccess handles precedence.
- When swapping in the production build: replace `index.html` (and any new assets), keep `.htaccess`, leave `index.php` alone unless the user asks otherwise.
