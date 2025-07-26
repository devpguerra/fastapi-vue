from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" ADD "is_confirmed" BOOL NOT NULL  DEFAULT False;
        ALTER TABLE "users" ADD "confirmation_token" VARCHAR(255);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" DROP COLUMN "is_confirmed";
        ALTER TABLE "users" DROP COLUMN "confirmation_token";"""
