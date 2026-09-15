"""Generated from the OpenAPI document. Do not edit by hand.

Regenerate with:

    python scripts/generate_tools.py openapi.json src/bazarr_mcp/tools.py

One tool per operation, 89 of them, covering the whole API.
"""

from .runtime import _DESTRUCTIVE, _READ, _WRITE, call, mcp


@mcp.tool(annotations=_WRITE)
def create_episodes_blacklist(seriesid: int, episodeid: int, provider: str, subs_id: str, language: str, subtitles_path: str) -> str:
    """Add an episodes subtitles to blacklist.

    POST /api/episodes/blacklist

    Args:
        seriesid: Series ID
        episodeid: Episode ID
        provider: Provider name
        subs_id: Subtitles ID
        language: Subtitles language
        subtitles_path: Subtitles file path
    """
    return call("POST", "/api/episodes/blacklist", query=None, body=None, form={"seriesid": seriesid, "episodeid": episodeid, "provider": provider, "subs_id": subs_id, "language": language, "subtitles_path": subtitles_path})


@mcp.tool(annotations=_WRITE)
def create_episodes_subtitles(seriesid: int, episodeid: int, language: str, forced: str, hi: str, file: str) -> str:
    """Upload an episode subtitles.

    POST /api/episodes/subtitles

    Args:
        seriesid: Series ID
        episodeid: Episode ID
        language: Language code2
        forced: Forced true/false as string
        hi: HI true/false as string
        file: Subtitles file as file upload object
    """
    return call("POST", "/api/episodes/subtitles", query=None, body=None, form={"seriesid": seriesid, "episodeid": episodeid, "language": language, "forced": forced, "hi": hi, "file": file})


@mcp.tool(annotations=_WRITE)
def create_jellyfin_test_connection(url: str, apikey: str) -> str:
    """Test connection to a Jellyfin server with provided credentials.

    POST /api/jellyfin/test-connection

    Args:
        url: Jellyfin server URL
        apikey: Jellyfin API key
    """
    return call("POST", "/api/jellyfin/test-connection", query=None, body=None, form={"url": url, "apikey": apikey})


@mcp.tool(annotations=_WRITE)
def create_movies(radarrid: list | None = None, profileid: list | None = None) -> str:
    """Update specific movies languages profile.

    POST /api/movies

    Args:
        radarrid: Radarr movie(s) ID
        profileid: Languages profile(s) ID or "none"
    """
    return call("POST", "/api/movies", query=None, body=None, form={"radarrid": radarrid, "profileid": profileid})


@mcp.tool(annotations=_WRITE)
def create_movies_blacklist(radarrid: int, provider: str, subs_id: str, language: str, subtitles_path: str) -> str:
    """Add a movies subtitles to blacklist.

    POST /api/movies/blacklist

    Args:
        radarrid: Radarr ID
        provider: Provider name
        subs_id: Subtitles ID
        language: Subtitles language
        subtitles_path: Subtitles file path
    """
    return call("POST", "/api/movies/blacklist", query=None, body=None, form={"radarrid": radarrid, "provider": provider, "subs_id": subs_id, "language": language, "subtitles_path": subtitles_path})


@mcp.tool(annotations=_WRITE)
def create_movies_subtitles(radarrid: int, language: str, forced: str, hi: str, file: str) -> str:
    """Upload a movie subtitles.

    POST /api/movies/subtitles

    Args:
        radarrid: Movie ID
        language: Language code2
        forced: Forced true/false as string
        hi: HI true/false as string
        file: Subtitles file as file upload object
    """
    return call("POST", "/api/movies/subtitles", query=None, body=None, form={"radarrid": radarrid, "language": language, "forced": forced, "hi": hi, "file": file})


@mcp.tool(annotations=_WRITE)
def create_plex_apikey(apikey: str) -> str:
    """POST plex/apikey.

    POST /api/plex/apikey

    Args:
        apikey: API key
    """
    return call("POST", "/api/plex/apikey", query=None, body=None, form={"apikey": apikey})


@mcp.tool(annotations=_WRITE)
def create_plex_encrypt_apikey() -> str:
    """POST plex/encrypt-apikey.

    POST /api/plex/encrypt-apikey
    """
    return call("POST", "/api/plex/encrypt-apikey", query=None, body=None, form=None)


