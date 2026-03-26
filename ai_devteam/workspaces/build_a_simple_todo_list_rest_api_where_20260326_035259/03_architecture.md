---
## HIGH-LEVEL DESIGN (HLD)

**Project:** Todo List REST API with JWT Authentication  
**Prepared by:** Architect Agent  
**Version:** 1.0  

### 1. Technology Stack
| Layer          | Technology           | Justification                                                                 |
| :------------- | :------------------- | :--------------------------------------------------------------------------- |
| Backend        | FastAPI (Python)     | Lightweight, fast, and easy-to use framework for building REST APIs.         |
| Database       | PostgreSQL           | Relational database with strong support for structured data and scalability. |
| Auth           | JWT (PyJWT library)  | Provides secure, stateless authentication via tokens.                        |
| Hosting        | Docker + AWS ECS     | Containerization ensures portability; AWS ECS offers scalable hosting.       |
| API Docs       | Swagger (via FastAPI)| Built-in support for OpenAPI/Swagger documentation simplifies integration.   |

### 2. System Architecture
The system consists of the following components:  
```
[Client] → [FastAPI Backend] → [PostgreSQL Database]
                      ↓
              [JWT Authentication]
```

- **Client:** External applications or users interacting with the API.  
- **FastAPI Backend:** Handles HTTP requests, authentication, and CRUD operations.  
- **PostgreSQL Database:** Stores user accounts and tasks securely.  
- **JWT Authentication:** Provides secure access control via stateless tokens.  

### 3. Data Models
#### Entity: User  
| Field       | Type     | Constraints         | Description                          |
| :---------- | :------- | :------------------ | :----------------------------------- |
| id          | UUID     | PK, auto           | Unique identifier for the user.      |
| email       | String   | Unique, required    | User's email address.                |
| password    | String   | Required            | Hashed password for authentication.  |

#### Entity: Task  
| Field       | Type     | Constraints         | Description                          |
| :---------- | :------- | :------------------ | :----------------------------------- |
| id          | UUID     | PK, auto           | Unique identifier for the task.      |
| user_id     | UUID     | FK (User.id), req. | Reference to the user who owns the task. |
| title       | String   | Required            | Task title.                          |
| description | String   | Optional            | Detailed description of the task.    |
| created_at  | DateTime | Auto                | Timestamp of task creation.          |
| updated_at  | DateTime | Auto                | Timestamp of last update.            |

### 4. API Contracts
#### **POST /api/login**  
- **Purpose:** Authenticate user and issue JWT token.  
- **Auth:** Public.  
- **Request Body:**  
  ```json
  {
    "email": "user@example.com",
    "password": "password123"
  }
  ```  
- **Response 200:**  
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "Bearer"
  }
  ```  
- **Response Errors:**  
  - 401 Unauthorized: Invalid credentials.  

#### **POST /api/tasks**  
- **Purpose:** Create a new task.  
- **Auth:** Required.  
- **Request Body:**  
  ```json
  {
    "title": "Buy groceries",
    "description": "Milk, eggs, bread"
  }
  ```  
- **Response 201:**  
  ```json
  {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "created_at": "2023-10-01T12:00:00Z",
    "updated_at": "2023-10-01T12:00:00Z"
  }
  ```  
- **Response Errors:**  
  - 400 Bad Request: Missing required fields.  

#### **GET /api/tasks**  
- **Purpose:** Retrieve all tasks for the authenticated user.  
- **Auth:** Required.  
- **Request Body:** None.  
- **Response 200:**  
  ```json
  [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "created_at": "2023-10-01T12:00:00Z",
      "updated_at": "2023-10-01T12:00:00Z"
    }
  ]
  ```  
- **Response Errors:**  
  - 401 Unauthorized: Invalid or missing token.  

#### **PUT /api/tasks/{id}**  
- **Purpose:** Update an existing task.  
- **Auth:** Required.  
- **Request Body:**  
  ```json
  {
    "title": "Buy groceries",
    "description": "Milk, eggs, bread, cheese"
  }
  ```  
- **Response 200:**  
  ```json
  {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread, cheese",
    "created_at": "2023-10-01T12:00:00Z",
    "updated_at": "2023-10-01T12:30:00Z"
  }
  ```  
- **Response Errors:**  
  - 404 Not Found: Task does not exist.  

#### **DELETE /api/tasks/{id}**  
- **Purpose:** Delete a task.  
- **Auth:** Required.  
- **Request Body:** None.  
- **Response 204:** No content.  
- **Response Errors:**  
  - 404 Not Found: Task does not exist.  

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
│   │   ├── services/
│   │   │   ├── jwt.py
│   │   │   ├── user_service.py
│   │   │   ├── task_service.py
│   │   ├── main.py
│   ├── tests/
│   │   ├── test_auth.py
│   │   ├── test_tasks.py
│   ├── Dockerfile
│   └── requirements.txt
└── README.md
```

### 6. Technical Risks
| Risk                            | Likelihood | Impact | Mitigation                                   |
| :------------------------------ | :--------- | :----- | :------------------------------------------ |
| Incorrect JWT implementation    | Medium     | High   | Use a proven library (PyJWT) and test thoroughly. |
| Unauthorized data access        | Low        | High   | Validate user ownership for all task operations. |
| Scalability under high load     | Medium     | Medium | Optimize database queries and use connection pooling. |

### 7. Non-Functional Design Decisions
- **Performance:** FastAPI ensures low-latency responses. Database queries will be optimized with indexes on `user_id`.  
- **Security:** JWT tokens are signed using a secure secret key. Passwords are stored as salted hashes using bcrypt.  
- **Scalability:** The system is containerized with Docker, enabling horizontal scaling via AWS ECS.  
- **Accessibility:** Swagger documentation is auto-generated for developers to integrate easily.  

---
**Status:** COMPLETE — Ready for Solution Developer.  
---