
# Relaytest

A test

## Deliverables

The application is available on Render.com at the address:

https://relaytest.onrender.com/docs

Please be aware the free service shuts down the application when unused.

The code is available on Github at:

https://github.com/pynchia/relaytest


## Dependencies / initial setup

Dependencies can be installed with the commands

`python3 -m venv .venv`

`. .venv/bin/activate`

`pip install pdm`

`pdm install`


## Tests

the unit tests can be launched in the root directory of the project by:

- activating the virtual environment and running `pytest`

or

- by running `pdm run pytest`

## Run the application locally

the application can be run locally with the command

`uvicorn app.main:app` with the python venv activated

or

`pdm run uvicorn app.main:app` without activating the python venv


## Notes

The following notes have a fundamental reason: lack of time.


- No authentication is provided. The description of the test does not specify who would be the client calling the earnings endpoint: I assumed it would be an internal system, which would pass the weekly activity log in an anonymous form, without any link to any user. I would add a token-based authentication (JWT) or at least a predefined secret token value shared with the client service and stored in an env var/docker secret.

- As the earnings EP must be stateless, not data is kept in the DB after each request.

- In order to prevent race conditions the drops are marked with an id that identifies the request.

- At present the backend is a mix of async EPs that rely on a sync DB session. Of course it makes little sense and the session should be async as well. I haven't tried on sqlite yet.

- The program only calculates the earnings for an activity log of a rate_card of type `bronze`. i.e. `POST /earnings/bronze_tier`

- The other rate cards are not implemented, although present in comments to show how composition is used within the `CRUDEarnings` class  (I called it CRUD because of habit and it gives an idea for a class that actually performs operations on the entity).

- The calculated earnings are populated partially, i.e. the field `hours_worked` is not calculated. All other attributes are calculated (i.e. `line_items`, `minimum_earnings`, `final_earnings`)

- The automated unit tests include one tests only.

- The application is not containerised, no Dockerfile, although it would be rather simple to add.

- The code gets deployed to Render.com automatically upon every push to the `main` branch.

- Also CI github actions that run the tests and guard deployment could be added easily. And/or to a dockerfile, depending on how one wants to play it


