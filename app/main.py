from fastapi import FastAPI
from app.api.endpoints import router as AnalyzeRouter

def create_app() -> FastAPI:
    app = FastAPI(
        title="LangChain Translation and Analysis Demo",
        description="基于 LCEL 和异步 FastAPI 的模块化 AI 服务",
        version="0.1.0",
    )
    # 注册路由
    app.include_router(AnalyzeRouter)
    return app
app = create_app()
