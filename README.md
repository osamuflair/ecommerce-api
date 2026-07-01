# ecommerce-api

A RESTful e-commerce API built with FastAPI and PostgreSQL.

## Tech Stack
- FastAPI
- PostgreSQL
- SQLAlchemy 2.0
- Alembic
- Pydantic v2
- JWT Authentication (pwdlib/argon2)

## Features
- User registration and authentication with JWT
- Role-based access control (Customer, Staff, Admin)
- Product and category management (admin only)
- Shopping cart with stock validation
- Wishlist management
- Order checkout with address selection
- Order status management (staff only)
- Customer order cancellation with automatic stock restoration

## API Endpoints
All endpoints are prefixed with `/api/v1`

- `POST /users/register` — Register a new user
- `POST /users/login` — Login and receive JWT token
- `GET/PUT/DELETE /users/me` — Manage your own account
- `GET/POST/PUT/DELETE /addresses` — Manage delivery addresses
- `GET/POST/PUT/DELETE /cart/items` — Manage shopping cart
- `GET/POST/DELETE /wishlist/items` — Manage wishlist
- `POST /orders/checkout` — Place an order
- `GET /orders` — View your orders
- `GET /categories` — Browse categories
- `GET /products` — Browse products
