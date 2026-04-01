---
description: How to build and run the project with Docker Compose
---

### Prerequisites

- Docker Engine installed and running.
- Docker Compose plugin (available with recent Docker versions).
- A valid `Dockerfile` for the service you want to build (e.g., `backend/Dockerfile`).

### Steps

1. **Navigate to the project root**
   ```bash
   cd /home/misha/code/FlotyliaSite
   ```
2. **Ensure `docker-compose.yml` references a build context**
   ```yaml
   services:
     web:
       build:
         context: ./backend # directory containing Dockerfile
         dockerfile: Dockerfile
       ports:
         - "8080:8000"
   ```
   _If you already have an `image:` entry pointing to a pre‑built image, skip the `build:` block and make sure the image exists locally or in a registry._
3. **Build the images and start the containers**
   ```bash
   docker compose up --build
   ```
   - `--build` forces rebuilding of images before starting containers.
   - Omit `--build` on subsequent runs if the images are up‑to‑date.
4. **Run in detached mode (optional)**
   ```bash
   docker compose up -d
   ```
   The containers will run in the background.
5. **Stop and remove containers, networks, and volumes**
   ```bash
   docker compose down
   ```
   Add `-v` to also remove named volumes.

### Common Pitfalls

- **Missing image**: `image: myapp-image` will fail unless `myapp-image` exists locally or in a registry. Use `build:` instead to build from your Dockerfile.
- **Incorrect service name**: Ensure you reference the correct service name (`web` in this example) when using commands like `docker compose up web`.
- **Port conflicts**: Make sure host ports (e.g., `8080`) are not already in use.

### Quick Reference

- Build & run: `docker compose up --build`
- Run detached: `docker compose up -d`
- Stop & clean: `docker compose down`
- Rebuild only: `docker compose build`

_Feel free to adjust the `build.context` and `dockerfile` paths to match your project structure._
