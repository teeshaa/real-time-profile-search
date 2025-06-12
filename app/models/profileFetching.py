
from pydantic import BaseModel


class ProfileFetchingRequest(BaseModel):
    query: str
