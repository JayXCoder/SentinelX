import os

os.environ.setdefault("DATABASE_URL", "sqlite:///./.pytest.db")
os.environ.setdefault("REDIS_URL", "redis://localhost:4637/0")
