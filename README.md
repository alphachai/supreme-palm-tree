# supreme-palm-tree

A demo API built with Python 3.8 and FastAPI.


#### Getting Started
You'll need to have `docker` and `docker-compose` installed, but that's it! Run `make up` to start the service.

#### Legend

☑️ - planned

🟢 - completed

🟡 - work-in-progress

❌ - incomplete



## API

Full documentation and interactive examples is generated via [Swagger](https://swagger.io/tools/swagger-ui/). View at `http://127.0.0.1:8000/docs`.

| Endpoint | Description | GET | POST | PUT | DELETE |
| - | - | - | - | - | - |
| / | Health check | ☑️🟢 |  |  |  |
| /users/ | list/create users | ☑️🟢 | ☑️🟢 |  |  |
| /users/{id}/ | describe/update user | ☑️🟢 |  | ☑️🟢 |  |
| /orders/ | list/create orders | ☑️🟢 | ☑️🟢 |  |  |
| /orders/{id}/ | describe/update order | ☑️🟢 |  | ☑️🟢 | ☑️🟢 |
| /orders/status/ | list order statuses | ☑️🟢 |  |  |  |
| /pizzas/ | list/create pizzas | ☑️🟢 | ☑️🟢 |  |  |
| /pizzas/{id}/ | describe pizza | ☑️🟢 |  | ☑️❌ |  |
| /pizzas/toppings/ | list/create toppings | ☑️🟢 | ☑️❌ |  |  |
| /pizzas/toppings/{id}/ | describe/update topping | ☑️❌ |  | ☑️❌ |  |



## ORM

This project uses sqlalchemy to manage postgresql models and alembic to generate migrations based on those models. Models are found in `app/models.py`.

#### Models

* User 🟢
* Order 🟢
* OrderStatus ❌ (used enum instead, `schemas.Status`)
* OrderStatusUpdate ❌
* Pizza 🟢
* Topping ❌ (used enum instead, `schemas.Topping`)
* PizzaTopping ❌


#### Migrations

Migrations are applied in the docker entrypoint (`docker/entrypoint.sh`) with `alembic upgrade head`.

After changes to the models, generate new migrations with the following process.

*  Start the service.
  `make up`
* Open a shell within the container.
  `make exec`
* Generate migrations - these will be reflected in your project checkout, since the directory is mounted as a volume by the container.
  `alembic revision --autogenerate -m "change desc"`

*for more info, please see the [Alembic docs](https://alembic.sqlalchemy.org/en/latest/autogenerate.html)*



## Code Quality

Linted with `flake8` (style and potential bugs) and `isort` (import sorting).

Formatted automatically with `black` (style), `autoflake` (unused imports), and `isort`.




## Testing

None yet.

* Tests should be deterministic and repeatable.
* Tests should always setup and teardown.
* Tests should be structured to allow parallelization without clashing. (namespace mocks/stubs)
* I prefer test coverage > 90%.



# Notes

* User *should ideally* validate email and accept a password to hash, if it is going to be the source of truth for identity (IDP). (This is the reason why I used separate "base" and "creation" schemas for each model.) However, no API should provide it's own IDP. The only use for creating users should be session management, and it's use should (1) probably not be behind this API, but if it must, (2) it should be restricted by token-based authentication.
* It may make sense to roll up API requests into a single call with a new, non-restful endpoint, or via a graphql / gRPC interface. Although, for a pizza shop, the additional overhead for all the requests may be rather inconsequential behind a CDN since the components of a pizza won't change often enough.