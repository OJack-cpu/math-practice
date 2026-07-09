# 实验六 模块三：Docker 容器化报告

## 概述

将考研数学刷题系统完整容器化，实现前端、后端、数据库三个服务的 Docker 编排，支持一键部署。

---

## 交付文件清单

| 文件 | 说明 |
|------|------|
| `backend/Dockerfile` | 后端 FastAPI 容器镜像 |
| `frontend/Dockerfile` | 前端 React 多阶段构建镜像 |
| `frontend/nginx.conf` | Nginx 反向代理配置 |
| `docker-compose.yml` | 三服务编排文件 |

---

## 一、后端 Dockerfile

### 设计要点

- **基础镜像**：`python:3.11-slim`（轻量级，减少镜像体积）
- **系统依赖**：安装 `gcc` + `libpq-dev` 以支持 psycopg2 编译
- **缓存优化**：先复制 `requirements.txt` 再 `pip install`，利用 Docker 层缓存
- **安全加固**：使用非 root 用户 `appuser` 运行
- **生产就绪**：默认不启用热重载，通过 `ENV=development` 可切换

### Dockerfile 内容

```dockerfile
FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 二、前端 Dockerfile

### 多阶段构建设计

采用两阶段构建策略，将构建依赖与运行时分离：

**Stage 1 — 构建阶段 (node:20-alpine)**：
- 安装 npm 依赖（`npm ci` 利用锁定文件保证可复现）
- 执行 `vite build` 生成静态文件到 `dist/`

**Stage 2 — 运行阶段 (nginx:1.25-alpine)**：
- 仅复制 `dist/` 目录和 `nginx.conf`
- 最终镜像不包含 node_modules 和源码，体积大幅缩小

```dockerfile
# Stage 1: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci --silent
COPY . .
RUN npm run build

# Stage 2: Serve
FROM nginx:1.25-alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

---

## 三、Nginx 反向代理配置

### 路由策略

| 路径 | 处理方式 | 说明 |
|------|----------|------|
| `/` | 静态文件 | SPA 模式，`try_files $uri /index.html` |
| `/api/` | 反向代理 | 转发到 `http://backend:8000` |

```nginx
server {
    listen 80;
    location / {
        root /usr/share/nginx/html;
        index index.html;
        try_files $uri $uri/ /index.html;
    }
    location /api/ {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### 关键设计
- `try_files $uri $uri/ /index.html`：支持 React Router 的 SPA 路由
- `proxy_set_header`：正确传递客户端 IP 和协议信息
- 服务名 `backend` 通过 Docker Compose 的网络 DNS 解析

---

## 四、docker-compose.yml 编排

### 服务拓扑

```
                    ┌─────────────┐
     Port 80 ──────▶│  frontend   │ (Nginx + React)
                    │  (nginx)    │
                    └──────┬──────┘
                           │ /api/* → backend:8000
                    ┌──────▼──────┐
     Port 8000 ────▶│  backend    │ (FastAPI + uvicorn)
                    │  (python)   │
                    └──────┬──────┘
                           │ postgresql://db:5432
                    ┌──────▼──────┐
     Port 5432 ────▶│     db      │ (PostgreSQL 16)
                    │  (postgres) │
                    └─────────────┘
```

### 关键配置

**数据库健康检查**：
```yaml
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U mathapp -d math_practice"]
  interval: 5s
  timeout: 5s
  retries: 5
```

**服务依赖**：
```yaml
depends_on:
  db:
    condition: service_healthy  # 等待数据库就绪后再启动
```

**环境变量注入**：
- `DATABASE_URL`: PostgreSQL 连接串，使用服务名 `db` 而非 IP
- `ALLOWED_ORIGINS`: CORS 白名单

**数据持久化**：
```yaml
volumes:
  pgdata:  # 命名卷，容器销毁后数据保留
```

---

## 五、部署步骤

```bash
# 1. 构建并启动所有服务
docker compose up -d

# 2. 查看服务状态
docker compose ps

# 3. 查看后端日志（种子数据自动填充）
docker compose logs backend

# 4. 访问应用
# 前端：http://localhost
# API 文档：http://localhost:8000/docs
```

---

## 六、镜像大小估计

| 服务 | 基础镜像 | 预估大小 |
|------|----------|----------|
| backend | python:3.11-slim (~150MB) | ~200MB |
| frontend | nginx:1.25-alpine (~10MB) | ~15MB |
| db | postgres:16-alpine (~120MB) | ~120MB (不含数据) |

---

## 七、设计决策总结

1. **服务名通信**：容器间使用 Docker DNS 服务名（如 `db`、`backend`），不使用 IP
2. **健康检查**：确保数据库先就绪再启动后端，避免启动时序问题
3. **多阶段构建**：前端镜像体积从 ~500MB 减少到 ~15MB
4. **非 root 用户**：后端容器以 `appuser` 运行，遵循安全最佳实践
5. **配置外置**：所有环境相关参数通过环境变量注入，支持不同环境部署
