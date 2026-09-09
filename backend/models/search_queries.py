from pydantic import BaseModel


class SearchQueries(BaseModel):
    queries: list[str]