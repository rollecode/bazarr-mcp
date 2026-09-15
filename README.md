<center align="center" style="text-align: center;justify-content:center;">
<div align="center" style="text-align: center;justify-content:center;">
<h1 align="center" style="text-align: center;justify-content:center;">

Bazarr MCP server

<img style="justify-content:center;text-align: center;width: 95px; height: auto;" width="793" height="411" alt="image" src="https://github.com/user-attachments/assets/abed1a04-d69b-4ab4-a490-d606064df72d" />
<img style="justify-content:center;text-align: center;width: 49px; height: auto;" alt="Bazarr" src="public/logo.png" />

</h1>


![Version](https://img.shields.io/badge/version-1.0.0-blue.svg?style=for-the-badge) ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Bazarr](https://img.shields.io/badge/Bazarr-3B82F6?style=for-the-badge&logo=bazarr&logoColor=white) ![Coverage](https://img.shields.io/badge/API_coverage-89%2F89-brightgreen?style=for-the-badge)

</div>
</center>

<hr>

Run Bazarr from Claude.ai and Claude Code. All 89 operations of its API are tools. Not a curated subset: every endpoint Bazarr's web interface can reach, this can reach.

<hr>

## Why not the other options

Bazarr publishes no OpenAPI file, so the surface was read out of its source: 60 routed resources carrying 89 handlers.

| Server | Bazarr tools | Coverage |
| --- | --- | --- |
| `davidgibbons/mcp-arr` | 13 | 15 % |
| `GauranshMathur/ARR_MCP` | a handful | partial |
| `bardesss/arr-mcp` | subtitle verbs only | partial |
| This one | **89** | **100 %** |

The others cover wanted lists and a subtitle search. Nothing else exposes the blacklist, subtitle upload, the provider configuration, language profiles, announcements, backups, the task scheduler or the Plex and Jellyfin integrations.

## How it stays complete

Bazarr builds its Swagger at runtime from flask_restx decorators, so there is no file to download. `scripts/extract_spec.py` reads those decorators straight from the source and writes the equivalent OpenAPI document; `scripts/generate_tools.py` then turns it into tools:

```bash
git clone --depth 1 https://github.com/morpheus65535/bazarr.git /tmp/bazarr
python scripts/extract_spec.py /tmp/bazarr/bazarr/api openapi.json
python scripts/generate_tools.py openapi.json src/bazarr_mcp/tools.py
```

A test compares every generated call against every operation in the extracted spec, in both directions. An endpoint Bazarr adds and this misses fails the build; so does a tool pointing at an endpoint that does not exist.

## Tool names

Verb first, derived from the method and path, so the name says what it does:

| Pattern | Meaning | Example |
| --- | --- | --- |
| `list_*` | Read a collection | `list_episodes_wanted`, `list_providers` |
| `get_*_by_id` | Read one record | `list_subtitles_info` |
| `create_*` | POST | `create_episodes_subtitles` |
| `update_*` | PATCH | `update_episodes_subtitles` |
| `delete_*` | DELETE | `delete_episodes_blacklist` |

89 tools is a lot to put in front of a model at once. If your client supports tool filtering, narrow it to the groups you use.

## What is covered

Every namespace: `account`, `announcements`, `backups`, `badges`, `blacklist`, `endpoints`, `episodes`, `episodes_subtitles`, `files`, `files_radarr`, `files_sonarr`, `health`, `history`, `jobs`, `languages`, `languages_profiles`, `logs`, `movies`, `movies_subtitles`, `notifications`, `oauth`, `ping`, `plex`, `providers`, `providers_episodes`, `providers_movies`, `radarr`, `releases`, `searches`, `series`, `settings`, `sonarr`, `stats`, `status`, `subtitles`, `subtitles_contents`, `subtitles_info`, `system`, `tags`, `tasks`, `wanted`.

## Setup

```bash
git clone https://github.com/rollecode/bazarr-mcp.git
cd bazarr-mcp
uv venv && uv pip install -e .
```

```bash
export BAZARR_URL=http://127.0.0.1:6767
export BAZARR_API_KEY=...   # Settings, General, Security, API key
```

### Claude Code

```bash
claude mcp add bazarr -- /path/to/bazarr-mcp/.venv/bin/bazarr-mcp
```

## Writing

Bazarr takes form fields rather than JSON bodies, and these tools send them that way. Settings are read and written whole through `list_system_settings` and `create_system_settings`.

## Hosting it

Running it over HTTP puts it in reach of Claude.ai as a custom connector, and of Claude Code on other machines. Three tiers, the same shape the other servers in this family use:

| Tier | Port | What it does |
| --- | --- | --- |
| `bazarr-mcp` | 8560 | The server. No login of its own, never exposed |
| nginx | 8561 | Front door, behind a Cloudflare Tunnel |
| `auth-server.js` | 8562 | OAuth 2.1 sign-in, or a fixed bearer token |

```bash
npm install
node set-password.js 'a password for the sign-in page'
printf 'BAZARR_URL=...\n' > ~/.config/bazarr-mcp/env
chmod 600 ~/.config/bazarr-mcp/env
```

Copy `systemd/*.service` into `/etc/systemd/system/`, replacing `YOUR_USER` and the `ISSUER` hostname, then:

```bash
sudo systemctl enable --now bazarr-mcp bazarr-mcp-auth
```

Point `nginx/bazarr-mcp.conf` at your own hostname and send the tunnel at `127.0.0.1:8561`.

Environment the server itself reads: `BAZARR_URL, BAZARR_API_KEY`. The sign-in page carries the Bazarr mark and accent colour, set through `APP_NAME`, `APP_ACCENT` and `APP_BLURB` in the auth unit.

### Claude.ai

Settings, Connectors, Add custom connector, URL `https://bazarr-mcp.your-domain/mcp`, client ID and secret blank. The sign-in page asks for the password set above. Connectors belong to the account, so adding it once covers mobile too.

## Development

```bash
uv pip install -e . pytest ruff
.venv/bin/python -m pytest tests
.venv/bin/ruff check .
```

