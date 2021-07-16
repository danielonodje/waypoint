from fastapi import HTTPException, status
from waypoint.repository import WaypointRepository


async def list_waypoints_usecase(repository: WaypointRepository):
    try:
        waypoints = await repository.list()

        return waypoints
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the waypoint",
        )
