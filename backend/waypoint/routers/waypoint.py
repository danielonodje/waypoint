from fastapi import APIRouter, Depends

from waypoint.repository import WaypointRepository, get_waypoint_repository
from waypoint.usecases import (
    create_waypoint_usecase,
    list_waypoints_usecase,
    CreateWaypoint,
)
from waypoint.domain import Waypoint

router = APIRouter()


@router.post("", response_model=Waypoint)
async def create_waypoint(
    create_data: CreateWaypoint,
    repository: WaypointRepository = Depends(get_waypoint_repository),
):
    response = await create_waypoint_usecase(repository, create_data)
    return response


@router.get(
    "",
)
async def list_waypoints(
    repository: WaypointRepository = Depends(get_waypoint_repository),
):
    response = await list_waypoints_usecase(repository)
    return response