@mcp.tool(annotations=_WRITE)
def create_plex_oauth_logout() -> str:
    """POST plex/oauth/logout.

    POST /api/plex/oauth/logout
    """
    return call("POST", "/api/plex/oauth/logout", query=None, body=None, form=None)


@mcp.tool(annotations=_WRITE)
def create_plex_oauth_pin(client_id: str | None = None) -> str:
    """POST plex/oauth/pin.

    POST /api/plex/oauth/pin

    Args:
        client_id: Client ID
    """
    return call("POST", "/api/plex/oauth/pin", query=None, body=None, form={"clientId": client_id})


@mcp.tool(annotations=_WRITE)
def create_plex_select_server(machine_identifier: str, name: str, uri: str, local: str | None = None, connections: str | None = None) -> str:
    """POST plex/select-server.

    POST /api/plex/select-server

    Args:
        machine_identifier: Machine identifier
        name: Server name
        uri: Connection URI
        local: Is local connection
        connections: All available connection URIs
    """
    return call("POST", "/api/plex/select-server", query=None, body=None, form={"machineIdentifier": machine_identifier, "name": name, "uri": uri, "local": local, "connections": connections})


@mcp.tool(annotations=_WRITE)
def create_plex_test_connection(uri: str) -> str:
    """POST plex/test-connection.

    POST /api/plex/test-connection

    Args:
        uri: Server URI
    """
    return call("POST", "/api/plex/test-connection", query=None, body=None, form={"uri": uri})


@mcp.tool(annotations=_WRITE)
def create_plex_webhook_create() -> str:
    """POST plex/webhook/create.

    POST /api/plex/webhook/create
    """
    return call("POST", "/api/plex/webhook/create", query=None, body=None, form=None)


@mcp.tool(annotations=_WRITE)
def create_plex_webhook_delete(webhook_url: str) -> str:
    """POST plex/webhook/delete.

    POST /api/plex/webhook/delete

    Args:
        webhook_url: Webhook URL to delete
    """
    return call("POST", "/api/plex/webhook/delete", query=None, body=None, form={"webhook_url": webhook_url})


@mcp.tool(annotations=_WRITE)
def create_providers(action: str) -> str:
    """Reset providers status.

    POST /api/providers

    Args:
        action: Action to perform from ["reset"]
    """
    return call("POST", "/api/providers", query=None, body=None, form={"action": action})


@mcp.tool(annotations=_WRITE)
def create_providers_episodes(seriesid: int, episodeid: int, hi: str, forced: str, original_format: str, provider: str, subtitle: str) -> str:
    """Manually download an episode subtitles.

    POST /api/providers/episodes

    Args:
        seriesid: Series ID
        episodeid: Episode ID
        hi: HI subtitles from ["True", "False"]
        forced: Forced subtitles from ["True", "False"]
        original_format: Use original subtitles format from ["True", "False"]
        provider: Provider name
        subtitle: Subtitle ID as returned by GET
    """
    return call("POST", "/api/providers/episodes", query=None, body=None, form={"seriesid": seriesid, "episodeid": episodeid, "hi": hi, "forced": forced, "original_format": original_format, "provider": provider, "subtitle": subtitle})


@mcp.tool(annotations=_WRITE)
def create_providers_movies(radarrid: int, hi: str, forced: str, original_format: str, provider: str, subtitle: str) -> str:
    """Manually download a movie subtitles.

    POST /api/providers/movies

    Args:
        radarrid: Movie ID
        hi: HI subtitles from ["True", "False"]
        forced: Forced subtitles from ["True", "False"]
        original_format: Use original subtitles format from ["True", "False"]
        provider: Provider name
        subtitle: Subtitle ID as returned by GET
    """
    return call("POST", "/api/providers/movies", query=None, body=None, form={"radarrid": radarrid, "hi": hi, "forced": forced, "original_format": original_format, "provider": provider, "subtitle": subtitle})


@mcp.tool(annotations=_WRITE)
def create_series(seriesid: list | None = None, profileid: list | None = None) -> str:
    """Update specific series languages profile.

    POST /api/series

    Args:
        seriesid: Sonarr series ID
        profileid: Languages profile(s) ID or "none"
    """
    return call("POST", "/api/series", query=None, body=None, form={"seriesid": seriesid, "profileid": profileid})


