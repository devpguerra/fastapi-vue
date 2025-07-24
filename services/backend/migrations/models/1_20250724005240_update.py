from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" ADD "email" VARCHAR(255)  UNIQUE;
        ALTER TABLE "users" ADD "is_oauth" BOOL NOT NULL  DEFAULT False;
        CREATE UNIQUE INDEX "uid_users_email_133a6f" ON "users" ("email");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX "idx_users_email_133a6f";
        ALTER TABLE "users" DROP COLUMN "email";
        ALTER TABLE "users" DROP COLUMN "is_oauth";"""
