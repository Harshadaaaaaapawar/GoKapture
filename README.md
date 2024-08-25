## Getting Started

### Prerequisites

Ensure you have the following installed:

- Docker
- Docker Compose
- Python 3

### Running the Application Locally

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/task-manager-api.git
   cd task-manager-api
   ```

2. Build and start the application using Docker Compose:

   ```bash
   docker-compose up --build
   ```

3. The API will be available at http://localhost:5000.

### Running Tests

1. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Run the tests:

   ```bash
   pytest
   ```

## Assumptions

The application assumes basic user roles (Admin and User). Admins have access to more features, such as managing all tasks.

## Example Endpoints

1. User Registration:

   ```bash
   POST /api/register
   {
   "username": "user1",
   "password": "password123",
   "role": "User"
   }
   ```

2. User Login
   ```bash
   POST /api/login
   {
   "username": "user1",
   "password": "password123"
   }
   ```
3. Create Task

   ```bash
   POST /api/tasks
   {
   "title": "New Task",
   "description": "Task description",
   "status": "Todo",
   "priority": "High",
   "due_date": "2024-07-31"
   }
   ```

4. Get Tasks with Pagination, Filtering, and Search

   ```bash
   GET /api/tasks?page=1&per_page=5&status="Todo"&priority="High"&search="task"
   ```

5. Update task

   ```bash
   PUT /api/tasks/{taskId}
   {
   "title": "Updated Task",
   "description": "Updated description",
   "status": "In Progress",
   "priority": "Medium"
   }
   ```