@mcp.tool(annotations=_WRITE)
def create_system(action: str) -> str:
    """Shutdown or restart Bazarr.

    POST /api/system

    Args:
        action: Action to perform from ["shutdown", "restart"]
    """
    return call("POST", "/api/system", query=None, body=None, form={"action": action})


@mcp.tool(annotations=_WRITE)
def create_system_account(action: str, username: str | None = None, password: str | None = None) -> str:
    """Login or logout from Bazarr UI when using form login.

    POST /api/system/account

    Args:
        action: Action from ["login", "logout"]
        username: Bazarr username
        password: Bazarr password
    """
    return call("POST", "/api/system/account", query=None, body=None, form={"action": action, "username": username, "password": password})


@mcp.tool(annotations=_WRITE)
def create_system_announcements(hash_: str) -> str:
    """Mark announcement as dismissed.

    POST /api/system/announcements

    Args:
        hash_: hash of the announcement to dismiss
    """
    return call("POST", "/api/system/announcements", query=None, body=None, form={"hash": hash_})


@mcp.tool(annotations=_WRITE)
def create_system_backups() -> str:
    """Create a new backup.

    POST /api/system/backups
    """
    return call("POST", "/api/system/backups", query=None, body=None, form=None)


@mcp.tool(annotations=_WRITE)
def create_system_jobs(id_: int, action: str) -> str:
    """Force start, move to top or move to bottom of the queue a specific job.

    POST /api/system/jobs

    Args:
        id_: Job ID act onto
        action: Action to perform from ["force_start", "move_top", "move_bottom"]
    """
    return call("POST", "/api/system/jobs", query=None, body=None, form={"id": id_, "action": action})


@mcp.tool(annotations=_WRITE)
def create_system_settings() -> str:
    """POST system/settings.

    POST /api/system/settings
    """
    return call("POST", "/api/system/settings", query=None, body=None, form=None)


@mcp.tool(annotations=_WRITE)
def create_system_tasks(taskid: str) -> str:
    """Run task.

    POST /api/system/tasks

    Args:
        taskid: Task id of the task to run
    """
    return call("POST", "/api/system/tasks", query=None, body=None, form={"taskid": taskid})


@mcp.tool(annotations=_WRITE)
def create_system_webhooks_test() -> str:
    """Test external webhook connection.

    POST /api/system/webhooks/test
    """
    return call("POST", "/api/system/webhooks/test", query=None, body=None, form=None)


@mcp.tool(annotations=_WRITE)
def create_webhooks_plex(payload: str) -> str:
    """Trigger subtitles search on play media event in Plex.

    POST /api/webhooks/plex

    Args:
        payload: Webhook payload
    """
    return call("POST", "/api/webhooks/plex", query=None, body=None, form={"payload": payload})


@mcp.tool(annotations=_WRITE)
def create_webhooks_radarr() -> str:
    """Search for missing subtitles based on Radarr webhooks.

    POST /api/webhooks/radarr
    """
    return call("POST", "/api/webhooks/radarr", query=None, body=None, form=None)


@mcp.tool(annotations=_WRITE)
def create_webhooks_sonarr() -> str:
    """Search for missing subtitles based on Sonarr webhooks.

    POST /api/webhooks/sonarr
    """
    return call("POST", "/api/webhooks/sonarr", query=None, body=None, form=None)


@mcp.tool(annotations=_DESTRUCTIVE)
def delete_episodes_blacklist(all_: str | None = None, provider: str | None = None, subs_id: str | None = None) -> str:
    """Delete an episodes subtitles from blacklist.

    DELETE /api/episodes/blacklist

    Args:
        all_: Empty episodes subtitles blacklist
        provider: Provider name
        subs_id: Subtitles ID
    """
    return call("DELETE", "/api/episodes/blacklist", query=None, body=None, form={"all": all_, "provider": provider, "subs_id": subs_id})


