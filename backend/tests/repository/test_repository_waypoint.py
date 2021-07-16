import pytest
import uuid
from databases import Database
from sqlalchemy import create_engine, MetaData

from waypoint.repository.waypoint import WaypointRepository
from waypoint.domain.waypoint import Waypoint


@pytest.fixture
async def repository():
    test_connection_string = "sqlite:///test_memory"

    metadata = MetaData()
    table = WaypointRepository.get_table_definition(metadata)

    engine = create_engine(test_connection_string, echo=True)

    metadata.create_all(engine)

    database = Database(test_connection_string, force_rollback=True)

    async with WaypointRepository.get_instance(database, table) as repository:
        yield repository
        await database.execute(query="DELETE FROM waypoints")


@pytest.mark.asyncio
async def test_create_waypoint(repository):
    waypoint = Waypoint(id=uuid.uuid4(), longitude=76.4654534, latitude=89.231767)

    await repository.save(waypoint)

    waypoints = await repository.list()

    assert len(waypoints) == 1
    assert waypoints[0].id == waypoint.id
    assert waypoints[0].longitude == waypoint.longitude
    assert waypoints[0].latitude == waypoint.latitude


@pytest.mark.asyncio
async def test_get_waypoint(repository):
    waypoint = Waypoint(id=uuid.uuid4(), longitude=76.4654534, latitude=89.231767)

    await repository.save(waypoint)

    created_waypoint = await repository.get(waypoint.id)

    assert created_waypoint.id == waypoint.id
    assert created_waypoint.longitude == waypoint.longitude
    assert created_waypoint.latitude == waypoint.latitude


@pytest.mark.asyncio
async def test_list_waypoints(repository):
    waypoint1 = Waypoint(id=uuid.uuid4(), longitude=76.4654534, latitude=89.231767)
    waypoint2 = Waypoint(id=uuid.uuid4(), longitude=76.4654534, latitude=89.231767)
    waypoint3 = Waypoint(id=uuid.uuid4(), longitude=76.4654534, latitude=89.231767)

    await repository.save(waypoint1)
    await repository.save(waypoint2)
    await repository.save(waypoint3)

    waypoints_list = [waypoint1, waypoint2, waypoint3]

    waypoints = await repository.list()

    assert len(waypoints) == len(waypoints_list)
    assert waypoints_list == waypoints


@pytest.mark.asyncio
async def test_delete_waypoint(repository):
    waypoint = Waypoint(id=uuid.uuid4(), longitude=76.4654534, latitude=89.231767)

    await repository.save(waypoint)

    created_waypoint = await repository.get(waypoint.id)

    assert created_waypoint == waypoint

    await repository.delete(waypoint.id)

    deleted_waypoint = await repository.get(waypoint.id)

    assert deleted_waypoint is None
