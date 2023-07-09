import asyncio
import logging

from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from app.db import base
from app.db.init_db import init_db
from app.db.session import async_session, engine_async

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
async def init() -> None:
    try:
        async with engine_async.begin() as conn:
            logger.info("DROP DATABASE")
            await conn.run_sync(base.Base.metadata.drop_all)  # type: ignore
            logger.info("CREATE DATABASE")
            await conn.run_sync(base.Base.metadata.create_all)  # type: ignore
        async with async_session() as db:
            await init_db(db=db)
            await db.execute("SELECT 1")  # type: ignore
        logger.info("DATABASE DONE")
    except Exception as e:
        logger.error(e)
        raise e


async def main() -> None:
    logger.info("Initializing service")
    await init()
    logger.info("Service finished initializing")


if __name__ == "__main__":
    asyncio.run(main())