@mcp.tool(annotations=_DESTRUCTIVE)
def delete_episodes_subtitles(seriesid: int, episodeid: int, language: str, forced: str, hi: str, path: str) -> str:
    """Delete an episode subtitles.

    DELETE /api/episodes/subtitles

    Args:
        seriesid: Series ID
        episodeid: Episode ID
        language: Language code2
        forced: Forced true/false as string
        hi: HI true/false as string
        path: Path of the subtitles file
    """
    return call("DELETE", "/api/episodes/subtitles", query=None, body=None, form={"seriesid": seriesid, "episodeid": episodeid, "language": language, "forced": forced, "hi": hi, "path": path})


@mcp.tool(annotations=_DESTRUCTIVE)
def delete_movies_blacklist(all_: str | None = None, provider: str | None = None, subs_id: str | None = None) -> str:
    """Delete a movies subtitles from blacklist.

    DELETE /api/movies/blacklist

    Args:
        all_: Empty movies subtitles blacklist
        provider: Provider name
        subs_id: Subtitles ID
    """
    return call("DELETE", "/api/movies/blacklist", query=None, body=None, form={"all": all_, "provider": provider, "subs_id": subs_id})


@mcp.tool(annotations=_DESTRUCTIVE)
def delete_movies_subtitles(radarrid: int, language: str, forced: str, hi: str, path: str) -> str:
    """Delete a movie subtitles.

    DELETE /api/movies/subtitles

    Args:
        radarrid: Movie ID
        language: Language code2
        forced: Forced true/false as string
        hi: HI true/false as string
        path: Path of the subtitles file
    """
    return call("DELETE", "/api/movies/subtitles", query=None, body=None, form={"radarrid": radarrid, "language": language, "forced": forced, "hi": hi, "path": path})


@mcp.tool(annotations=_DESTRUCTIVE)
def delete_system_backups(filename: str) -> str:
    """Delete a backup file.

    DELETE /api/system/backups

    Args:
        filename: Backups to delete filename
    """
    return call("DELETE", "/api/system/backups", query=None, body=None, form={"filename": filename})


@mcp.tool(annotations=_DESTRUCTIVE)
def delete_system_jobs(id_: int) -> str:
    """Delete a job from the queue.

    DELETE /api/system/jobs

    Args:
        id_: Job ID to delete from queue
    """
    return call("DELETE", "/api/system/jobs", query=None, body=None, form={"id": id_})


@mcp.tool(annotations=_DESTRUCTIVE)
def delete_system_logs() -> str:
    """Force log rotation and create a new log file.

    DELETE /api/system/logs
    """
    return call("DELETE", "/api/system/logs", query=None, body=None, form=None)


@mcp.tool(annotations=_READ)
def get_plex_oauth_pin_by_pin_id_check(pin_id: str) -> str:
    """GET plex/oauth/pin/<string:pin_id>/check.

    GET /api/plex/oauth/pin/{pin_id}/check

    Args:
        pin_id: Path parameter.
    """
    return call("GET", f"/api/plex/oauth/pin/{pin_id}/check", query=None, body=None, form=None)


@mcp.tool(annotations=_READ)
def list_badges() -> str:
    """Get badges count to update the UI.

    GET /api/badges
    """
    return call("GET", "/api/badges", query=None, body=None, form=None)


@mcp.tool(annotations=_READ)
def list_episodes(seriesid: list | None = None, episodeid: list | None = None) -> str:
    """List episodes metadata for specific series or episodes.

    GET /api/episodes

    Args:
        seriesid: Series IDs to list episodes for
        episodeid: Episodes ID to list
    """
    return call("GET", "/api/episodes", query={"seriesid[]": seriesid, "episodeid[]": episodeid}, body=None, form=None)


@mcp.tool(annotations=_READ)
def list_episodes_blacklist(start: int | None = None, length: int | None = None) -> str:
    """List blacklisted episodes subtitles.

    GET /api/episodes/blacklist

    Args:
        start: Paging start integer
        length: Paging length integer
    """
    return call("GET", "/api/episodes/blacklist", query={"start": start, "length": length}, body=None, form=None)


@mcp.tool(annotations=_READ)
def list_episodes_history(start: int | None = None, length: int | None = None, episodeid: int | None = None) -> str:
    """List episodes history events.

    GET /api/episodes/history

    Args:
        start: Paging start integer
        length: Paging length integer
        episodeid: Episode ID
    """
    return call("GET", "/api/episodes/history", query={"start": start, "length": length, "episodeid": episodeid}, body=None, form=None)


