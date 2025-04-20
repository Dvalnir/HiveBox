ARG PYTHON_IMAGE="python:3.10-alpine"

# hadolint ignore=DL3006
FROM ${PYTHON_IMAGE} AS builder
WORKDIR /HiveBox
COPY requirements.txt .
RUN python -m pip install --no-cache-dir --requirement requirements.txt
COPY src src/
COPY pyproject.toml .
RUN python -m build

# hadolint ignore=DL3006
FROM ${PYTHON_IMAGE}
WORKDIR /HiveBox
COPY --from=builder /HiveBox/dist/hivebox-*-py3-none-any.whl dist/hivebox-*-py3-none-any.whl
RUN python -m pip install --no-cache-dir ./dist/hivebox-*-py3-none-any.whl
COPY main.py .
CMD ["python", "main.py"]
