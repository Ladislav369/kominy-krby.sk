# kominy-krby.sk

Web for **kominy-krby.sk** — hosted on Websupport.sk.

## Layout

```
.
├── index.html            # current test/placeholder page
├── deploy.sh             # FTP deploy helper (reads .env)
├── .env.example          # template for FTP credentials (copy to .env, do NOT commit)
└── public/               # site source (when production build lands here)
```

## Deploy

1. Copy `.env.example` → `.env` and fill in `FTP_HOST`, `FTP_USER`, `FTP_PASS`, `FTP_REMOTE_DIR`.
2. Run `./deploy.sh` — it uploads everything in the repo root (or `public/`, if it exists) via FTPS using `curl`.
3. Verify at https://kominy-krby.sk.

## Notes

- Hosting: Websupport.sk → webadmin at https://admin.websupport.sk/
- FTP credentials are managed in the Websupport webadmin panel.
- Default Websupport remote dir for the document root is typically `/web/` or `/www/` — confirm in webadmin.
