from tortoise import fields, models
from typing import Optional


class Users(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=60, unique=True)
    email = fields.CharField(255, unique=True)
    auth_provider = fields.CharField(max_length=50, null=True)
    full_name = fields.CharField(max_length=50, null=True)
    password = fields.CharField(max_length=128, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
    is_confirmed = fields.BooleanField(default=False)
    confirmation_token = fields.CharField(max_length=255, null=True)   


class Notes(models.Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=225)
    content = fields.TextField()
    author = fields.ForeignKeyField("models.Users", related_name="note")
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}, {self.author_id} on {self.created_at}"