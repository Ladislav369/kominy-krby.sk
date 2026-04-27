# CLAUDE.md — kominy-krby.sk

## Memory

This repo has its own memory at `memory/`. **When working in this repo, use it instead of the global auto-memory store** for anything project-scoped.

- Read `memory/MEMORY.md` at the start of any work in this repo (it's the index).
- Write new project/reference entries as `memory/<topic>.md` with the standard frontmatter (`name`, `description`, `type`) and add a one-line pointer to `memory/MEMORY.md`.
- Cross-project user preferences and feedback still go to the global memory store.
- Do not commit secrets to memory entries — point at where they live (e.g. `.env`) instead.

## Deployment

- `./deploy.sh` uploads via FTPS using `.env` credentials. See `README.md` for the full layout.
- Document root on Websupport: `/kominy-krby.sk/web/`. The Websupport parking `index.php` is preserved on the server; a `.htaccess` (`DirectoryIndex index.html index.php`) makes our page win.

## Conventions

- Never commit `.env` (FTP creds) or `.backups/` (server-side originals). `.gitignore` enforces this.
- Use absolute domain refs (`kominy-krby.sk`) in copy and links — the site is also reachable as `www.kominy-krby.sk` but the canonical form is the bare domain.
