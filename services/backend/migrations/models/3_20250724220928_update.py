from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" ADD "auth_provider" VARCHAR(50);
        ALTER TABLE "users" DROP COLUMN "is_oauth";
        ALTER TABLE "users" ALTER COLUMN "email" SET NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" ADD "is_oauth" BOOL NOT NULL  DEFAULT False;
        ALTER TABLE "users" DROP COLUMN "auth_provider";
        ALTER TABLE "users" ALTER COLUMN "email" DROP NOT NULL;"""
