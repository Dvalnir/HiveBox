FROM python:3.13-alpine@sha256:18159b2be11db91f84b8f8f655cd860f805dbd9e49a583ddaac8ab39bf4fe1a7
RUN addgroup hivebox && adduser -G hivebox -D hivebox
USER hivebox
WORKDIR /home/hivebox
COPY --chown=hivebox:hivebox requirements.txt .
RUN python -m pip install --no-cache-dir --requirement requirements.txt
COPY --chown=hivebox:hivebox src src/
EXPOSE 80/tcp
EXPOSE 80/udp
ENTRYPOINT ["python", "-m", "fastapi"]
CMD ["run", "./src/hive_box/main.py", "--port", "80", "--proxy-headers"]
