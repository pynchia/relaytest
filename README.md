
# Relaytest

A test

## Deliverables

The application is available on Render.com at the address:

https://relaytest.onrender.com/docs

Please be aware the free service shuts down the application when unused.

The code is available on Github at:

https://github.com/pynchia/relaytest



## Notes

The following notes have a fundamental reason: lack of time.


- No authantication is provided. The description of the test does not specify who would be the client calling the earnings endpoint: I assumed it would be an internal system, which would pass the weekly activity log in an anonymous form, without any link to any user. I would add a token-based authentication (JWT) or at least a predefined secret token value shared with the client service and stored in an env var/docker secret.

- As the earnings EP must be stateless, not data is kept in the DB after each request.

- In order to prevent race conditions the drops are marked with an id that identifies the request.

- At present the backend is a silyl mix of async EPs that rely on a sync DB session. Of course it makes little sense and the session should be async as well.

- The program only calculates the earnings for an activity log of a rate_card of type `bronze`. i.e. `POST /earnings/bronze_tier`

- The other rate cards are not implemented, although present in comments to show how composition is used within the `CRUDEarnings` class  (I calle dit CRUD because of habit and it gives an idea for a class that actually performs operations on the entity).

- The calculated earnings are populated partially, i.e. the field `hours_worked` is not calculated. All other attributes are calculated (i.e. `line_items`, `minimum_earnings`, `final_earnings`)

- The automated unit tests include one tests only.

- The application is not containerised, no Dockerfile, although it would be rather simple to add.

- Also CI github actions that run the tests could be added easily. And/or to a dockerfile.
