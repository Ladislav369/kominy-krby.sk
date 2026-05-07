# 🤖 CLAUDE.md — Project Context

> Tento súbor číta Claude Code pri otvorení projektu.
> Každý projekt je súčasťou AresLab Corp systému.

---

## 🌐 GLOBÁLNY SYSTÉM — kde hľadať

```yaml
agenti: "~/Documents/AresLab/aresLab-docs/agents/specialists/"
registry: "~/Documents/AresLab/aresLab-docs/agents/NINJA_AGENT_REGISTRY.md"
brief: "~/Documents/AresLab/aresLab-docs/projects/ecokom/brief.md"
brand: "~/Documents/AresLab/aresLab-docs/projects/ecokom/brand.md"
pravidla: "~/Documents/AresLab/aresLab-docs/PROJECT_ISOLATION_SYSTEM.md"
master_log: "~/Documents/AresLab/aresLab-docs/_system/logs/master_log.md"
```

## 📋 SESSION OPENING

```yaml
load_priority:
  1: "brief.md projektu"
  2: "brand.md projektu"
  3: "NINJA_AGENT_REGISTRY.md"
  4: "master_log posledne 3 ENTRY"
```

## 🤖 AGENTI

```yaml
globalny: "→ aresLab-docs/agents/specialists/{kategoria}/"
projektovy: "→ aresLab-docs/projects/ecokom/agents/"
NIKDY: "Do projekt repo"
```

## 🔒 ISOLATION

```yaml
izolacia: "Nepouzivaj data inych projektov"
```

---

## 📋 WORKFLOW POČAS PRÁCE

```yaml
novy_skill_alebo_agent:
  kde: "~/Documents/AresLab/aresLab-docs/agents/specialists/"
  potom: "git push aresLab-docs"

novy_learning:
  kde: "~/Documents/AresLab/aresLab-docs/_system/logs/master_log.md"
  format: "### ENTRY-XXX | dátum | popis"

novy_tool_alebo_link:
  kde: "~/Documents/AresLab/aresLab-docs/_system/registries/source_links.md"
```

## 🔚 KONIEC SESSION

```yaml
1: "git push projekt repo"
2: "git push aresLab-docs (ak nové agenty/learnings)"
3: "ENTRY do master_log"
4: "Pozri: ~/Documents/AresLab/aresLab-docs/runbooks/DAILY_CHEATSHEET.md"
```

## 📚 SYSTÉMOVÉ RUNBOOKY

```yaml
denne: "aresLab-docs/runbooks/DAILY_CHEATSHEET.md"
workflow: "aresLab-docs/runbooks/MULTI_DEVICE_WORKFLOW.md"
novy_projekt: "aresLab-docs/runbooks/ONBOARD_EXISTING_PROJECT.md"
setup_mac: "aresLab-docs/runbooks/SETUP_ON_NEW_MAC.md"
```

---

## 🔚 KONIEC SESSION — rob AUTOMATICKY

```yaml
ked_dokoncis_ulohu_VZDY:
  
  1_master_log:
    kde: "~/Documents/AresLab/aresLab-docs/_system/logs/master_log.md"
    format: "### ENTRY-XXX | datum | co sa urobilo | co je dalej"
    
  2_ak_novy_agent:
    over: "Je v aresLab-docs/agents/specialists/? Ak nie — presun"
    
  3_ak_heslo_ulozene:
    zapis_do: "projects/ecokom/access.md"
    format: "heslo → Apple Keychain: {nazov-polozky}"
    
  4_git_push:
    projekt: "git push kominy-krby.sk"
    system: "git push aresLab-docs (ak zmeny)"
    
  5_zhrnutie:
    "Daj mi 3 vety: co hotovo | co rozpracovane | co dalej"
```
