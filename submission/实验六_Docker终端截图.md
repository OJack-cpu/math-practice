# 实验六 模块三：Docker 终端截图

---

## 截图 1：`docker compose ps` — 运行中的容器

```
NAME                   IMAGE                COMMAND                  SERVICE    CREATED         STATUS                    PORTS
workspace-backend-1    workspace-backend    "uvicorn main:app --…"   backend    49 seconds ago   Up 37 seconds             0.0.0.0:8000->8000/tcp
workspace-db-1         postgres:16-alpine   "docker-entrypoint.s…"   db         49 seconds ago   Up 48 seconds (healthy)   0.0.0.0:5432->5432/tcp
workspace-frontend-1   workspace-frontend   "/docker-entrypoint.…"   frontend   49 seconds ago   Up 36 seconds             0.0.0.0:80->80/tcp
```

> 三个服务全部启动：PostgreSQL (healthy)、FastAPI 后端、Nginx+React 前端。

---

## 截图 2：`docker images` — 构建的镜像

```
REPOSITORY           TAG         IMAGE ID       CREATED              SIZE
workspace-frontend   latest      ecd8580e1211   About a minute ago   51.1MB
workspace-backend    latest      8c1b9fcd3e65   About a minute ago   376MB
postgres             16-alpine   de3a4eab8fdf   38 hours ago         294MB
```

> 前端多阶段构建后仅 51MB，后端 376MB，数据库 294MB。

---

## 截图 3：API 验证 — 后端通过 PostgreSQL 正常返回数据

```
$ curl -s http://localhost:8000/api/knowledge-points

[
    {
        "id": 1,
        "name": "极限与连续",
        "category": "高等数学",
        "description": "数列极限、函数极限、无穷小、连续性、间断点"
    },
    {
        "id": 2,
        "name": "导数与微分",
        "category": "高等数学",
        "description": "导数定义、求导法则、高阶导数、微分中值定理"
    },
    ...
]
```

```
$ curl -s http://localhost:80/
HTTP 200 | Size: 474 bytes
```

> 后端成功连接 PostgreSQL 并返回 21 个知识点数据，前端 Nginx 正常响应 200。

---

## 补充验证：全部 API 端点测试

```
端点                                     结果
─────────────────────────────────────────────────────
/api/knowledge-points                    ✅ 21 个知识点
/api/questions                           ✅ 10 道题目 (分页)
/api/dashboard                           ✅ 题库57道，已答题3次
/api/analysis/weak-points                ✅ 21 个薄弱点
/api/error-book                          ✅ HTTP 200
/api/review/due                          ✅ HTTP 200
/api/stats/correct-rate-trend            ✅ HTTP 200
http://localhost:80/ (前端)              ✅ HTTP 200
```

> 全部 8 个端点验证通过，前端 + 后端 + PostgreSQL 三服务 Docker 编排正常工作。

---

## 截图 4：PostgreSQL 数据库日志

```
db-1  | 2026-07-09 07:35:43.990 UTC [1] LOG:  listening on IPv4 address "0.0.0.0", port 5432
db-1  | 2026-07-09 07:35:43.990 UTC [1] LOG:  listening on IPv6 address "::", port 5432
db-1  | 2026-07-09 07:35:43.999 UTC [1] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
db-1  | 2026-07-09 07:35:44.018 UTC [1] LOG:  database system is ready to accept connections
```

> PostgreSQL 正常监听并接受连接。
---

## 截图 5：浏览器访问前端页面

![前端仪表盘](image.b8d34ca8b8.png)

> 访问地址：http://localhost:80/（通过 CloudStudio 端口 80 预览）
> 页面显示：题库总数 57、总答题数 0、总正确率 0%、正确率趋势、知识点掌握度雷达图。证明前端、后端、PostgreSQL 三服务通过 Docker 编排成功运行。
