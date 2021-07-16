# Waypoint Web Service

## API

Simple FastAPI python web service. To make things easier we're using sqlite as a db, this sqlite db will get created inside the container so when the container is destroyed the db is automatically disposed.

Tests are in the `backend/tests` folder, the majority of application logic is in the `backend/waypoint` folder, and the FastAPI app is defined in `backend/main.py`

## Frontend

Vanilla JS Webpage. Uses [Leaflet JS](https://leafletjs.com/) for the map

Clicking on the map will fill the input box with a Latitude and Longitude value. Clicking `Add Waypoint` will call the Flask API and store it in the db.

On page load / reload, the webpage will fetch the available waypoints from the backend and add them as markers on the map.

I've added a default map marker as a mystery location :)

The frontend is a single `index.html` file in the `/backend/static` directory

### Testing

We're using [poetry](https://python-poetry.org/docs/) for package management and general venv wrangling. Running `poetry run pytest` in the backend directory will the tests

### Running

`docker-compose up` will start the app. It runs at `http://0.0.0.0:8080`. This loads the map directly.
