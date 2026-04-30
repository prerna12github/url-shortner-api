FROM ghcr.io/astral-sh/uv:alpine3.22
WORKDIR /app
COPY . .
RUN uv sync
EXPOSE 8000
CMD ["fastapi", "run"]