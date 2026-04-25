# Caddy Migration Design

## Goal

Replace the external `nginx` + manual `certbot` edge layer with `caddy`, so HTTPS is managed by Caddy itself.

## Scope

- Remove `nginx` and `certbot` services from `docker-compose.yml`
- Add a new `caddy` service exposing ports `80` and `443`
- Persist Caddy state in dedicated Docker volumes for ACME data and runtime config
- Replace the old `nginx/default.conf` with a repository-level `Caddyfile`
- Leave `Caddyfile` intentionally empty so it can be filled manually later

## Notes

- Until the `Caddyfile` is filled with site and reverse proxy directives, the stack will not serve the application routes
- Automatic HTTPS will only start working after a valid site block is added to `Caddyfile`
- Internal app containers (`frontend`, `admin`, `backend`, `grafana`) remain unchanged in this migration
