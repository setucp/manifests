# Setu manifests

Ready-to-use app manifests for [Setu](https://github.com/setucp/setu), the
control panel for single-binary web apps.

## What a manifest is

A manifest is one TOML file per app version. It is the only app-specific
knowledge Setu has: where to download the release (and its sha256), which
executable to run, whether the app needs a PostgreSQL database or
persistent directories, how its environment is built (bind address,
database URL, generated secrets, a one-time admin password), its health
endpoint, default resource limits, and what a backup holds.

The full reference is
[docs/MANIFEST.md](https://github.com/setucp/setu/blob/main/docs/MANIFEST.md)
in the Setu repository.

## Using one

In the panel: **Apps → Add**, then paste the file or its raw URL. Or with
the API:

```sh
curl -X POST https://<panel>/api/v1/apps \
  -H 'Content-Type: application/json' -H 'Origin: https://<panel>' \
  --cookie '<session>' \
  -d '{"url": "https://raw.githubusercontent.com/setucp/manifests/main/miniflux/manifest.toml"}'
```

Then create a site from it (**Sites → New**).

## Manifests

| directory | app | release format |
|---|---|---|
| [`miniflux/`](miniflux/manifest.toml) | [Miniflux](https://miniflux.app) feed reader (Go, PostgreSQL) | bare executable (`format = "binary"`) |
| [`hello-axum/`](hello-axum/) | Setu's Rust sample app (Axum + sqlx) | `tar.gz` archive |
| [`vyasa/`](vyasa/manifest.toml) | [Vyasa](https://github.com/vyasa-cms/vyasa) CMS (Rust, PostgreSQL) | `tar.gz` archive |

## Adding a manifest

1. Create `<app-id>/manifest.toml` (the directory name is the manifest's
   `app.id`).
2. Point `run.binary."x86_64-linux"` at an official release asset and put
   the sha256 you computed from the downloaded file (`sha256sum`), not one
   copied from a web page. Use `format = "binary"` when the asset is the
   executable itself, the default `tar.gz` otherwise.
3. Check it: `POST /api/v1/apps/validate` with the TOML on any Setu panel
   stores nothing and reports every error with its line number.
4. Provision a site from it and confirm the health path answers, then
   open a pull request.

Release URLs are pinned per version; a new upstream version is a new
manifest version (bump `app.version`, `url` and `sha256` together).
