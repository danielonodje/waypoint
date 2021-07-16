import uuid
import pytest
from pydantic import ValidationError
from waypoint.domain.waypoint import Waypoint


def test_domain_model_init():
    id = uuid.uuid4()
    waypoint = Waypoint(id=id, longitude=76.340034, latitude=89.934456)

    assert waypoint.id == id
    assert waypoint.longitude == 76.340034
    assert waypoint.latitude == 89.934456


def test_init_with_invalid_id():
    with pytest.raises(ValidationError) as validation_error:
        Waypoint(id=4, longitude=76.565745, latitude=-80.345444)

    assert "value is not a valid uuid" in str(validation_error.value)


def test_init_with_invalid_latitude_type():
    with pytest.raises(ValidationError) as validation_error:
        Waypoint(id=uuid.uuid4(), longitude=12.75434, latitude="7E")

    assert "value is not a valid float" in str(validation_error.value)


def test_init_with_invalid_longitude_type():
    with pytest.raises(ValidationError) as validation_error:
        Waypoint(id=uuid.uuid4(), longitude="AS", latitude=56.893434)

    assert "value is not a valid float" in str(validation_error.value)


def test_init_with_invalid_latitude():
    with pytest.raises(ValidationError) as validation_error:
        Waypoint(id=uuid.uuid4(), longitude=34.89054, latitude=-91.04523)

    assert "Latitude must be between -90 and 90" in str(validation_error.value)


def test_init_with_invalid_longitude():
    with pytest.raises(ValidationError) as validation_error:
        Waypoint(id=uuid.uuid4(), longitude=276.04323, latitude=-61.787645)

    assert "Longitude must be between -180 and 180" in str(validation_error.value)


def test_init_from_dict():
    waypoint_dict = {"id": uuid.uuid4(), "longitude": 171.57734, "latitude": 56.34983}

    waypoint = Waypoint.from_dict(waypoint_dict)

    assert waypoint.id == waypoint_dict["id"]
    assert waypoint.latitude == waypoint_dict["latitude"]
    assert waypoint.longitude == waypoint_dict["longitude"]


def test_convert_to_dict():
    waypoint = Waypoint(id=uuid.uuid4(), longitude=176.33424, latitude=89.12634)

    waypoint_dict = waypoint.to_dict()
    assert isinstance(waypoint_dict, dict)

    assert waypoint.to_dict() == waypoint_dict


def test_entity_equality():
    waypoint_dict = {"id": uuid.uuid4(), "longitude": 171.02, "latitude": 56.43}

    waypoint1 = Waypoint.from_dict(waypoint_dict)
    waypoint2 = Waypoint.from_dict(waypoint_dict)

    assert waypoint1 == waypoint2
