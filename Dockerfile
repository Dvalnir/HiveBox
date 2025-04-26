FROM python:3.13-alpine
RUN addgroup hivebox && adduser -G hivebox -D hivebox
USER hivebox
WORKDIR /home/hivebox
COPY --chown=hivebox:hivebox requirements.txt .
RUN python -m pip install --no-cache-dir --requirement requirements.txt
COPY --chown=hivebox:hivebox src src/
EXPOSE 80/tcp
EXPOSE 80/udp
ENTRYPOINT ["python", "-m", "fastapi"]
CMD ["run", "./src/HiveBox/main.py", "--port", "80", "--proxy-headers"]
