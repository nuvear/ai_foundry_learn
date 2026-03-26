---
## UX SPECIFICATION DOCUMENT

**Project:** Todo List REST API with JWT Authentication  
**Prepared by:** UI/UX Designer Agent  
**Version:** 1.0  

### 1. Information Architecture  
The API interaction is structured as follows:  

- **Authentication:**  
  - `/login`: Authenticate users and issue JWT tokens.  
  - `/validate-token`: Validate the JWT token for active sessions.  

- **Tasks:**  
  - `/tasks`: Endpoint for task creation and retrieval (GET for list, POST for creation).  
  - `/tasks/{id}`: Endpoint for retrieving, updating, or deleting a specific task (GET, PUT, DELETE).  

### 2. Design System  
**Typography:**  
- Heading font: N/A (API; no visual interface).  
- Body font: N/A (API; no visual interface).  

**Colour Palette:**  
N/A (API interaction only; no UI elements).  

**Spacing:**  
N/A (API interaction only; no UI elements).  

### 3. Screen Wireframes  
This project does not include graphical screens, but API interaction wireframes are described below for clarity.  

**Screen: Login (POST `/login`)**  
- **Purpose:** Authenticate users with their username and password, and issue a JWT token.  
- **Request Body:**  
  ```json
  {
    "username": "[string, required]",
    "password": "[string, required]"
  }
  ```  
- **Response:**  
  - **Success (200):**  
    ```json
    {
      "token": "[string, JWT]"
    }
    ```  
  - **Error (401):**  
    ```json
    {
      "error": "Invalid username or password"
    }
    ```  

**Screen: Token Validation (GET `/validate-token`)**  
- **Purpose:** Validate JWT tokens to confirm user session validity.  
- **Request Headers:**  
  ```http
  Authorization: Bearer [JWT]
  ```  
- **Response:**  
  - **Success (200):**  
    ```json
    {
      "status": "valid"
    }
    ```  
  - **Error (403):**  
    ```json
    {
      "error": "Invalid or expired token"
    }
    ```  

**Screen: Create Task (POST `/tasks`)**  
- **Purpose:** Create a new task associated with the authenticated user.  
- **Request Body:**  
  ```json
  {
    "title": "[string, required]",
    "description": "[string, optional]"
  }
  ```  
- **Response:**  
  - **Success (201):**  
    ```json
    {
      "id": "[string, auto-generated]",
      "title": "[string]",
      "description": "[string]",
      "created_at": "[ISO 8601 timestamp]"
    }
    ```  
  - **Error (400):**  
    ```json
    {
      "error": "Title is required"
    }
    ```  

**Screen: Retrieve Tasks (GET `/tasks`)**  
- **Purpose:** Retrieve all tasks associated with the authenticated user.  
- **Response:**  
  - **Success (200):**  
    ```json
    [
      {
        "id": "[string]",
        "title": "[string]",
        "description": "[string]",
        "created_at": "[ISO 8601 timestamp]"
      }
    ]
    ```  

**Screen: Retrieve Task by ID (GET `/tasks/{id}`)**  
- **Purpose:** Retrieve a specific task by its unique ID.  
- **Response:**  
  - **Success (200):**  
    ```json
    {
      "id": "[string]",
      "title": "[string]",
      "description": "[string]",
      "created_at": "[ISO 8601 timestamp]"
    }
    ```  
  - **Error (404):**  
    ```json
    {
      "error": "Task not found"
    }
    ```  

**Screen: Update Task (PUT `/tasks/{id}`)**  
- **Purpose:** Update the title and/or description of an existing task.  
- **Request Body:**  
  ```json
  {
    "title": "[string, required]",
    "description": "[string, optional]"
  }
  ```  
- **Response:**  
  - **Success (200):**  
    ```json
    {
      "id": "[string]",
      "title": "[string]",
      "description": "[string]",
      "updated_at": "[ISO 8601 timestamp]"
    }
    ```  
  - **Error (400):**  
    ```json
    {
      "error": "Title is required"
    }
    ```  
  - **Error (404):**  
    ```json
    {
      "error": "Task not found"
    }
    ```  

**Screen: Delete Task (DELETE `/tasks/{id}`)**  
- **Purpose:** Delete a specific task by its unique ID.  
- **Response:**  
  - **Success (204):** No content.  
  - **Error (404):**  
    ```json
    {
      "error": "Task not found"
    }
    ```  

### 4. User Flows  
**Flow: US-001 — User Authentication**  
1. User sends a POST request to `/login` with their username and password.  
2. System responds with a JWT token upon successful authentication.  
3. User includes the JWT token in the Authorization header for subsequent requests.  
**Error path:** Invalid credentials return a 401 Unauthorized error.  

**Flow: US-003 — Create a Task**  
1. User sends a POST request to `/tasks` with the task title and optional description.  
2. System validates the JWT token and processes the request.  
3. System responds with the created task details.  
**Error path:** Missing title returns a 400 Bad Request error.  

**Flow: US-006 — Delete a Task**  
1. User sends a DELETE request to `/tasks/{id}` with the task ID.  
2. System validates the JWT token and verifies ownership of the task.  
3. System deletes the task and responds with a 204 status.  
**Error path:** Non-existent task ID returns a 404 Not Found error.  

### 5. Component Specifications  
| Component | States | Behaviour |  
| :--- | :--- | :--- |  
| JWT Token | valid, invalid, expired | Used for authenticating and authorizing API requests. |  
| Task | active, deleted | Tasks are created, updated, retrieved, or deleted based on user actions. |  

### 6. Accessibility Requirements  
- API documentation must be written in clear, developer-friendly language.  
- Error messages must be descriptive and actionable.  
- Endpoint responses must adhere to consistent JSON structure for ease of parsing.  

---
**Status:** COMPLETE — Ready for Architect.  
---