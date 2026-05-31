from typing import Annotated

from fastapi import Query

MAX_PAGE_LIMIT = 200
DEFAULT_PAGE_LIMIT = 50

LimitQuery = Annotated[int, Query(ge=1, le=MAX_PAGE_LIMIT)]
SkipQuery = Annotated[int, Query(ge=0, le=10_000)]