@mcp.tool(annotations=_READ)
def list_episodes_wanted(start: int | None = None, length: int | None = None, episodeid: list | None = None) -> str:
    """List episodes wanted subtitles.

    GET /api/episodes/wanted

    Args:
        start: Paging start integer
        length: Paging length integer
        episodeid: Episodes ID to list
    """
    return call("GET", "/api/episodes/wanted", query={"start": start, "length": length, "episodeid[]": episodeid}, body=None, form=None)


@mcp.tool(annotations=_READ)
def list_files(path: str | None = None) -> str:
    """List Bazarr file system content.

    GET /api/files

    Args:
        path: Path to browse
    """
    return call("GET", "/api/files", query={"path": path}, body=None, form=None)


@mcp.tool(annotations=_READ)
def list_files_radarr(path: str | None = None) -> str:
    """List Radarr file system content.

    GET /api/files/radarr

    Args:
        path: Path to browse
    """
    return call("GET", "/api/files/radarr", query={"path": path}, body=None, form=None)


@mcp.tool(annotations=_READ)
def list_files_sonarr(path: str | None = None) -> str:
    """List Sonarr file system content.

    GET /api/files/sonarr

    Args:
        path: Path to browse
    """
    return call("GET", "/api/files/sonarr", query={"path": path}, body=None, form=None)


@mcp.tool(annotations=_READ)
def list_history_stats(time_frame: str | None = None, action: str | None = None, provider: str | None = None, language: str | None = None) -> str:
    """Get history statistics.

    GET /api/history/stats

    Args:
        time_frame: Timeframe to get stats for. Must be in ["week", "month", "trimester", "year"]
        action: Action type to filter for.
        provider: Provider name to filter for.
        language: Language name to filter for
    """
    return call("GET", "/api/history/stats", query={"timeFrame": time_frame, "action": action, "provider": provider, "language": language}, body=None, form=None)


@mcp.tool(annotations=_READ)
def list_jellyfin_libraries(url: str | None = None, apikey: str | None = None) -> str:
    """List available movie and series libraries from the Jellyfin server.

    GET /api/jellyfin/libraries

    Args:
        url: Jellyfin server URL
        apikey: Jellyfin API key
    """
    return call("GET", "/api/jellyfin/libraries", query={"url": url, "apikey": apikey}, body=None, form=None)


@mcp.tool(annotations=_READ)
def list_movies(start: int | None = None, length: int | None = None, radarrid: list | None = None) -> str:
    """List movies metadata for specific movies.

    GET /api/movies

    Args:
        start: Paging start integer
        length: Paging length integer
        radarrid: Movies IDs to get metadata for
    """
    return call("GET", "/api/movies", query={"start": start, "length": length, "radarrid[]": radarrid}, body=None, form=None)


@mcp.tool(annotations=_READ)
def list_movies_blacklist(start: int | None = None, length: int | None = None) -> str:
    """List blacklisted movies subtitles.

    GET /api/movies/blacklist

    Args:
        start: Paging start integer
        length: Paging length integer
    """
    return call("GET", "/api/movies/blacklist", query={"start": start, "length": length}, body=None, form=None)


@mcp.tool(annotations=_READ)
def list_movies_history(start: int | None = None, length: int | None = None, radarrid: int | None = None) -> str:
    """List movies history events.

    GET /api/movies/history

    Args:
        start: Paging start integer
        length: Paging length integer
        radarrid: Movie ID
    """
    return call("GET", "/api/movies/history", query={"start": start, "length": length, "radarrid": radarrid}, body=None, form=None)


@mcp.tool(annotations=_READ)
def list_movies_tags() -> str:
    """List all distinct tags assigned to any movie.

    GET /api/movies/tags
    """
    return call("GET", "/api/movies/tags", query=None, body=None, form=None)


@mcp.tool(annotations=_READ)
def list_movies_wanted(start: int | None = None, length: int | None = None, radarrid: list | None = None) -> str:
    """List movies wanted subtitles.

    GET /api/movies/wanted

    Args:
        start: Paging start integer
        length: Paging length integer
        radarrid: Movies ID to list
    """
    return call("GET", "/api/movies/wanted", query={"start": start, "length": length, "radarrid[]": radarrid}, body=None, form=None)


