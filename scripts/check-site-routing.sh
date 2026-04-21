#!/usr/bin/env bash
set -euo pipefail

base_url="${1:-http://127.0.0.1}"
base_url="${base_url%/}"

tmp_dir="$(mktemp -d)"
trap 'rm -rf "$tmp_dir"' EXIT

root_headers="$tmp_dir/root.headers"
admin_headers="$tmp_dir/admin.headers"
root_body="$tmp_dir/root.html"
admin_body="$tmp_dir/admin.html"

curl -fsSL -D "$root_headers" "$base_url/" -o "$root_body"
curl -fsSL -D "$admin_headers" "$base_url/admin/" -o "$admin_body"

if ! grep -qi '^X-App-Name: frontend$' "$root_headers"; then
  echo "Expected / to return X-App-Name: frontend"
  echo "Actual headers:"
  cat "$root_headers"
  exit 1
fi

if ! grep -qi '^X-App-Name: admin$' "$admin_headers"; then
  echo "Expected /admin/ to return X-App-Name: admin"
  echo "Actual headers:"
  cat "$admin_headers"
  exit 1
fi

if ! grep -q '<title>MFS</title>' "$root_body"; then
  echo "Expected / to serve the public frontend HTML"
  exit 1
fi

if ! grep -q '/admin/assets/' "$admin_body"; then
  echo "Expected /admin/ to serve the admin frontend HTML"
  exit 1
fi

echo "Routing is correct for $base_url"
