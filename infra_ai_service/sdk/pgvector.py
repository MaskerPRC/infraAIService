from psycopg_pool import AsyncConnectionPool
from sentence_transformers import SentenceTransformer

from infra_ai_service.common.utils import setup_database
from infra_ai_service.config.config import settings

# 初始化模型
model = None
# 创建连接池（暂时不初始化）
pool = None


async def setup_model_and_pool():
    global model, pool
    # 初始化模型
    model = SentenceTransformer(settings.MODEL_NAME)
    # 创建异步连接池
    conn_str = (
        f"dbname={settings.DB_NAME} "
        f"user={settings.DB_USER} "
        f"password={settings.DB_PASSWORD} "
        f"host={settings.DB_HOST} "
        f"port={settings.DB_PORT}"
    )
    pool = AsyncConnectionPool(
        conn_str,
        min_size=4,
        max_size=10,
        open=True,
        max_idle=30 * 60.0,  # 允许空闲时间为30分钟
        reconnect_timeout=5 * 60.0,  # 5分钟后重试连接
    )

    # 设置数据库
    await setup_database(pool)