@mcp.tool(annotations=_READ)
def list_plex_autopulse_config() -> str:
    """GET plex/autopulse/config.

    GET /api/plex/autopulse/config
    """
    return call("GET", "/api/plex/autopulse/config", query=None, body=None, form=None)


@mcp.tool(annotations=_READ)
def list_plex_oauth_libraries() -> str:
    """GET plex/oauth/libraries.

    GET /api/plex/oauth/libraries
    """
    return call("GET", "/api/plex/oauth/libraries", query=None, body=None, form=None)


@mcp.tool(annotations=_READ)
def list_plex_oauth_pin() -> str:
    """GET plex/oauth/pin.

    GET /api/plex/oauth/pin
    """
    return call("GET", "/api/plex/oauth/pin", query=None, body=None, form=None)


@mcp.tool(annotations=_READ)
def list_plex_oauth_servers() -> str:
    """GET plex/oauth/servers.

    GET /api/plex/oauth/servers
    """
    return call("GET", "/api/plex/oauth/servers", query=None, body=None, form=None)


@mcp.tool(annotations=_READ)
def list_plex_oauth_validate() -> str:
    """GET plex/oauth/validate.

    GET /api/plex/oauth/validate
    """
    return call("GET", "/api/plex/oauth/validate", query=None, body=None, form=None)


@mcp.tool(annotations=_READ)
def list_plex_select_server() -> str:
    """GET plex/select-server.

    GET /api/plex/select-server
    """
    return call("GET", "/api/plex/select-server", query=None, body=None, form=None)


@mcp.tool(annotations=_READ)
def list_plex_test_connection() -> str:
    """GET plex/test-connection.

    GET /api/plex/test-connection
    """
    return call("GET", "/api/plex/test-connection", query=None, body=None, form=None)


@mcp.tool(annotations=_READ)
def list_plex_webhook_list() -> str:
    """GET plex/webhook/list.

    GET /api/plex/webhook/list
    """
    return call("GET", "/api/plex/webhook/list", query=None, body=None, form=None)


@mcp.tool(annotations=_READ)
def list_providers(history: str | None = None) -> str:
    """Get providers status.

    GET /api/providers

    Args:
        history: Provider name for history stats
    """
    return call("GET", "/api/providers", query={"history": history}, body=None, form=None)


@mcp.tool(annotations=_READ)
def list_providers_episodes(episodeid: int | None = None) -> str:
    """Search manually for an episode subtitles.

    GET /api/providers/episodes

    Args:
        episodeid: Episode ID
    """
    return call("GET", "/api/providers/episodes", query={"episodeid": episodeid}, body=None, form=None)


@mcp.tool(annotations=_READ)
def list_providers_movies(radarrid: int | None = None) -> str:
    """Search manually for a movie subtitles.

    GET /api/providers/movies

    Args:
        radarrid: Movie ID
    """
    return call("GET", "/api/providers/movies", query={"radarrid": radarrid}, body=None, form=None)


@mcp.tool(annotations=_READ)
def list_series(start: int | None = None, length: int | None = None, seriesid: list | None = None) -> str:
    """List series metadata for specific series.

    GET /api/series

    Args:
        start: Paging start integer
        length: Paging length integer
        seriesid: Series IDs to get metadata for
    """
    return call("GET", "/api/series", query={"start": start, "length": length, "seriesid[]": seriesid}, body=None, form=None)


@mcp.tool(annotations=_READ)
def list_series_tags() -> str:
    """List all distinct tags assigned to any series.

    GET /api/series/tags
    """
    return call("GET", "/api/series/tags", query=None, body=None, form=None)


@mcp.tool(annotations=_READ)
def list_subtitles(subtitles_path: str | None = None, sonarr_episode_id: int | None = None, radarr_movie_id: int | None = None) -> str:
    """Return available audio and embedded subtitles tracks with external subtitles. Used for manual subsync.

    GET /api/subtitles

    Args:
        subtitles_path: External subtitles file path
        sonarr_episode_id: Sonarr Episode ID
        radarr_movie_id: Radarr Movie ID
    """
    return call("GET", "/api/subtitles", query={"subtitlesPath": subtitles_path, "sonarrEpisodeId": sonarr_episode_id, "radarrMovieId": radarr_movie_id}, body=None, form=None)


