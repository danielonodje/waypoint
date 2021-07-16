import pytest
from asyncio import Future
from unittest import mock
from fastapi import HTTPException

from waypoint.usecases import create_waypoint_usecase, CreateWaypoint


def wrap_in_future(value):
    response = Future()
    response.set_result(value)

    return response


@pytest.mark.asyncio
async def test_create_waypoint():
    repository = mock.Mock()
    repository.save.side_effect = wrap_in_future

    create_data: CreateWaypoint = CreateWaypoint(longitude=-12.23233, latitude=23.65677)
    response = await create_waypoint_usecase(repository, create_data)

    assert response.id is not None
    assert response.longitude == create_data.longitude
    assert response.latitude == create_data.latitude


@pytest.mark.asyncio
async def test_create_waypoint_system_error():
    repository = mock.Mock()
    repository.save.side_effect = mock.Mock(side_effect=RuntimeError())

    create_data = {"longitude": -12.23233, "latitude": 23.65677}

    with pytest.raises(HTTPException) as e:
        await create_waypoint_usecase(repository, create_data)
        assert isinstance(e, HTTPException) is True
