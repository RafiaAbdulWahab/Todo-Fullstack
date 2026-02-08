# RESTful API Endpoints for Todo Full-Stack Web Application

This document defines the RESTful API endpoints for communication between the frontend and backend.

---

## Base URL
*   **Development:** `http://localhost:8000`

---

## Authentication
All API endpoints require a valid JWT token to be included in the `Authorization` header of every request. The backend will validate this token and use the authenticated user's ID to enforce user isolation and security.

---

## API Endpoints

### 1. List All Tasks
*   **Endpoint:** `GET /api/tasks`
*   **Description:** Retrieves a list of all tasks belonging to the authenticated user.
*   **Response:**
    *   **200 OK:** An array of task objects.
    *   **401 Unauthorized:** If the JWT token is missing or invalid.

### 2. Create a New Task
*   **Endpoint:** `POST /api/tasks`
*   **Description:** Creates a new task for the authenticated user.
*   **Request Body:** A JSON object containing the task details (e.g., `title`, `description`).
*   **Response:**
    *   **201 Created:** The newly created task object.
    *   **401 Unauthorized:** If the JWT token is missing or invalid.
    *   **422 Unprocessable Entity:** If the request body is invalid.

### 3. Fetch Specific Task Details
*   **Endpoint:** `GET /api/tasks/{id}`
*   **Description:** Retrieves the details of a specific task by its ID. The task must belong to the authenticated user.
*   **Response:**
    *   **200 OK:** The requested task object.
    *   **401 Unauthorized:** If the JWT token is missing or invalid.
    *   **404 Not Found:** If the task with the specified ID does not exist or does not belong to the user.

### 4. Update a Task
*   **Endpoint:** `PUT /api/tasks/{id}`
*   **Description:** Updates the details of a specific task by its ID. The task must belong to the authenticated user.
*   **Request Body:** A JSON object with the updated task details.
*   **Response:**
    *   **200 OK:** The updated task object.
    *   **401 Unauthorized:** If the JWT token is missing or invalid.
    *   **404 Not Found:** If the task with the specified ID does not exist or does not belong to the user.
    *   **422 Unprocessable Entity:** If the request body is invalid.

### 5. Remove a Task
*   **Endpoint:** `DELETE /api/tasks/{id}`
*   **Description:** Deletes a specific task by its ID. The task must belong to the authenticated user.
*   **Response:**
    *   **204 No Content:** If the task was successfully deleted.
    *   **401 Unauthorized:** If the JWT token is missing or invalid.
    *   **404 Not Found:** If the task with the specified ID does not exist or does not belong to the user.

### 6. Toggle Task Completion Status
*   **Endpoint:** `PATCH /api/tasks/{id}/complete`
*   **Description:** Toggles the completion status of a specific task by its ID. The task must belong to the authenticated user.
*   **Response:**
    *   **200 OK:** The updated task object with the new completion status.
    -   **401 Unauthorized:** If the JWT token is missing or invalid.
    -   **404 Not Found:** If the task with the specified ID does not exist or does not belong to the user.