@mcp.tool(annotations=_READ)
def list_subtitles_contents(subtitle_path: str | None = None) -> str:
    """Retrieve subtitle file contents.

    GET /api/subtitles/contents

    Args:
        subtitle_path: Subtitle filepath
    """
    return call("GET", "/api/subtitles/contents", query={"subtitlePath": subtitle_path}, body=None, form=None)


@mcp.tool(annotations=_READ)
def list_subtitles_info(filenames: list | None = None) -> str:
    """Guessit over subtitles filename.

    GET /api/subtitles/info

    Args:
        filenames: Subtitles filenames
    """
    return call("GET", "/api/subtitles/info", query={"filenames[]": filenames}, body=None, form=None)


@mcp.tool(annotations=_READ)
def list_system_announcements() -> str:
    """List announcements relative to Bazarr.

    GET /api/system/announcements
    """
    return call("GET", "/api/system/announcements", query=None, body=None, form=None)


@mcp.tool(annotations=_READ)
def list_system_backups() -> str:
    """List backup files.

    GET /api/system/backups
    """
    return call("GET", "/api/system/backups", query=None, body=None, form=None)


@mcp.tool(annotations=_READ)
def list_system_health() -> str:
    """List health issues.

    GET /api/system/health
    """
    return call("GET", "/api/system/health", query=None, body=None, form=None)


@mcp.tool(annotations=_READ)
def list_system_jobs(id_: int | None = None, status: str | None = None) -> str:
    """List jobs from the queue.

    GET /api/system/jobs

    Args:
        id_: Job ID to return
        status: Job status to return
    """
    return call("GET", "/api/system/jobs", query={"id": id_, "status": status}, body=None, form=None)


@mcp.tool(annotations=_READ)
def list_system_languages(history: str | None = None) -> str:
    """List languages for history filter or for language filter menu.

    GET /api/system/languages

    Args:
        history: Language name for history stats
    """
    return call("GET", "/api/system/languages", query={"history": history}, body=None, form=None)


@mcp.tool(annotations=_READ)
def list_system_languages_profiles() -> str:
    """List languages profiles.

    GET /api/system/languages/profiles
    """
    return call("GET", "/api/system/languages/profiles", query=None, body=None, form=None)


@mcp.tool(annotations=_READ)
def list_system_logs() -> str:
    """List log entries.

    GET /api/system/logs
    """
    return call("GET", "/api/system/logs", query=None, body=None, form=None)


@mcp.tool(annotations=_READ)
def list_system_ping() -> str:
    """Return status and http 200.

    GET /api/system/ping
    """
    return call("GET", "/api/system/ping", query=None, body=None, form=None)


@mcp.tool(annotations=_READ)
def list_system_releases() -> str:
    """Get Bazarr releases.

    GET /api/system/releases
    """
    return call("GET", "/api/system/releases", query=None, body=None, form=None)


@mcp.tool(annotations=_READ)
def list_system_searches(query: str | None = None) -> str:
    """List results from query.

    GET /api/system/searches

    Args:
        query: Series or movie name to search for
    """
    return call("GET", "/api/system/searches", query={"query": query}, body=None, form=None)


@mcp.tool(annotations=_READ)
def list_system_settings() -> str:
    """GET system/settings.

    GET /api/system/settings
    """
    return call("GET", "/api/system/settings", query=None, body=None, form=None)


@mcp.tool(annotations=_READ)
def list_system_status() -> str:
    """Return environment information and versions.

    GET /api/system/status
    """
    return call("GET", "/api/system/status", query=None, body=None, form=None)


@mcp.tool(annotations=_READ)
def list_system_tasks(taskid: str | None = None) -> str:
    """List tasks.

    GET /api/system/tasks

    Args:
        taskid: List tasks or a single task properties
    """
    return call("GET", "/api/system/tasks", query={"taskid": taskid}, body=None, form=None)


