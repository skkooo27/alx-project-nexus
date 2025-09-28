# E-Commerce Backend

A scalable E-commerce Backend System built with Django, PostgreSQL, and JWT Authentication.
This project simulates a real-world backend engineering environment, focusing on database design, API development, performance optimization, and secure authentication.

## Project Overview
This backend manages products, categories, and users** for an e-commerce platform.
It includes CRUD APIs, filtering, sorting, pagination, and JWT authentication, with APIs documented via Swagger/Postman.

## Features
* User Authentication.
  * Register, login, JWT-based authentication.
  * Secure password hashing.

* Product & Category Management
  * CRUD APIs for products and categories.
  * Filtering (by category), sorting (by price), and pagination.

* API Documentation.
  * Swagger / Postman collection for API testing.

* Database Optimization.
  * PostgreSQL schema with indexes for faster queries.


## 🛠 Tech Stack
* Backend Framework: Django REST Framework
* Database: PostgreSQL
* Authentication: JWT (djangorestframework-simplejwt)
* Documentation: Swagger / drf-yasg or Postman
* Containerization: Docker + Docker Compose
* Deployment: Railway.


## System Architecture

[ Client (Frontend) ]
        |
     REST API
        |
[ Django REST Framework ]
        |
[ PostgreSQL Database ]


## Setup & Installation

1. Clone repository
2. Create virtual environment & install dependencies
3. Configure environment variables
4. Run migrations
5. Start server


## API Endpoints
1.  Authentication
* `POST /api/auth/register/` → Register new user
* `POST /api/auth/login/` → Login and get JWT

2. Products
* `GET /api/products/` → List products (supports filtering, sorting, pagination)
* `POST /api/products/` → Create product (Admin only)
* `GET /api/products/{id}/` → Get single product
* `PUT /api/products/{id}/` → Update product
* `DELETE /api/products/{id}/` → Delete product

3. Categories

* `GET /api/categories/` → List categories
* `POST /api/categories/` → Create category
* `GET /api/categories/{id}/` → Get category
* `PUT /api/categories/{id}/` → Update category
* `DELETE /api/categories/{id}/` → Delete category

4. Authentication

This project uses JWT Authentication:

* Obtain access and refresh tokens via `/api/auth/login/`.
* Include access token in request headers:

Authorization: Bearer <access_token>


## 📑 API Documentation

Swagger UI available at:
/swagger/


## Performance Optimization

* Added indexes on `category_id` and `price` fields.
* Used queryset prefetch/select_related to minimize queries.
* Implemented paginated responses for large datasets.


## Future Improvements
* Add payment gateway integration (Stripe, PayPal).
