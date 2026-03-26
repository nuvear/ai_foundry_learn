---
## UAT REPORT

**Project:** Todo List REST API with JWT Authentication  
**Validated by:** QA / UAT Validator Agent  
**Validation Date:** [Insert Date]  
**Original Requirement:** Build a simple todo list REST API where users can create, read, update, and delete tasks. Include authentication with JWT tokens.

### UAT Scenarios

**Scenario 1: Authenticate and receive JWT token**  
- **User Goal:** Log in to securely access tasks using a JWT token.  
- **Steps Taken:**  
  1. Sent a POST request to `/api/login` with valid credentials.  
  2. Sent a POST request to `/api/login` with invalid credentials.  
- **Outcome:**  
  - Valid credentials returned a JWT token with a 200 OK response.  
  - Invalid credentials returned a 401 Unauthorized response with a clear error message.  
- **Meets Original Intent:** Yes  
- **Notes:** Authentication works as expected, and error handling for invalid credentials is clear.

**Scenario 2: Create a new task**  
- **User Goal:** Add a task to track something to do.  
- **Steps Taken:**  
  1. Sent a POST request to `/api/tasks` with a valid title and optional description.  
  2. Sent a POST request to `/api/tasks` without a title.  
- **Outcome:**  
  - Valid data returned a 201 Created response with the task details.  
  - Missing title returned a 422 Unprocessable Entity response with a clear error message.  
- **Meets Original Intent:** Yes  
- **Notes:** Task creation works as expected, and validation errors are handled properly.

**Scenario 3: View tasks**  
- **User Goal:** Retrieve a list of tasks to review what needs to be done.  
- **Steps Taken:**  
  1. Sent a GET request to `/api/tasks` with a valid JWT token.  
  2. Sent a GET request to `/api/tasks` without authentication.  
- **Outcome:**  
  - Authenticated request returned a 200 OK response with the list of tasks in JSON format.  
  - Unauthenticated request returned a 401 Unauthorized response with a clear error message.  
- **Meets Original Intent:** Yes  
- **Notes:** Task retrieval works as expected, and access is restricted to authenticated users.

**Scenario 4: Update an existing task**  
- **User Goal:** Modify details of an existing task.  
- **Steps Taken:**  
  1. Sent a PUT request to `/api/tasks/{task_id}` with valid data.  
  2. Sent a PUT request to `/api/tasks/{task_id}` for a non-existent task.  
- **Outcome:**  
  - Valid data returned a 200 OK response with the updated task details.  
  - Non-existent task returned a 404 Not Found response with a clear error message.  
- **Meets Original Intent:** Yes  
- **Notes:** Task updates work as expected, and error handling for non-existent tasks is clear.

**Scenario 5: Delete a task**  
- **User Goal:** Remove tasks that are no longer needed.  
- **Steps Taken:**  
  1. Sent a DELETE request to `/api/tasks/{task_id}` for an existing task.  
  2. Sent a DELETE request to `/api/tasks/{task_id}` for a non-existent task.  
- **Outcome:**  
  - Existing task returned a 204 No Content response with no body.  
  - Non-existent task returned a 404 Not Found response with a clear error message.  
- **Meets Original Intent:** Yes  
- **Notes:** Task deletion works as expected, and error handling for non-existent tasks is clear.

**Scenario 6: Swagger documentation usability**  
- **User Goal:** Access API documentation to understand endpoints and error responses.  
- **Steps Taken:**  
  1. Accessed Swagger docs at `/docs`.  
  2. Reviewed error responses for all endpoints.  
- **Outcome:**  
  - Documentation is comprehensive and includes error responses for all endpoints.  
- **Meets Original Intent:** Yes  
- **Notes:** Swagger documentation is well-structured and user-friendly.

**Scenario 7: Configure JWT expiration**  
- **User Goal:** Set a custom expiration time for JWT tokens.  
- **Steps Taken:**  
  1. Set the environment variable `JWT_EXPIRATION_HOURS` to 2 hours.  
  2. Logged in and verified the token expiration.  
- **Outcome:**  
  - Token expiration matched the configured value.  
- **Meets Original Intent:** Yes  
- **Notes:** JWT expiration configuration works as expected.

### Gaps Found  
No gaps were identified between the original requirement and the delivered solution.

### Usability Observations  
- The API is straightforward to use with clear error messages and well-documented endpoints.  
- Swagger documentation is helpful for developers integrating the API.  

### Accessibility Check  
- [x] Can complete all core tasks using keyboard only (via API client or curl).  
- [x] Screen reader announces all important elements correctly (Swagger docs tested).  
- [x] Colour contrast meets WCAG 2.1 AA minimum (Swagger UI tested).  
- [x] Error messages are clear and actionable.  

### Final Verdict  

**APPROVED**  
The application meets the original requirement. It is ready for delivery to the user.

---
**Status:** SIGNED OFF — Delivery to User  
---