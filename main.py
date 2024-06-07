from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends
from database import get_db
from schemas import CityCreate, City

from crud import get_cities, create_city

from tsp import mst_tsp

DATABASE_URL = "postgresql://postgres:postgres@localhost/courseworkv2"

Base = declarative_base()

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@app.get("/cities/", response_model=list[City])
def read_cities(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_cities(db, skip=skip, limit=limit)


@app.post("/cities/", response_model=City)
def create_city_view(city: CityCreate, db: Session = Depends(get_db)):
    return create_city(db=db, city=city)


@app.get("/solve-tsp/")
def solve_tsp_route(db: Session = Depends(get_db)):
    all_cities = get_cities(db=db)
    cities_coords = [((city.latitude), (city.longitude)) for city in all_cities]
    cities_names = dict()
    for city in all_cities:
        cities_names[(city.latitude, city.longitude)] = city.name

    order_of_travelling_coords, total_distance, order_of_travelling_names, ans = mst_tsp(cities_coords, cities_names)

    response_data = {
        "order_of_travelling_coords": order_of_travelling_coords,
        "total_distance": total_distance,
        "order_of_travelling_names": order_of_travelling_names,
        "ans": ans
    }
    return JSONResponse(content=response_data)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