@mcp.tool(annotations=_WRITE)
def patch_episodes_subtitles(seriesid: int, episodeid: int, language: str, forced: str, hi: str) -> str:
    """Download an episode subtitles.

    PATCH /api/episodes/subtitles

    Args:
        seriesid: Series ID
        episodeid: Episode ID
        language: Language code2
        forced: Forced true/false as string
        hi: HI true/false as string
    """
    return call("PATCH", "/api/episodes/subtitles", query=None, body=None, form={"seriesid": seriesid, "episodeid": episodeid, "language": language, "forced": forced, "hi": hi})


@mcp.tool(annotations=_WRITE)
def patch_movies(radarrid: int | None = None, action: str | None = None) -> str:
    """Run actions on specific movies.

    PATCH /api/movies

    Args:
        radarrid: Radarr movie ID
        action: Action to perform from ["scan-disk", "search-missing", "search-wanted", "sync"]
    """
    return call("PATCH", "/api/movies", query=None, body=None, form={"radarrid": radarrid, "action": action})


@mcp.tool(annotations=_WRITE)
def patch_movies_subtitles(radarrid: int, language: str, forced: str, hi: str) -> str:
    """Download a movie subtitles.

    PATCH /api/movies/subtitles

    Args:
        radarrid: Movie ID
        language: Language code2
        forced: Forced true/false as string
        hi: HI true/false as string
    """
    return call("PATCH", "/api/movies/subtitles", query=None, body=None, form={"radarrid": radarrid, "language": language, "forced": forced, "hi": hi})


@mcp.tool(annotations=_WRITE)
def patch_series(seriesid: int | None = None, action: str | None = None) -> str:
    """Run actions on specific series.

    PATCH /api/series

    Args:
        seriesid: Sonarr series ID
        action: Action to perform from ["scan-disk", "search-missing", "search-wanted", "sync"]
    """
    return call("PATCH", "/api/series", query=None, body=None, form={"seriesid": seriesid, "action": action})


@mcp.tool(annotations=_WRITE)
def patch_subtitles(action: str, language: str, type_: str, id_: int, path: str | None = None, forced: str | None = None, hi: str | None = None, original_format: str | None = None, reference: str | None = None, max_offset_seconds: str | None = None, no_fix_framerate: str | None = None, gss: str | None = None, subtitles_id: int | None = None) -> str:
    """Apply mods/tools on external subtitles.

    PATCH /api/subtitles

    Args:
        action: Action from ["sync", "translate", "extract" or mods name]
        language: Language code2
        path: Subtitles file path
        type_: Media type from ["episode", "movie"]
        id_: Media ID (episodeId, radarrId)
        forced: Forced subtitles from ["True", "False"]
        hi: HI subtitles from ["True", "False"]
        original_format: Use original subtitles format from ["True", "False"]
        reference: Reference to use for sync from video file track number (a:0) or some subtitles file path
        max_offset_seconds: Maximum offset seconds to allow
        no_fix_framerate: Don't try to fix framerate from ["True", "False"]
        gss: Use Golden-Section Search from ["True", "False"]
        subtitles_id: Subtitles database ID (required for the "extract" action)
    """
    return call("PATCH", "/api/subtitles", query=None, body=None, form={"action": action, "language": language, "path": path, "type": type_, "id": id_, "forced": forced, "hi": hi, "original_format": original_format, "reference": reference, "max_offset_seconds": max_offset_seconds, "no_fix_framerate": no_fix_framerate, "gss": gss, "subtitles_id": subtitles_id})


@mcp.tool(annotations=_WRITE)
def patch_system_backups(filename: str) -> str:
    """Restore a backup file.

    PATCH /api/system/backups

    Args:
        filename: Backups to restore filename
    """
    return call("PATCH", "/api/system/backups", query=None, body=None, form={"filename": filename})


@mcp.tool(annotations=_WRITE)
def patch_system_jobs(queue_name: str) -> str:
    """Empty a specific jobs queue.

    PATCH /api/system/jobs

    Args:
        queue_name: Jobs queue name to empty
    """
    return call("PATCH", "/api/system/jobs", query=None, body=None, form={"queueName": queue_name})


@mcp.tool(annotations=_WRITE)
def patch_system_notifications(url: str) -> str:
    """Test a notifications provider URL.

    PATCH /api/system/notifications

    Args:
        url: Notifications provider URL
    """
    return call("PATCH", "/api/system/notifications", query=None, body=None, form={"url": url})
