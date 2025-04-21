FROM python:3-alpine
WORKDIR /HiveBox
COPY requirements.txt .
RUN python -m pip install --no-cache-dir --requirement requirements.txt
COPY src src/
EXPOSE 80/tcp
EXPOSE 80/udp
ENTRYPOINT ["fastapi"]
CMD ["dev", "./src/HiveBox/main.py", "--host", "0.0.0.0", "--port", "80", "--proxy-headers"]
