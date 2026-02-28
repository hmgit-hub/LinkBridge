# 多阶段构建
FROM --platform=$BUILDPLATFORM python:3.12-slim AS builder

ARG BUILDPLATFORM
ARG TARGETPLATFORM
ARG TARGETOS
ARG TARGETARCH

WORKDIR /app

COPY requirements.txt .

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --user -r requirements.txt

# 运行时镜像
FROM --platform=$TARGETPLATFORM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.local/bin:$PATH"

COPY --from=builder /root/.local /root/.local
COPY . .

RUN mkdir -p /app/plugins && \
    chmod +x /app/.local/bin/*

EXPOSE 8000

CMD ["python", "main.py"]
