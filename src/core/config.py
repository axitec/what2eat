from typing import Literal
from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用配置（支持PostgreSQL和SQLite, 含连接池设置）"""

    app_name: str = "What to eat"
    debug: bool = False

    # 数据库类型
    db_type: Literal["postgresql", "sqlite"] = "sqlite"

    # PostgreSQL配置
    db_host: str = "lacalhost"
    db_port: int = 5432
    db_user: str = "postgres"
    db_password: str = "postgres"
    db_name: str = "what2eat"

    # 连接池配置（仅PostgresSQL 有效）
    # ---必选参数：中等并发常用---
    pool_size: int = 20  # 连接池基础大小，低- 高+
    max_overflow: int = 10  # 超出pool_size的最大连接数，低- 高+
    pool_timeout: int = 30  # 获取连接超时时间（秒），低- 高+
    pool_pre_ping: bool = True  # 取连接前是否检查可用性，低:false, 高:true

    # ---可选调优参数（高级场景）---
    pool_recycle: int = 3600  # 连接最大存活时间（秒），低- 高+，避免长连接被数据库踢掉
    pool_use_lifo: bool = (
        False  # 连接池获取连接顺序，低:false(FIFO), 高:true(LIFO) 可提高高并发的命中率
    )
    echo: bool = False  # 是否打印SQL日志，低:false, 高:true

    # SQLite配置
    sqlite_db_path: str = "data/what2eat.sqlite3"

    @computed_field
    @property
    def db_url(self) -> str:
        if self.db_type == "postgresql":
            return (
                f"postgresql+asyncpg://{self.db_user}:{self.db_password}"
                f"@{self.db_host}:{self.db_port}/{self.db_name}"
            )
        elif self.db_type == "sqlite":
            return f"sqlite+aiosqlite:///{self.sqlite_db_path}"
        else:
            raise ValueError(f"Unsupported db_type: {self.db_type}")

    @computed_field
    @property
    def engine_options(self) -> dict:
        """统一封装 engine options，供create_async_engine使用"""
        if self.db_type == "postgresql":
            return {
                "pool_size": self.pool_size,
                "max_overflow": self.max_overflow,
                "pool_timeout": self.pool_timeout,
                "pool_recycle": self.pool_recycle,
                "pool_pre_ping": self.pool_pre_ping,
                "pool_use_lifo": self.pool_use_lifo,
                "echo": self.echo,
            }
        # sqlite 不支持pool设置，返回最小参数
        return {"echo": self.echo}

    # JWT 配置
    jwt_secret: str = "的萨芬立刻就发送大量浪费"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False
    )


settings = Settings()
