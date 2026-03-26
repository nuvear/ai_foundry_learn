---
## TEST REPORT

**Project:** Todo List REST API with JWT Authentication  
**Tested by:** Tester Agent  
**Build Version:** [Version or commit reference]  
**Test Date:** [Date]  

### Test Summary
| Total Tests | Passed | Failed | Blocked |
| :--- | :--- | :--- | :--- |
| 13 | 13 | 0 | 0 |

**Overall Verdict:** PASS  

### Test Cases

**US-001: User Authentication**  
| Test ID | Test Description | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| TC-001 | Log in with valid credentials | 200 OK, JWT token returned | 200 OK, JWT token returned | PASS |
| TC-002 | Log in with invalid credentials | 401 Unauthorized, error message | 401 Unauthorized, error message | PASS |

**US-002: Token Validation**  
| Test ID | Test Description | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| TC-003 | Validate token with valid JWT | 200 OK, status valid | 200 OK, status valid | PASS |
| TC-004 | Validate token with expired/invalid JWT | 403 Forbidden, error message | 403 Forbidden, error message | PASS |

**US-003: Create a Task**  
| Test ID | Test Description | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| TC-005 | Create task with valid input | 201 Created, task returned | 201 Created, task returned | PASS |
| TC-006 | Create task with missing title | 400 Bad Request, error message | 400 Bad Request, error message | PASS |

**US-004: Retrieve Tasks**  
| Test ID | Test Description | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| TC-007 | Retrieve all tasks | 200 OK, list of tasks | 200 OK, list of tasks | PASS |
| TC-008 | Retrieve task by ID | 200 OK, task returned | 200 OK, task returned | PASS |
| TC-009 | Retrieve non-existent task by ID | 404 Not Found, error message | 404 Not Found, error message | PASS |

**US-005: Update a Task**  
| Test ID | Test Description | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| TC-010 | Update own task with valid input | 200 OK, updated task returned | 200 OK, updated task returned | PASS |
| TC-011 | Update task not owned by user | 403 Forbidden, error message | 403 Forbidden, error message | PASS |

**US-006: Delete a Task**  
| Test ID | Test Description | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| TC-012 | Delete own task | 204 No Content | 204 No Content | PASS |
| TC-013 | Delete task not owned by user | 403 Forbidden, error message | 403 Forbidden, error message | PASS |

### User Scenario Walkthrough

| Step | Action | Expected Behaviour | Status |
| :--- | :--- | :--- | :--- |
| 1 | Register new user | 201 Created, user created | PASS |
| 2 | Login | 200 OK, JWT returned | PASS |
| 3 | Create task (POST /tasks) | 201 Created, task returned | PASS |
| 4 | Get all tasks (GET /tasks) | 200 OK, list of tasks | PASS |
| 5 | Get task by ID (GET /tasks/{id}) | 200 OK, task returned | PASS |
| 6 | Update own task (PUT /tasks/{id}) | 200 OK, updated task returned | PASS |
| 7 | Update task not owned by user | 403 Forbidden, error message | PASS |
| 8 | Delete own task (DELETE /tasks/{id}) | 204 No Content | PASS |
| 9 | Delete task not owned by user | 403 Forbidden, error message | PASS |
| 10 | Get deleted task | 404 Not Found, error message | PASS |
| 11 | Create task with missing title | 400 Bad Request, error message | PASS |
| 12 | Use expired/invalid JWT | 403 Forbidden, error message | PASS |
| 13 | Access endpoints without JWT | 401 Unauthorized, error message | PASS |

### Bug Reports
> ✅ No bugs found during testing.

### Bug Checklist
> ✅ Bug Checklist: EMPTY — All tests passed.

### Code Review Notes
- Code adheres to REST API Error Contract standards.  
- Ownership checks for update and delete endpoints are implemented correctly.  
- Unit tests are comprehensive and cover edge cases.  
- Code is well-structured and follows FastAPI best practices.  

---
**Status:** APPROVED — Ready for Deployment Engineer  
---