import uuid
from pydantic import BaseModel, validator


class CreateWaypoint(BaseModel):
    longitude: float
    latitude: float

    @validator("longitude")
    def validate_longitude(cls, v):
        """
        Check that the supplied longitude field is valid
        Valid longitudes must be between -180 and 180 degrees
        """
        if not abs(v) <= 180:
            raise ValueError("Longitude must be between -180 and 180")
        return v

    @validator("latitude")
    def validate_latitude(cls, v):
        """
        Check that the supplied latitude field is valid
        Valid latitudes must be between -90 and 90 degrees
        """
        if not abs(v) <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        return v


class Waypoint(CreateWaypoint):
    id: uuid.UUID

    @classmethod
    def from_dict(self, d):
        """
        create a new Waypoint from a given dict
        """
        return self(**d)

    def to_dict(self):
        """
        transform a Waypoint object into a dict representation
        """
        return {
            "id": str(self.id),
            "latitude": self.latitude,
            "longitude": self.longitude,
        }
