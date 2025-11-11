from fastapi import Depends, FastAPI, Response

from src.core.config import Settings, get_settings

app = FastAPI(description="Fast API 练习项目实战")


# # 路由引入
# @app.get("/")
# def read_root(
#     # 使用FastAPI的依赖注入系统获取配置实例
#     # FastAPI 会调用 get_settings()，由于缓存的存在，这几乎没有开销
#     settings: Settings = Depends(get_settings),
# ):
#     """
#     一个实例端点，演示如何访问配置
#     """
#     return {
#         "message": f"Hello from the {settings.app_name}!",
#         "detabase_url": settings.db_url,
#         "jwt_secret": settings.jwt_secret,
#     }


@app.get("/health")
async def health_check(response: Response):
    response.status_code = 200
    return {"status": "ok👌"}
