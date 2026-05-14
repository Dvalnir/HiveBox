FROM python:3.13.13-alpine3.23@sha256:420cd0bf0f3998275875e02ecd5808168cf0843cbb4d3c536432f729247b2acc
RUN addgroup hivebox && adduser -G hivebox -D hivebox
USER hivebox
WORKDIR /home/hivebox
# Copy uv from the official docker image
COPY --from=ghcr.io/astral-sh/uv:0.11.14@sha256:1025398289b62de8269e70c45b91ffa37c373f38118d7da036fb8bb8efc85d97 /uv /uvx /bin/
# Install dependecies
COPY --chown=hivebox:hivebox pyproject.toml uv.lock ./
COPY --chown=hivebox:hivebox src src/
RUN uv sync --no-dev --locked
EXPOSE 80/tcp
EXPOSE 80/udp
ENTRYPOINT ["uv", "run", "fastapi"]
CMD ["run", "./src/hive_box/main.py", "--port", "80", "--proxy-headers"]
