---
## HIGH-LEVEL DESIGN (HLD)

**Project:** Todo List REST API with JWT Authentication  
**Prepared by:** Architect Agent  
**Version:** 1.0  

### 1. Technology Stack
| Layer | Technology | Justification |
| :--- | :--- | :--- |
| Frontend | N/A | No frontend development required; API is standalone. |
| Backend | FastAPI (Python) | FastAPI is lightweight, fast, and supports asynchronous programming. It provides built-in support for OpenAPI documentation and JWT authentication. |
| Database | PostgreSQL | PostgreSQL is a reliable, scalable relational database with strong support for ACID transactions, ideal for managing structured data like tasks. |
| Auth | PyJWT | PyJWT is a lightweight library for handling JWT tokens in Python, making it easy to implement token-based authentication. |
| Hosting | Docker + AWS Elastic Beanstalk | Docker ensures consistent deployment environments, while AWS Elastic Beanstalk simplifies deployment and scaling. |

### 2. System Architecture
The system consists of the following components:
```
[Client] → [FastAPI Backend] → [PostgreSQL Database]
                     ↓
               [JWT Authentication]
```

- **Client:** Sends HTTP requests to the API endpoints.
- **FastAPI Backend:** Handles authentication, CRUD operations, and API logic.
- **PostgreSQL Database:** Stores user and task data securely.
- **JWT Authentication:** Ensures secure access to API endpoints.

### 3. Data Models
#### Entity: User
| Field | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| id | UUID | PK, auto | Unique identifier for the user. |
| username | String | Unique, required | User's login name. |
| password_hash | String | Required | Hashed password for authentication. |

#### Entity: Task
| Field | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| id | UUID | PK, auto | Unique identifier for the task. |
| user_id | UUID | FK, required | ID of the user who owns the task. |
| title | String | Required | Title of the task. |
| description | String | Optional | Detailed description of the task. |
| created_at | Timestamp | Auto | Timestamp when the task was created. |
| updated_at | Timestamp | Auto | Timestamp when the task was last updated. |

### 4. API Contracts
#### **POST /login**
- **Purpose:** Authenticate users and issue a JWT token.
- **Auth:** Public.
- **Request Body:**  
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **Response 200:**  
  ```json
  {
    "token": "string"
  }
  ```
- **Response Errors:**  
  - 401 Unauthorized: Invalid username or password.

---

#### **GET /validate-token**
- **Purpose:** Validate the JWT token for active sessions.
- **Auth:** Requires JWT in Authorization header.
- **Request Headers:**  
  ```
  Authorization: Bearer [JWT]
  ```
- **Response 200:**  
  ```json
  {
    "status": "valid"
  }
  ```
- **Response Errors:**  
  - 403 Forbidden: Invalid or expired token.

---

#### **POST /tasks**
- **Purpose:** Create a new task.
- **Auth:** Requires JWT in Authorization header.
- **Request Body:**  
  ```json
  {
    "title": "string",
    "description": "string"
  }
  ```
- **Response 201:**  
  ```json
  {
    "id": "string",
    "title": "string",
    "description": "string",
    "created_at": "timestamp"
  }
  ```
- **Response Errors:**  
  - 400 Bad Request: Title is required.

---

#### **GET /tasks**
- **Purpose:** Retrieve all tasks for the authenticated user.
- **Auth:** Requires JWT in Authorization header.
- **Response 200:**  
  ```json
  [
    {
      "id": "string",
      "title": "string",
      "description": "string",
      "created_at": "timestamp"
    }
  ]
  ```

---

#### **GET /tasks/{id}**
- **Purpose:** Retrieve a specific task by ID.
- **Auth:** Requires JWT in Authorization header.
- **Response 200:**  
  ```json
  {
    "id": "string",
    "title": "string",
    "description": "string",
    "created_at": "timestamp"
  }
  ```
- **Response Errors:**  
  - 404 Not Found: Task not found.

---

#### **PUT /tasks/{id}**
- **Purpose:** Update an existing task.
- **Auth:** Requires JWT in Authorization header.
- **Request Body:**  
  ```json
  {
    "title": "string",
    "description": "string"
  }
  ```
- **Response 200:**  
  ```json
  {
    "id": "string",
    "title": "string",
    "description": "string",
    "updated_at": "timestamp"
  }
  ```
- **Response Errors:**  
  - 400 Bad Request: Title is required.
  - 404 Not Found: Task not found.

---

#### **DELETE /tasks/{id}**
- **Purpose:** Delete a specific task.
- **Auth:** Requires JWT in Authorization header.
- **Response 204:** No content.
- **Response Errors:**  
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
│   │   ├── main.py
│   │   ├── utils/
│   │   │   ├── jwt_handler.py
│   │   └── config.py
│   ├── tests/
│   └── Dockerfile
└── README.md
```

### 6. Technical Risks
| Risk | Likelihood | Impact | Mitigation |
| :--- | :--- | :--- | :--- |
| Incorrect JWT implementation | Medium | High | Use PyJWT and follow best practices for token generation and validation. |
| API performance issues under load | Low | Medium | Optimize database queries and test with high-concurrency scenarios. |
| Security vulnerabilities | Medium | High | Implement HTTPS, validate inputs, and use strong password hashing (e.g., bcrypt). |

### 7. Non-Functional Design Decisions
- **Performance:** FastAPI ensures low-latency responses; database indexing will optimize task retrieval.
- **Security:** JWT tokens are signed using a secret key and include expiration times. Passwords are hashed using bcrypt.
- **Scalability:** The architecture supports containerized deployment for easy scaling.
- **Accessibility:** OpenAPI documentation is auto-generated by FastAPI for developer-friendly interaction.

---
**Status:** COMPLETE — Ready for Solution Developer.  
---