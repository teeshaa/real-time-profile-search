from fastapi import APIRouter, Depends

from app.controllers.profileFetching import ProfileFetchingController
from app.models.profileFetching import ProfileFetchingRequest

router = APIRouter()


@router.post("/profile/fetch")
async def fetch_profile(
    profile_request: ProfileFetchingRequest,
    controller: ProfileFetchingController = Depends(ProfileFetchingController),
):
    return await controller.search_profiles(profile_request)
