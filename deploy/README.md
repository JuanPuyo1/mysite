# VPS deployment (Hostinger + Caddy)

## One-time VPS setup

```bash
ssh root@152.239.114.205

apt update && apt install -y docker.io docker-compose-plugin
mkdir -p /opt/esteban-site/data
cd /opt/esteban-site
```

Copy `docker-compose.yml` and create `.env` on the VPS (see project docs or your local copy).

If port `8001` is already used by another container, pick another host port:

```env
HOST_PORT=8002
```

Log in to GitHub Container Registry (only if the package is private):

```bash
echo YOUR_GITHUB_PAT | docker login ghcr.io -u YOUR_GITHUB_USERNAME --password-stdin
```

## Caddy

Add the block from `deploy/Caddyfile.snippet` to your existing Caddyfile.
Match the `reverse_proxy` port to `HOST_PORT` in `.env` (default `8001`).

Reload Caddy after editing:

```bash
caddy validate --config /etc/caddy/Caddyfile
systemctl reload caddy
```

The app binds to `127.0.0.1` only — Caddy is the public entry point on `:443`.

## Deploy a new release

After pushing to `main`, GitHub Actions builds and pushes `ghcr.io/juanpuyo1/mysite:latest`.

On the VPS:

```bash
cd /opt/esteban-site
docker pull ghcr.io/juanpuyo1/mysite:latest
docker compose up -d
```
