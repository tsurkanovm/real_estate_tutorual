# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Environment

- **Local dev**: `/home/asus/projects/local/odoof`
- **Remote VPS**: `/opt/projects/estate` — production server, accessible via SSH
- All `docker compose` commands must be run from the project root directory

## Project Overview

An Odoo 18 real estate brokerage system running in Docker. Contains two addons:
- `ud_estate` — core module (property listings, offers, types, tags, dashboard, user extension)
- `ud_estate_account` — extends `ud_estate` with invoice creation on property sale

## Common Commands

All Odoo commands run inside Docker. The database name is `odoof` (main). On the VPS there is no demo database.

```bash
# Start / stop
docker compose up -d
docker compose down

# View logs
docker compose logs -f web

# After Python changes (models, controllers)
docker compose restart web

# Update module + restart (new fields, new views)
docker compose run --rm --entrypoint /usr/bin/odoo web --config /etc/odoo/odoo.conf -d odoof -u ud_estate --without-demo=all --stop-after-init && docker compose restart web

# Shell inside container
docker compose exec web bash

# Inside container: quick module update
odoo -d odoof -u ud_estate --stop-after-init

# Install/reset demo database (local dev only)
docker compose run --rm --entrypoint /usr/bin/odoo web --config /etc/odoo/odoo.conf -d odoof_demo -i ud_estate --with-demo --stop-after-init && docker compose restart web

# Install Ukrainian language
# Add --load-language=uk_UA to any update/install command
```

XML/view-only changes are auto-reloaded via `--dev xml` — just refresh the browser.

## Files NOT in git (must be created manually on each environment)

These files are excluded from git and must be created on the server before `docker compose up`:

- `config/odoo.conf` — Odoo config (addons path, DB connection)
- `secrets/db_password` — plain-text DB password file (used by Docker secrets)
- `.env` — Docker image names and DB connection vars (`ODOO_IMAGE`, `DB_IMAGE`, `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_NAME`)

The `proxy` external Docker network must also exist: `docker network create proxy`

## Architecture

### Module: `ud_estate`

**Models:**
- `ud_estate.property` — central model; state machine: `new → received → accepted → sold → cancelled`; computed fields: `name` (human-readable description), `total_area` (living + garden), `best_offer` (max offer price)
- `ud_estate.property.offer` — buyer offers; computed `date_deadline` with inverse (based on `validity` days); accepting an offer sets property state to `accepted`
- `ud_estate.property.type` — seeded master data (Residential, Commercial, Industrial, Land)
- `ud_estate.property.tag` — many2many tags
- `ud_estate.dashboard` — reporting/KPI model
- `res.users` (inherited) — adds property relation to Odoo users

**Security (`security/`):**
- `ud_security.xml` — two groups: `estate_group_user` (Agent) and `estate_group_manager` (Manager)
- Record rules: Agents see only their own or unassigned properties; Managers see all
- `ir.model.access.csv` — Managers get CRUD (no delete on properties); Agents get read/create/update on properties and full CRUD on offers; base users get read

### Module: `ud_estate_account`

Inherits `ud_estate.property` and overrides `action_set_sold()` to auto-create an account invoice with two lines: the property sale price and a fixed €100 administrative fee.

### Docker Setup

- `web` service: Odoo 18 on port 8069 (exposed internally only; fronted by a reverse proxy on VPS)
- `db` service: PostgreSQL 17
- Odoo config: `config/odoo.conf` — addons path `/mnt/extra-addons`, DB host `db`
- Networks: `internal` (web↔db), `proxy` (external, for reverse proxy access to web)
