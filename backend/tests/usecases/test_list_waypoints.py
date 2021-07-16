import pytest
import uuid
from unittest import mock
from asyncio import Future
from fastapi import HTTPException

from waypoint.domain import Waypoint
from waypoint.usecases import list_waypoints_usecase


@pytest.mark.asyncio
async def test_list_waypoints():
    waypoints_list = [
        Waypoint(id=uuid.uuid4(), longitude=76.46, latitude=89.23),
        Waypoint(id=uuid.uuid4(), longitude=76.46, latitude=89.23),
        Waypoint(id=uuid.uuid4(), longitude=76.46, latitude=89.23),
    ]

    repository = mock.Mock()
    mock_response = Future()

    mock_response.set_result(waypoints_list)
    repository.list.return_value = mock_response

    response = await list_waypoints_usecase(repository)

    assert response == waypoints_list


@pytest.mark.asyncio
async def test_list_waypoints_error():
    repository = mock.Mock()
    repository.list.side_effect = mock.Mock(side_effect=RuntimeError())

    with pytest.raises(HTTPException) as e:
        await list_waypoints_usecase(repository)
        assert isinstance(e, HTTPException) is True
