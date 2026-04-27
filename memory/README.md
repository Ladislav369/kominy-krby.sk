# memory/

Project-versioned memory for kominy-krby.sk. Same format as the global Claude Code auto-memory system, but lives in the repo so it's reviewed in PRs and travels with the code.

- `MEMORY.md` — index of memory entries (one line per entry, max ~150 chars).
- `*.md` (with frontmatter `name`, `description`, `type` ∈ `user|feedback|project|reference`) — the actual memory entries.

When working in this repo, read `memory/MEMORY.md` first and prefer writing project-scoped memory here instead of the global `~/.claude/projects/.../memory/` location. Cross-project user/feedback memory still belongs in the global store.
