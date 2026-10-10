# hello-axum

The small Rust app Setu uses in its end-to-end tests
([`apps/hello`](https://github.com/setucp/setu/tree/main/apps/hello)),
published here as a sample: an Axum server with a PostgreSQL-backed
notes table, two data directories and a `/healthz` endpoint.

The release archive
`hello-axum-0.1.0-x86_64-unknown-linux-musl.tar.gz` (in this repository's
[`hello-axum-0.1.0`](https://github.com/setucp/manifests/releases/tag/hello-axum-0.1.0)
release) holds one top-level folder:

```
hello-axum-0.1.0-x86_64-unknown-linux-musl/
  hello      static musl executable
  VERSION
```

so the manifest's `exec` is
`hello-axum-0.1.0-x86_64-unknown-linux-musl/hello`. It was built from the
Setu repository with

```sh
CC_x86_64_unknown_linux_musl=clang \
  cargo build --release --target x86_64-unknown-linux-musl -p hello
```

| variable | source |
|---|---|
| `HELLO_BIND` | `bind_addr` (127.0.0.1:port) |
| `DATABASE_URL` | the site's database |
| `HELLO_UPLOADS_DIR`, `HELLO_STATE_DIR` | `data/uploads`, `data/state` |
| `HELLO_NAME`, `HELLO_VERSION` | constants shown on `/` |
