"""models for fastapi app.
10.11.2023 https://github.com/kissmeandillkissumylove"""

from sqlalchemy import MetaData, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy import Table, Column, JSON, Boolean
from datetime import datetime

metadata = MetaData()  # create a variable with metadata

role = Table(  # table for roles
    "role",  # name
    metadata,
    Column("id", Integer, primary_key=True),  # user id. unique
    Column("name", String, nullable=False),  # name. cant be empty
    Column("permissions", JSON),  # user permissions
)

user = Table(  # table for user info
    "user",  # name
    metadata,
    Column("id", Integer, primary_key=True),  # id. unique
    Column("email", String, nullable=False),  # email. cant be empty
    Column("username", String, nullable=False),  # name. cant be empty
    Column("hashed_password", String, nullable=False),  # password. no empty
    # when user created account
    Column("registered_at", TIMESTAMP, default=datetime.utcnow),
    Column("role_id", Integer, ForeignKey("role.c.id")),  # user role
    Column("is_active", Boolean, default=True, nullable=False),
    Column("is_superuser", Boolean, default=False, nullable=False),
    Column("is_verified", Boolean, default=False, nullable=False),
)

# we can create engine with following code: ->
"""engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)"""
# but we won’t do this, because... we will use migrations
