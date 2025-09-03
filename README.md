# My FastAPI App

A modern, asynchronous REST API built with FastAPI, featuring user authentication, post management, and a voting system.

## Features

- **User Authentication**: JWT-based authentication system
- **Post Management**: Full CRUD operations for posts with ownership
- **Voting System**: Users can vote on posts
- **Search & Pagination**: Search posts by title with pagination support
- **Async Database**: PostgreSQL with async SQLAlchemy and SQLModel
- **Database Migrations**: Alembic for schema management
- **CORS Support**: Configured for cross-origin requests
- **Input Validation**: Pydantic models for robust data validation

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy with SQLModel
- **Migrations**: Alembic
- **Authentication**: JWT (JSON Web Tokens)
- **Password Hashing**: bcrypt
- **Package Management**: uv
- **ASGI Server**: Uvicorn

## Prerequisites

- Python 3.13+
- PostgreSQL database
- uv package manager

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/dumnevijay/my-fastapi-app.git
   cd my-fastapi-app
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   ```

## Environment Setup

Create a `.env` file in the root directory with the following variables:

```env
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_PASSWORD=your_password
DATABASE_NAME=your_database_name
DATABASE_USERNAME=your_username
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Database Setup

1. **Create PostgreSQL database**:
   ```sql
   CREATE DATABASE your_database_name;
   ```

2. **Run database migrations**:
   ```bash
   uv run alembic upgrade head
   ```

## Running the Application

Start the development server:

```bash
uv run uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### API Documentation

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## API Endpoints

### Authentication
- `POST /login` - User login
- `POST /users/` - User registration
- `GET /users/{id}` - Get user by ID

### Posts
- `GET /posts/` - Get all posts (with search, pagination)
- `POST /posts/` - Create a new post
- `GET /posts/{id}` - Get post by ID
- `PUT /posts/{id}` - Update post
- `DELETE /posts/{id}` - Delete post

### Voting
- `POST /vote/` - Vote on a post

## Testing

Run tests with pytest:

```bash
uv run pytest
```

## Project Structure

```
my-fastapi-app/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application
│   ├── config.py        # Configuration settings
│   ├── database.py      # Database connection
│   ├── models.py        # SQLModel database models
│   ├── schemes.py       # Pydantic schemas
│   ├── oauth2.py        # JWT authentication
│   ├── utils.py         # Utility functions
│   └── routers/
│       ├── auth.py      # Authentication routes
│       ├── post.py      # Post management routes
│       ├── user.py      # User management routes
│       └── vote.py      # Voting routes
├── tests/
│   ├── __init__.py
│   └── test_users.py
├── alembic/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
├── pyproject.toml
├── requirements.txt
├── uv.lock
├── alembic.ini
└── README.md
```

## Database Models

### User
- `id`: Primary key
- `email`: Unique email address
- `password`: Hashed password
- `created_at`: Timestamp

### Post
- `id`: Primary key
- `title`: Post title
- `content`: Post content
- `is_published`: Publication status
- `created_at`: Timestamp
- `owner_id`: Foreign key to User

### Vote
- `user_id`: Foreign key to User (composite primary key)
- `post_id`: Foreign key to Post (composite primary key)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built following FastAPI best practices
- Inspired by modern REST API patterns
- Uses SQLModel for type-safe database operations</content>
<parameter name="filePath">d:\Personal Projects\fastAPI\README.md
