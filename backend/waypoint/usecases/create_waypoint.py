import uuid
from fastapi import HTTPException, status
from waypoint.repository.waypoint import WaypointRepository
from waypoint.domain.waypoint import Waypoint, CreateWaypoint


async def create_waypoint_usecase(
    repository: WaypointRepository, create_data: CreateWaypoint
):
    try:
        waypoint = Waypoint(
            id=uuid.uuid4(),
            longitude=create_data.longitude,
            latitude=create_data.latitude,
        )

        await repository.save(waypoint)

        return waypoint

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the waypoint",
        )
