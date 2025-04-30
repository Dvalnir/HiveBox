FROM python:3.13-alpine@sha256:18159b2be11db91f84b8f8f655cd860f805dbd9e49a583ddaac8ab39bf4fe1a7
RUN addgroup hivebox && adduser -G hivebox -D hivebox
USER hivebox
WORKDIR /home/hivebox
COPY --from=ghcr.io/astral-sh/uv:0.7.2-alpine@sha256:c7b64811537bb43384150d3fa35c7cd42309d1ef45727d45df0619c14415b121 \
/usr/local/bin/uv /usr/local/bin/uvx /bin/
COPY --chown=hivebox:hivebox pyproject.toml .
COPY --chown=hivebox:hivebox uv.lock .
COPY --chown=hivebox:hivebox src src/
RUN uv sync --no-dev --locked
EXPOSE 80/tcp
EXPOSE 80/udp
ENTRYPOINT ["uv", "run", "fastapi"]
CMD ["run", "./src/hive_box/main.py", "--port", "80", "--proxy-headers"]
