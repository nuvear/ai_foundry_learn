---
## HIGH-LEVEL DESIGN (HLD)

**Project:** Todo List REST API with JWT Authentication  
**Prepared by:** Architect Agent  
**Version:** 1.0  

### 1. Technology Stack
| Layer       | Technology         | Justification                                                                 |
| :---------- | :----------------- | :--------------------------------------------------------------------------- |
| Backend     | FastAPI (Python)   | Lightweight, fast, and built-in support for REST APIs and JWT authentication. |
| Database    | PostgreSQL         | Relational database with strong support for scalability and ACID compliance. |
| Auth        | JWT (PyJWT)        | Industry-standard token-based authentication for stateless APIs.             |
| Hosting     | Docker + AWS ECS   | Docker ensures portability; AWS ECS simplifies container orchestration.      |
| CI/CD       | GitHub Actions     | Streamlined CI/CD pipelines with native GitHub integration.                  |

### 2. System Architecture
The system consists of the following components:
```
[Client] → [FastAPI Backend] → [PostgreSQL Database]
                       ↓
                  [JWT Auth]
```

- **Client:** External applications or developers interacting with the API.  
- **FastAPI Backend:** Handles all API requests, including authentication and CRUD operations.  
- **PostgreSQL Database:** Stores user information and tasks securely.  
- **JWT Auth:** Provides token-based authentication and authorization for secure API access.  

### 3. Data Models

#### **Entity: User**
| Field        | Type       | Constraints     | Description                     |
| :----------- | :--------- | :-------------- | :------------------------------ |
| id           | UUID       | PK, auto        | Unique identifier for the user. |
| username     | String     | Unique, not null | User's chosen display name.     |
| email        | String     | Unique, not null | User's email address.           |
| password_hash| String     | Not null        | Hashed password for security.   |
| created_at   | Timestamp  | auto            | Account creation timestamp.     |

#### **Entity: Task**
| Field        | Type       | Constraints     | Description                     |
| :----------- | :--------- | :-------------- | :------------------------------ |
| id           | UUID       | PK, auto        | Unique identifier for the task. |
| user_id      | UUID       | FK, not null    | Reference to the owning user.   |
| title        | String     | Not null        | Title of the task.              |
| description  | Text       | Optional        | Detailed description of the task.|
| status       | String     | Enum (Pending, Completed) | Current status of the task. |
| created_at   | Timestamp  | auto            | Task creation timestamp.        |
| updated_at   | Timestamp  | auto            | Last update timestamp.          |

### 4. API Contracts

#### **POST /register**
- **Purpose:** Register a new user.  
- **Auth:** Public.  
- **Request Body:**  
```json
{
  "username": "string",
  "email": "string",
  "password": "string"
}
```
- **Response 201:**  
```json
{
  "id": "uuid",
  "username": "string",
  "email": "string",
  "created_at": "timestamp"
}
```
- **Response Errors:**  
  - 409 Conflict: Email already in use.  

---

#### **POST /login**
- **Purpose:** Authenticate user and issue JWT token.  
- **Auth:** Public.  
- **Request Body:**  
```json
{
  "email": "string",
  "password": "string"
}
```
- **Response 200:**  
```json
{
  "access_token": "string",
  "expires_in": 86400
}
```
- **Response Errors:**  
  - 401 Unauthorized: Invalid credentials.  

---

#### **POST /tasks**
- **Purpose:** Create a new task.  
- **Auth:** JWT required.  
- **Request Body:**  
```json
{
  "title": "string",
  "description": "string",
  "status": "string"
}
```
- **Response 201:**  
```json
{
  "id": "uuid",
  "title": "string",
  "description": "string",
  "status": "string",
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```
- **Response Errors:**  
  - 401 Unauthorized: Invalid or missing JWT token.  

---

#### **GET /tasks**
- **Purpose:** Retrieve all tasks for the authenticated user.  
- **Auth:** JWT required.  
- **Request Body:** None.  
- **Response 200:**  
```json
[
  {
    "id": "uuid",
    "title": "string",
    "description": "string",
    "status": "string",
    "created_at": "timestamp",
    "updated_at": "timestamp"
  }
]
```
- **Response Errors:**  
  - 401 Unauthorized: Invalid or missing JWT token.  

---

#### **PUT /tasks/{id}**
- **Purpose:** Update a specific task.  
- **Auth:** JWT required.  
- **Request Body:**  
```json
{
  "title": "string",
  "description": "string",
  "status": "string"
}
```
- **Response 200:**  
```json
{
  "id": "uuid",
  "title": "string",
  "description": "string",
  "status": "string",
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```
- **Response Errors:**  
  - 401 Unauthorized: Invalid or missing JWT token.  
  - 404 Not Found: Task not found.  

---

#### **DELETE /tasks/{id}**
- **Purpose:** Delete a specific task.  
- **Auth:** JWT required.  
- **Request Body:** None.  
- **Response 204:** No content.  
- **Response Errors:**  
  - 401 Unauthorized: Invalid or missing JWT token.  
  - 404 Not Found: Task not found.  

---

### 5. Project Structure
```
project-root/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── task.py
│   │   ├── routes/
│   │   │   ├── auth.py
│   │   │   ├── tasks.py
│   │   ├── utils/
│   │   │   ├── jwt.py
│   │   ├── main.py
│   │   ├── config.py
│   └── tests/
│       ├── test_auth.py
│       ├── test_tasks.py
├── Dockerfile
├── requirements.txt
└── README.md
```

### 6. Technical Risks
| Risk                          | Likelihood | Impact | Mitigation                                      |
| :---------------------------- | :--------- | :----- | :--------------------------------------------- |
| Incorrect JWT implementation. | Medium     | High   | Use well-tested libraries like PyJWT.          |
| SQL injection vulnerabilities.| Low        | High   | Use parameterized queries in ORM (SQLAlchemy). |
| Scalability issues.           | Medium     | Medium | Optimize database indexing and query patterns. |

### 7. Non-Functional Design Decisions
- **Performance:** FastAPI ensures low latency; database indexing improves query speed.  
- **Security:** All passwords are hashed using bcrypt; JWT tokens are signed with a secret key.  
- **Scalability:** PostgreSQL supports high user and task volumes; Docker ensures horizontal scaling.  
- **Accessibility:** Consistent error codes and messages for developer usability.  

---
**Status:** COMPLETE — Ready for Solution Developer.  
---