from typing import AsyncGenerator

from fastapi.responses import StreamingResponse

from app.models.profileFetching import ProfileFetchingRequest
from app.usecases.profileFetching import ProfileFetchingUsecase


class ProfileFetchingController:
    def __init__(self):
        self.usecase = ProfileFetchingUsecase()

    async def search_profiles(self, request: ProfileFetchingRequest) -> StreamingResponse:
        async def generate_response() -> AsyncGenerator[str, None]:
            try:
                async for chunk in self.usecase.search_profiles_streaming(request.query):
                    yield f"{chunk}\n"
                yield "{\"type\": \"data\", \"data\": \"[DONE]\"}\n"
            except Exception as e:
                yield "{\"type\": \"error\", \"data\": \"Stream processing failed\"}\n"

        return StreamingResponse(
            generate_response(),
            media_type="application/json",
            headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
        )
