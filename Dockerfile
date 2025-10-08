FROM python:3.14-alpine@sha256:0bf59161c735f604ea070af402d65b1a088ce3fd7fe4329f5983446148e84930
RUN addgroup hivebox && adduser -G hivebox -D hivebox
USER hivebox
WORKDIR /home/hivebox
COPY --from=ghcr.io/astral-sh/uv:0.7.2-alpine@sha256:c7b64811537bb43384150d3fa35c7cd42309d1ef45727d45df0619c14415b121 \
/usr/local/bin/uv /usr/local/bin/uvx /bin/
COPY --chown=hivebox:hivebox README.md pyproject.toml uv.lock ./
COPY --chown=hivebox:hivebox src src/
RUN uv sync --no-dev --locked
EXPOSE 80/tcp
EXPOSE 80/udp
ENTRYPOINT ["uv", "run", "fastapi"]
CMD ["run", "./src/hive_box/main.py", "--port", "80", "--proxy-headers"]
