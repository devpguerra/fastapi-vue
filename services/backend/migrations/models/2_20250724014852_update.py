from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" ALTER COLUMN "username" TYPE VARCHAR(60) USING "username"::VARCHAR(60);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" ALTER COLUMN "username" TYPE VARCHAR(20) USING "username"::VARCHAR(20);"""
