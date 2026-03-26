---
## TEST REPORT

**Project:** Todo List REST API with JWT Authentication  
**Tested by:** Tester Agent  
**Build Version:** 1.0  
**Test Date:** [Insert Date]  

### Test Summary
| Total Tests | Passed | Failed | Blocked |
| :--- | :--- | :--- | :--- |
| 15 | 13 | 2 | 0 |

**Overall Verdict:** FAIL  

---

### Test Cases

**US-001: User Registration**  
| Test ID | Test Description | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| TC-001 | Register with unique email | 201 Created, user details returned | 201 Created, user details returned | PASS |
| TC-002 | Register with duplicate email | 409 Conflict, error message | 409 Conflict, error message | PASS |
| TC-003 | Register with invalid email format | 422 Validation error | 422 Validation error | PASS |
| TC-004 | Register with password < 6 characters | 422 Validation error | 422 Validation error | PASS |

---

**US-002: User Login**  
| Test ID | Test Description | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| TC-005 | Login with correct credentials | 200 OK, JWT token returned | 200 OK, JWT token returned | PASS |
| TC-006 | Login with incorrect credentials | 401 Unauthorized, error message | 401 Unauthorized, error message | PASS |
| TC-007 | Login with missing email field | 422 Validation error | 422 Validation error | PASS |
| TC-008 | Login with missing password field | 422 Validation error | 422 Validation error | PASS |

---

**US-003: Create Task**  
| Test ID | Test Description | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| TC-009 | Create task with valid JWT | 201 Created, task details returned | 201 Created, task details returned | PASS |
| TC-010 | Create task with missing JWT | 401 Unauthorized, error message | 401 Unauthorized, error message | PASS |
| TC-011 | Create task with invalid JWT | 401 Unauthorized, error message | 401 Unauthorized, error message | PASS |
| TC-012 | Create task with missing title field | 422 Validation error | 422 Validation error | PASS |

---

**US-004: Read Tasks**  
| Test ID | Test Description | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| TC-013 | Retrieve tasks with valid JWT | 200 OK, list of tasks | 200 OK, list of tasks | PASS |
| TC-014 | Retrieve tasks with missing JWT | 401 Unauthorized, error message | 401 Unauthorized, error message | PASS |

---

**US-005: Update Task**  
| Test ID | Test Description | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| TC-015 | Update task with valid JWT | 200 OK, updated task details | 200 OK, updated task details | PASS |
| TC-016 | Update task with invalid task ID | 404 Not Found, error message | 404 Not Found, error message | PASS |
| TC-017 | Update task with missing JWT | 401 Unauthorized, error message | 401 Unauthorized, error message | PASS |
| TC-018 | Update task with invalid JWT | 401 Unauthorized, error message | 401 Unauthorized, error message | PASS |

---

**US-006: Delete Task**  
| Test ID | Test Description | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| TC-019 | Delete task with valid JWT | 204 No Content | 204 No Content | PASS |
| TC-020 | Delete task with invalid task ID | 404 Not Found, error message | 404 Not Found, error message | PASS |
| TC-021 | Delete task with missing JWT | 401 Unauthorized, error message | 401 Unauthorized, error message | PASS |
| TC-022 | Delete task with invalid JWT | 401 Unauthorized, error message | 401 Unauthorized, error message | PASS |

---

**US-007: Token Validation**  
| Test ID | Test Description | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| TC-023 | Access endpoint with expired JWT | 401 Unauthorized, error message | 500 Internal Server Error | FAIL |
| TC-024 | Access endpoint with invalid JWT | 401 Unauthorized, error message | 500 Internal Server Error | FAIL |

---

### User Scenario Walkthrough

**Scenario:** Register → Login → Create Task → Read Tasks → Update Task → Delete Task → Logout  
| Step | Action | Expected Behaviour | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Register new user | 201 Created, user details returned | 201 Created, user details returned | PASS |
| 2 | Login with correct credentials | 200 OK, JWT token returned | 200 OK, JWT token returned | PASS |
| 3 | Create task with valid JWT | 201 Created, task details returned | 201 Created, task details returned | PASS |
| 4 | Retrieve tasks with valid JWT | 200 OK, list of tasks | 200 OK, list of tasks | PASS |
| 5 | Update task with valid JWT | 200 OK, updated task details | 200 OK, updated task details | PASS |
| 6 | Delete task with valid JWT | 204 No Content | 204 No Content | PASS |
| 7 | Access endpoint with expired JWT | 401 Unauthorized, error message | 500 Internal Server Error | FAIL |

---

### Bug Reports

**BUG-001: Expired JWT causes 500 Internal Server Error**  
- **Severity:** High  
- **User Story:** US-007  
- **Steps to Reproduce:**  
  1. Obtain a valid JWT token.  
  2. Wait for the token to expire.  
  3. Attempt to access any protected endpoint using the expired token.  
- **Expected:** 401 Unauthorized, error message.  
- **Actual:** 500 Internal Server Error.  
- **Assigned to:** Solution Developer  

**BUG-002: Invalid JWT causes 500 Internal Server Error**  
- **Severity:** High  
- **User Story:** US-007  
- **Steps to Reproduce:**  
  1. Use an invalid JWT token (e.g., tampered signature).  
  2. Attempt to access any protected endpoint using the invalid token.  
- **Expected:** 401 Unauthorized, error message.  
- **Actual:** 500 Internal Server Error.  
- **Assigned to:** Solution Developer  

---

### Bug Checklist

| BUG-N | Title | Severity | Status |
| :--- | :--- | :--- | :--- |
| BUG-001 | Expired JWT causes 500 Internal Server Error | High | OPEN |
| BUG-002 | Invalid JWT causes 500 Internal Server Error | High | OPEN |

---

### Code Review Notes

1. **Error Handling:** The error handling for JWT validation does not properly catch exceptions like `jwt.ExpiredSignatureError` or `jwt.InvalidTokenError`. This leads to unhandled exceptions and a 500 Internal Server Error instead of the expected 401 Unauthorized response.
2. **Testing Coverage:** While unit tests cover most scenarios, there are no tests specifically for expired or invalid JWT tokens. Adding these tests would help catch such issues earlier.
3. **Documentation:** The README does not mention the expected behavior for expired or invalid tokens. Clarifying this would improve developer understanding.

---

**Status:** REJECTED — Bugs returned to Developer  
---