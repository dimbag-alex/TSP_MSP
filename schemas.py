from pydantic import BaseModel


class CityBase(BaseModel):
    name: str
    latitude: float
    longitude: float


class CityCreate(CityBase):
    pass


class City(CityBase):
    id: int

    class Config:
        # orm_mode = True
        from_attributes = True
