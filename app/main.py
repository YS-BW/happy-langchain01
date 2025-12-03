from fastapi import FastAPI
from app.api.endpoints import router as AnalyzeRouter
from fastapi.middleware.cors import CORSMiddleware
def create_app() -> FastAPI:
    app = FastAPI(
        title="LangChain Translation and Analysis Demo",
        description="基于 LCEL 和异步 FastAPI 的模块化 AI 服务",
        version="0.1.0",
    )
    origins = [
    "*", # 生产环境中应限制为你的前端域名，但在开发环境中使用 "*" 最方便
    "http://127.0.0.1",
    "http://localhost",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins, # 允许的源（前端域名）
        allow_credentials=True,
        allow_methods=["*"], # 允许所有 HTTP 方法，包括 OPTIONS
        allow_headers=["*"], # 允许所有头部
    )
    # 注册路由
    app.include_router(AnalyzeRouter)
    return app
app = create_app()
