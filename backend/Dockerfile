# 考研数学刷题系统 —— 后端 Dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖（psycopg2 编译需要）
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# 先复制依赖文件，利用 Docker 缓存层
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建非 root 用户运行
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# 生产环境不启用 reload；通过 ENV=development 可开启热重载
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
