# MASTER PROJECT DEVELOPMENT PROMPT
# EMPLOYEE HELPDESK – AI-POWERED EMPLOYEE SUPPORT SYSTEM

Act as a senior full-stack developer, software architect, Python backend engineer, React developer, database designer, AI engineer, UI/UX designer, and technical mentor.

I want you to help me build a complete, professional, industry-standard project named **Employee Helpdesk – AI-Powered Employee Support System**.

This is an academic/training capstone project. It must satisfy all the functional, technical, architectural, testing, and demonstration requirements described below.

I am a beginner/intermediate developer. Therefore, guide me through the project step by step, explaining every file, every function, every API, every database relationship, and every command.

Do not skip implementation details.

---

# 1. PROJECT OVERVIEW

Build an AI-powered employee helpdesk application where employees can submit IT or organizational support requests and support staff can manage, investigate, prioritize, and resolve those requests.

The system must use AI to analyze tickets and provide recommendations, but AI must never automatically resolve tickets or make final operational decisions.

A human support staff member must remain responsible for reviewing AI recommendations and managing the ticket lifecycle.

The application must have two separate role-based experiences:

1. Employee Portal
2. Support Staff Portal

Both portals must use the same application, backend, database, and AI integration.

## Main Objectives

- Allow employees to create and track support tickets.
- Allow support staff to manage tickets from all employees.
- Provide AI-powered ticket analysis using a free local language model.
- Recommend ticket categories and priorities.
- Generate suggested responses and resolution guidance.
- Maintain complete ticket activity history.
- Collect human feedback on AI recommendations.
- Provide dashboards and ticket analytics.
- Store all operational information in PostgreSQL.
- Ensure role-based access control and secure authentication.

---

# 2. TECHNOLOGY STACK

Use exactly the following core technologies.

## Frontend

- React.js
- Vite
- JavaScript
- Tailwind CSS
- React Router DOM
- Axios
- Lucide React icons
- Recharts for dashboard charts

## Backend

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- Uvicorn
- JWT authentication
- Passlib or an appropriate secure password-hashing library

## Database

- PostgreSQL
- pgAdmin for database administration
- SQLAlchemy ORM

## AI Integration

- Ollama
- Qwen2.5 3B Instruct (or a suitable free local alternative)
- Local model execution only
- Structured JSON output from the model

## Testing

- pytest
- FastAPI TestClient
- Database test fixtures
- Mocked AI integration for model-unavailable tests

## Development Environment

- Windows
- PyCharm
- PowerShell terminal
- Git and GitHub

Do not use paid APIs, paid AI services, or cloud-hosted LLM inference.

Do not use SQLite as the application's operational database.

---

# 3. APPLICATION IDENTITY AND DESIGN

Application name: **Employee Helpdesk**

Create a premium, modern enterprise SaaS design.

The application should look like a professionally developed internal company support platform rather than a basic student CRUD project.

## Visual Identity

Use a consistent design system:

- Primary background: dark navy or deep blue.
- Primary accent: electric blue.
- Secondary accent: subtle violet.
- Main content: clean white or light grey surfaces.
- Typography: modern and readable.
- Cards: clean, rounded, subtle shadows.
- Buttons: consistent styling and hover states.
- Icons: Lucide React.
- Charts: clean enterprise-style visualizations.
- Tables: professional spacing, filters, badges, and pagination.

Avoid excessive gradients, unnecessary animations, cluttered layouts, and oversized decorative elements.

The application must be responsive and usable on desktop and tablet screens.

Create a consistent sidebar, header, navigation system, dashboard cards, forms, tables, modals, and ticket detail pages.

---

# 4. ROLE-BASED LOGIN AND AUTHENTICATION

The application must have a login system with two roles:

- `employee`
- `support_staff`

## Login Page

Create a professional login page with:

- Employee Helpdesk branding.
- Email input.
- Password input.
- Login button.
- Validation messages.
- Loading state.
- Error handling.

After successful login, redirect the user according to their role.

Employees must be redirected to the Employee Dashboard.

Support staff must be redirected to the Support Dashboard.

## Authentication Requirements

- Store user accounts in PostgreSQL.
- Never store plain-text passwords.
- Hash passwords securely.
- Use JWT access tokens.
- Protect private API endpoints.
- Validate tokens on the backend.
- Implement role-based authorization.
- Provide logout functionality.
- Prevent employees from accessing support staff APIs.
- Prevent employees from viewing another employee's tickets.
- Do not depend only on frontend route protection.
- Enforce authorization on every protected backend operation.

For the initial demonstration, provide a secure way to create sample employee and support staff accounts.

Do not provide unrestricted public support staff registration.

---

# 5. EMPLOYEE PORTAL

Create a dedicated Employee Portal with its own navigation and dashboard.

The employee should only see information associated with their account and tickets.

## Employee Sidebar

Include:

- Dashboard
- Create Ticket
- My Tickets
- Notifications or activity indicators only where supported by existing ticket data
- Profile
- Logout

Do not add unrelated features.

## 5.1 Employee Dashboard

Display dashboard cards for:

- Total Tickets
- New Tickets
- In Progress Tickets
- Resolved Tickets

Also display:

- Recent tickets.
- Ticket status distribution.
- A clear Create New Ticket action.
- Recent activity on the employee's tickets.

All dashboard metrics must be calculated from PostgreSQL data.

## 5.2 Create Ticket

Create a ticket submission form with:

- Subject
- Detailed description
- Category
- Priority

Suggested categories:

- Hardware
- Software
- Network
- Access and Permissions
- Email
- Other

Priority values:

- Low
- Medium
- High
- Critical

Requirements:

- Validate required fields.
- Show useful validation messages.
- Submit ticket to FastAPI.
- Save ticket in PostgreSQL.
- Automatically associate the ticket with the authenticated employee.
- Assign initial status as `New`.
- Record ticket creation in the activity history.
- Display confirmation after successful submission.

Employees must not be able to impersonate another requester by supplying another user ID.

## 5.3 My Tickets

Display all tickets created by the logged-in employee.

Each ticket should show:

- Ticket ID
- Subject
- Category
- Priority
- Current status
- Created date
- Last updated date

Provide:

- Search
- Status filtering
- Priority filtering
- Sorting
- Pagination where appropriate

Employees must only see their own tickets.

## 5.4 Employee Ticket Details

When an employee opens a ticket, display:

- Ticket ID
- Subject
- Full description
- Category
- Current priority
- Current status
- Creation date
- Last updated date
- Assigned support staff member, when applicable
- Comments
- Activity timeline
- AI suggestions, where available
- Feedback option

### Expanded Ticket Status Tracker

This is an important UI requirement.

Create a visually clear status progression:

`New → In Progress → Resolved`

Display:

- Current status.
- Completed stages.
- Current active stage.
- Pending stages.
- Date and time of each transition.
- Previous status changes.
- Person responsible for the update.
- Relevant activity notes.
- Resolution notes when resolved.

Use a visual stepper or timeline rather than displaying status as a simple text badge.

If a ticket is reopened, record the reopening as a new activity event. Never delete the previous status history.

Employees can view the status tracker but cannot change ticket status or priority.

## 5.5 Employee Comments

Allow employees to:

- Add comments to their tickets.
- View support staff responses.
- Read the complete conversation associated with a ticket.

Record comments in the ticket activity history.

Ensure employees cannot comment on tickets that do not belong to them.

## 5.6 AI Suggestions and Feedback

Employees can view AI suggestions associated with their tickets, where appropriate.

Display:

- Recommended category.
- Recommended priority.
- AI explanation.
- Suggested response or resolution guidance, if available.

Allow employees to provide feedback on whether the AI suggestion was helpful.

Feedback must be stored in PostgreSQL.

---

# 6. SUPPORT STAFF PORTAL

Create a separate Support Staff Portal with its own dashboard, navigation, and ticket-management functionality.

Support staff must be able to access tickets from all employees.

## Support Sidebar

Include:

- Dashboard
- All Tickets
- New Tickets
- In Progress
- Resolved
- AI Assistance
- AI Feedback
- Logout

These sections must be implemented using the same underlying ticket records, not separate duplicated data.

## 6.1 Support Dashboard

Display:

- Total Tickets
- New Tickets
- In Progress Tickets
- Resolved Tickets
- High-Priority Tickets
- Critical-Priority Tickets

Also display:

- Ticket status distribution chart.
- Priority distribution chart.
- Recent tickets.
- Recently updated tickets.
- Ticket category distribution.

All values must be calculated using PostgreSQL queries or appropriate SQLAlchemy aggregate queries.

## 6.2 All Tickets

Create a professional ticket management table.

Columns:

- Ticket ID
- Subject
- Employee/Requester
- Category
- Priority
- Status
- Assigned Support Staff
- Created Date
- Last Updated
- Action

Provide:

- Search by ticket ID or subject.
- Filter by status.
- Filter by priority.
- Filter by category.
- Filter by requester where appropriate.
- Sort by creation date and priority.
- Pagination.

## 6.3 Support Ticket Details

When support staff opens a ticket, display:

- Employee information.
- Ticket subject and description.
- Category.
- Current priority.
- Current status.
- Assigned staff member.
- Full activity timeline.
- Comments.
- AI analysis.
- AI recommendations.
- Resolution notes.

The support ticket details page must include the same expanded status tracker as the employee view.

However, support staff must also have controls to update the ticket.

## 6.4 Status Management

Support staff can update ticket status:

- New
- In Progress
- Resolved

Support staff may reopen a resolved ticket where necessary.

Every change must:

- Update the ticket's current status.
- Record the previous status.
- Record the new status.
- Record the person performing the update.
- Record the timestamp.
- Save any relevant update note.
- Create a ticket activity record.

Never overwrite or delete previous activity records.

## 6.5 Priority Management

Support staff can change priority:

- Low
- Medium
- High
- Critical

The system must retain the previous and new priority in activity history.

AI priority recommendations must not automatically overwrite the actual ticket priority.

## 6.6 Assignment

Support staff must be able to assign a ticket to a support staff member.

Store the assigned staff member using a foreign-key relationship to the users table.

Record assignment changes in ticket activity history.

## 6.7 Support Comments and Resolution Notes

Support staff can:

- Add comments.
- Respond to employee comments.
- Add resolution notes.
- View the full ticket conversation.

The system must distinguish comments and status-change activities appropriately.

---

# 7. AI-POWERED TICKET ANALYSIS

AI is one of the core requirements.

Use Ollama with a free locally running model such as:

`qwen2.5:3b`

The AI must run locally.

Do not use:

- OpenAI paid APIs.
- Azure OpenAI.
- Gemini paid APIs.
- Cloud LLM inference.
- Any paid external AI service.

## 7.1 AI Analysis Workflow

When support staff clicks the Analyze Ticket button:

1. Backend retrieves the ticket information.
2. Backend sends the relevant ticket details to the local Ollama model.
3. The model analyzes the issue.
4. The model returns structured JSON.
5. Backend validates the response.
6. Backend stores the suggestion in PostgreSQL.
7. Frontend displays the analysis.

## 7.2 AI Output

The AI should return:

- Suggested category.
- Suggested priority.
- Explanation.
- Short issue summary.
- Suggested response.
- Recommended troubleshooting steps.
- Confidence score, if reliably supported.

Example structure:

{
  "suggested_category": "Network",
  "suggested_priority": "High",
  "summary": "Employee is unable to access the internal network.",
  "explanation": "The reported issue may affect access to essential company resources.",
  "suggested_response": "Please confirm whether the issue occurs on other devices.",
  "troubleshooting_steps": [
    "Check network connectivity.",
    "Verify VPN configuration.",
    "Confirm whether other employees are affected."
  ],
  "confidence": 0.87
}

Validate all returned values before saving them.

Do not blindly trust the model output.

If JSON parsing or validation fails, handle the failure gracefully.

## 7.3 Human-in-the-Loop AI Workflow

AI recommendations are advisory only.

The support staff member must be able to:

- Review AI analysis.
- Accept a suggested category.
- Accept a suggested priority.
- Reject recommendations.
- Modify recommendations before applying them.
- Use the suggested response as a reference.

If a recommendation is accepted and applied, update the relevant ticket field through a normal backend operation and record the human decision in activity history.

Never automatically resolve tickets using AI.

## 7.4 AI Unavailable Handling

If Ollama is not running or the model is unavailable:

- Do not crash the backend.
- Return a meaningful error.
- Show a clear message in the frontend.
- Keep existing ticket functionality available.
- Do not invent AI results.
- Log the failure.

The rest of the application must continue working without AI.

---

# 8. DATABASE DESIGN

Use PostgreSQL as the only operational database.

Design normalized relational tables with appropriate primary keys, foreign keys, constraints, indexes, and timestamps.

At minimum, create the following five operational data areas, with a users table for authentication.

## 8.1 Users Table

Fields:

- id
- full_name
- email
- password_hash
- role
- created_at
- updated_at

Roles:

- employee
- support_staff

Email must be unique.

Passwords must be securely hashed.

## 8.2 Tickets Table

Fields:

- id
- subject
- description
- requester_id
- assigned_to_id
- category
- priority
- status
- created_at
- updated_at
- resolved_at

Relationships:

- requester_id references users.id.
- assigned_to_id references users.id and may be null.

## 8.3 Ticket Activities Table

Fields:

- id
- ticket_id
- actor_id
- activity_type
- old_value
- new_value
- comment
- created_at

Activity types may include:

- ticket_created
- status_changed
- priority_changed
- assigned
- comment_added
- resolution_added
- ticket_reopened
- ai_recommendation_applied

Use this table to maintain a complete and chronological ticket history.

## 8.4 AI Suggestions Table

Fields:

- id
- ticket_id
- suggested_category
- suggested_priority
- summary
- explanation
- suggested_response
- troubleshooting_steps
- confidence
- model_name
- status
- created_at

Suggestion status may include:

- pending
- accepted
- rejected
- modified

Use JSONB where appropriate for structured troubleshooting steps.

## 8.5 AI Feedback Table

Fields:

- id
- suggestion_id
- employee_id
- is_helpful
- feedback_comment
- created_at

Use appropriate foreign keys.

Prevent unauthorized feedback submissions.

## Database Requirements

- Use SQLAlchemy models.
- Create database relationships.
- Use Pydantic schemas separately from ORM models.
- Keep database connection details in environment variables.
- Use database sessions properly.
- Use migrations with Alembic where appropriate.
- Avoid hardcoded credentials.
- Include meaningful indexes and constraints.
- Provide SQL queries demonstrating JOIN and aggregate operations.

The database must preserve all ticket information after backend restart.

---

# 9. FASTAPI BACKEND ARCHITECTURE

Use a clean modular backend structure.

Recommended structure:

backend/
- app/
  - main.py
  - database.py
  - models/
    - user.py
    - ticket.py
    - ticket_activity.py
    - ai_suggestion.py
    - ai_feedback.py
  - schemas/
    - auth.py
    - user.py
    - ticket.py
    - activity.py
    - ai.py
    - feedback.py
  - routes/
    - auth.py
    - users.py
    - tickets.py
    - activities.py
    - ai.py
    - dashboard.py
  - services/
    - auth_service.py
    - ticket_service.py
    - ai_service.py
    - dashboard_service.py
  - dependencies/
    - auth.py
    - permissions.py
  - utils/
    - security.py
    - logging_config.py
- tests/
- .env
- .env.example
- requirements.txt
- README.md

You may improve the structure if necessary, but keep the application modular and understandable.

Do not put all backend functionality inside main.py.

---

# 10. REQUIRED REST API ENDPOINTS

Implement REST APIs with correct HTTP methods, validation, authorization, and response codes.

## Authentication

- POST /api/auth/login
- POST /api/auth/register (employee registration only, if enabled)
- GET /api/auth/me

Provide a secure process for creating initial support staff accounts.

## Users

- GET /api/users/me
- GET /api/users/support-staff (authorized users only)

## Tickets

- POST /api/tickets/
- GET /api/tickets/
- GET /api/tickets/my
- GET /api/tickets/{ticket_id}
- PUT /api/tickets/{ticket_id}
- PATCH /api/tickets/{ticket_id}/status
- PATCH /api/tickets/{ticket_id}/priority
- PATCH /api/tickets/{ticket_id}/assign

Enforce role-based access on every endpoint.

## Activities and Comments

- GET /api/tickets/{ticket_id}/activities
- POST /api/tickets/{ticket_id}/comments

## AI

- POST /api/tickets/{ticket_id}/analyze
- GET /api/tickets/{ticket_id}/ai-suggestions
- PATCH /api/ai-suggestions/{suggestion_id}/decision

## Feedback

- POST /api/ai-suggestions/{suggestion_id}/feedback
- GET /api/ai-feedback (authorized support staff only)

## Dashboard

- GET /api/dashboard/employee
- GET /api/dashboard/support

Use Pydantic request and response schemas.

Return appropriate errors for:

- Invalid input.
- Missing authentication.
- Invalid token.
- Unauthorized role.
- Missing ticket.
- Access to another employee's ticket.
- Database errors.
- AI service unavailability.

Use appropriate HTTP codes such as 400, 401, 403, 404, 422, and 503 where applicable.

Document all APIs through FastAPI Swagger documentation.

---

# 11. FRONTEND ARCHITECTURE

Use React with Vite.

Recommended structure:

frontend/
- src/
  - api/
    - axios.js
    - authService.js
    - ticketService.js
    - dashboardService.js
    - aiService.js
  - components/
    - common/
    - dashboard/
    - tickets/
    - ai/
    - layout/
  - pages/
    - Login.jsx
    - employee/
      - EmployeeDashboard.jsx
      - CreateTicket.jsx
      - MyTickets.jsx
      - EmployeeTicketDetails.jsx
    - support/
      - SupportDashboard.jsx
      - AllTickets.jsx
      - SupportTicketDetails.jsx
      - AIFeedback.jsx
  - layouts/
    - EmployeeLayout.jsx
    - SupportLayout.jsx
  - context/
    - AuthContext.jsx
  - hooks/
  - routes/
    - ProtectedRoute.jsx
    - RoleRoute.jsx
  - utils/
  - App.jsx
  - main.jsx
  - index.css

You may improve the structure, but maintain clear separation of responsibilities.

## Frontend Requirements

- Separate employee and support staff layouts.
- Protected routes.
- Role-based navigation.
- JWT handling.
- Axios API integration.
- Loading indicators.
- Error messages.
- Empty states.
- Form validation.
- Confirmation dialogs for important actions.
- Responsive design.
- Reusable components.
- No hardcoded mock data in the final integrated application.

Use real backend API responses for all ticket and dashboard data.

---

# 12. TICKET LIFECYCLE AND BUSINESS RULES

Implement the ticket lifecycle:

New → In Progress → Resolved

Allow reopening a ticket where necessary.

Important rules:

1. Employees can create tickets and view their own tickets.
2. Employees cannot change ticket status or priority.
3. Support staff can manage all tickets.
4. Only support staff can assign tickets.
5. Every ticket status change must be recorded.
6. Every priority change must be recorded.
7. Every assignment change must be recorded.
8. All comments must be associated with a ticket and author.
9. AI recommendations must be stored separately from actual ticket values.
10. AI must never automatically resolve a ticket.
11. Historical activities must never be deleted when a ticket is updated.
12. All information must persist in PostgreSQL.
13. Both portals must use the same underlying ticket records.
14. Enforce all business rules in the backend, not just in React.

---

# 13. SQL REQUIREMENTS

Demonstrate SQL JOIN operations and aggregate queries.

Examples:

- Retrieve tickets with employee names.
- Retrieve tickets with assigned support staff names.
- Retrieve ticket activities with actor names.
- Count tickets by status.
- Count tickets by priority.
- Count tickets by category.
- Retrieve the latest activity for each ticket.
- Calculate employee ticket totals.
- Calculate support dashboard metrics.
- Retrieve AI feedback statistics.

Use SQLAlchemy queries in the actual application.

Include representative SQL queries in the project documentation.

---

# 14. TESTING REQUIREMENTS

Use pytest.

Create tests for all major functionality.

At minimum, include:

## Authentication Tests

- Valid login.
- Invalid password.
- Missing credentials.
- Invalid JWT.
- Employee cannot access support endpoints.

## Ticket Tests

- Create valid ticket.
- Retrieve ticket.
- Retrieve only the employee's own tickets.
- Support staff can retrieve all tickets.
- Reject invalid ticket input.
- Reject access to another employee's ticket.

## Workflow Tests

- Update ticket status.
- Update ticket priority.
- Assign ticket.
- Record activity history.
- Reopen a resolved ticket.
- Prevent employee status changes.

## AI Tests

- Successful mocked AI response.
- Invalid AI output.
- Ollama unavailable.
- No AI result is invented when the model is unavailable.
- AI recommendations do not automatically modify ticket fields.

## Feedback Tests

- Submit valid feedback.
- Reject unauthorized feedback.
- Retrieve feedback as support staff.

Use test fixtures and a separate test database configuration.

Do not require an actual Ollama model to run ordinary automated tests. Mock the AI service.

---

# 15. LOGGING AND ERROR HANDLING

Implement structured application logging.

Log:

- Authentication failures.
- Ticket creation.
- Ticket updates.
- Status changes.
- Priority changes.
- Assignment changes.
- AI analysis attempts.
- AI service errors.
- Database errors.

Never log passwords, access tokens, or other secrets.

Provide meaningful frontend error messages.

Avoid exposing internal stack traces to end users.

---

# 16. ENVIRONMENT CONFIGURATION

Create:

- `.env`
- `.env.example`
- `.gitignore`
- `requirements.txt`

Environment variables should include:

- DATABASE_URL
- SECRET_KEY
- ALGORITHM
- ACCESS_TOKEN_EXPIRE_MINUTES
- OLLAMA_BASE_URL
- OLLAMA_MODEL

Do not hardcode database passwords, secret keys, or API credentials.

Never commit `.env` to GitHub.

Include `.env.example` with placeholder values.

---

# 17. REQUIRED LIVE DEMONSTRATION SCENARIOS

The completed application must demonstrate these six scenarios.

### Scenario 1: Routine Ticket

1. Employee logs in.
2. Employee creates a routine ticket.
3. Ticket is stored in PostgreSQL.
4. Support staff logs in.
5. Support staff views the new ticket.
6. Support staff runs AI analysis.
7. Support staff reviews the recommendation.
8. Support staff updates the ticket status.
9. Employee sees the updated status and activity timeline.

### Scenario 2: Major Outage

1. Employee submits a ticket describing a major system or network outage.
2. AI identifies the issue and recommends an appropriate high or critical priority.
3. Support staff reviews the recommendation.
4. Support staff decides the actual priority.
5. The decision is saved and recorded in activity history.

### Scenario 3: Human Correction of AI

1. AI recommends a category or priority.
2. Support staff disagrees with the recommendation.
3. Support staff rejects or modifies it.
4. The final decision is saved.
5. The activity history shows the human decision.

### Scenario 4: AI Unavailable

1. Stop Ollama or make the local model unavailable.
2. Attempt AI analysis.
3. The application displays a clear error.
4. Existing ticket functionality continues working.
5. No fabricated AI result is displayed.

### Scenario 5: Invalid Request

1. Submit a ticket with missing or invalid information.
2. Backend rejects it with appropriate validation errors.
3. Frontend displays a useful error.
4. No invalid ticket is saved.

### Scenario 6: Database Persistence

1. Create tickets.
2. Add comments.
3. Change status and priority.
4. Generate AI suggestions and feedback.
5. Restart the backend.
6. Log in again.
7. Verify that all previously saved data remains available.

---

# 18. DOCUMENTATION AND SUBMISSION REQUIREMENTS

Create a complete README.md containing:

- Project overview.
- Problem statement.
- Objectives.
- Features.
- Technology stack.
- Architecture diagram.
- Database schema and relationships.
- Backend folder structure.
- Frontend folder structure.
- Installation instructions.
- PostgreSQL setup.
- Ollama installation and model setup.
- Environment configuration.
- How to run backend.
- How to run frontend.
- How to create demo accounts.
- API endpoint documentation.
- Testing instructions.
- Six live demonstration scenarios.
- Screenshots section.
- Known limitations.

Also create:

- Architecture diagram.
- Database ER diagram.
- API documentation.
- Requirements file.
- `.env.example`.
- Test suite.

Keep documentation aligned with the actual implementation.

---

# 19. GIT AND GITHUB

Use Git for version control.

Create meaningful commits after each major phase.

Suggested commit messages:

- Initial project setup
- Configure FastAPI backend
- Add PostgreSQL database models
- Implement authentication and role permissions
- Implement ticket management APIs
- Add ticket activity history
- Integrate local Ollama AI
- Add AI feedback workflow
- Build employee portal
- Build support staff portal
- Add dashboard analytics
- Add automated tests
- Complete documentation

Do not commit:

- `.env`
- Virtual environments
- `node_modules`
- Python cache files
- Model files
- Database backups
- Local secrets

---

# 20. DEVELOPMENT WORKFLOW – VERY IMPORTANT

I want you to build the project with me from scratch.

Do not generate the entire project in one response.

Work in clearly defined phases.

For every phase:

1. Explain the objective.
2. Explain what we are building.
3. Show the exact folder structure.
4. Tell me exactly where to create each folder and file.
5. Provide complete code for every required file.
6. Explain what each file does.
7. Provide exact Windows PowerShell commands.
8. Explain what each command does.
9. Tell me how to run the code.
10. Tell me how to test it.
11. Show the expected output.
12. Help debug any errors before moving on.

Never provide incomplete code with statements such as "add the remaining logic yourself."

When modifying an existing file, provide the complete updated file, not just a partial snippet, unless I explicitly request a small patch.

Do not move to the next phase until I confirm that the current phase works.

Avoid introducing unnecessary packages.

Explain beginner-level concepts whenever they are important to the implementation.

Maintain consistent file names, API routes, database fields, imports, and architecture across all phases.

Do not silently change earlier implementation decisions.

---

# 21. PROJECT IMPLEMENTATION PHASES

Follow this exact sequence unless a genuine technical dependency requires a small adjustment.

## PHASE 1 – Project Setup

- Create project root.
- Create backend directory.
- Create Python virtual environment.
- Install initial dependencies.
- Create FastAPI application.
- Create health endpoint.
- Run Uvicorn.
- Verify Swagger documentation.

## PHASE 2 – PostgreSQL Setup and Database Design

- Create PostgreSQL database.
- Configure SQLAlchemy.
- Configure database connection.
- Create users table.
- Create tickets table.
- Create ticket activities table.
- Create AI suggestions table.
- Create AI feedback table.
- Verify tables in pgAdmin.
- Test database connectivity.

## PHASE 3 – Authentication and Role-Based Access

- Password hashing.
- Login API.
- JWT generation.
- Current-user dependency.
- Employee role protection.
- Support staff role protection.
- Demo account creation.
- Authentication tests.

## PHASE 4 – Ticket CRUD APIs

- Create tickets.
- List employee tickets.
- List all support tickets.
- Retrieve ticket details.
- Update ticket information where permitted.
- Input validation.
- Role-based access control.

## PHASE 5 – Ticket Workflow and Activity History

- Status changes.
- Priority changes.
- Assignment.
- Comments.
- Resolution notes.
- Reopening.
- Expanded ticket timeline data.
- Activity history APIs.

## PHASE 6 – Dashboard APIs and SQL

- Employee dashboard.
- Support dashboard.
- SQL JOIN queries.
- Aggregate queries.
- Ticket statistics.
- Dashboard tests.

## PHASE 7 – Local AI Integration

- Install Ollama.
- Download and configure Qwen2.5 3B Instruct.
- Build AI service.
- Create analysis prompts.
- Validate structured JSON output.
- Store AI suggestions.
- Handle invalid AI responses.
- Handle Ollama unavailability.

## PHASE 8 – Human Feedback and AI Decision Workflow

- Accept AI recommendation.
- Reject AI recommendation.
- Modify recommendation.
- Apply approved changes.
- Record human decisions.
- Employee feedback.
- Support staff feedback dashboard/API.

## PHASE 9 – Backend Testing and Finalization

- Complete pytest suite.
- Authentication tests.
- Ticket tests.
- Role-permission tests.
- Activity tests.
- AI mock tests.
- Database persistence tests.
- Logging and error handling.
- API documentation review.

## PHASE 10 – React Frontend Setup

- Create Vite application.
- Install frontend dependencies.
- Configure Tailwind CSS.
- Configure Axios.
- Configure React Router.
- Set up application styling.
- Create reusable components.

## PHASE 11 – Login and Authentication UI

- Login page.
- Auth context.
- JWT handling.
- Protected routes.
- Role-based routes.
- Employee and support layouts.
- Logout.

## PHASE 12 – Employee Portal

- Employee dashboard.
- Create ticket form.
- My tickets page.
- Ticket details page.
- Expanded status tracker.
- Comments.
- AI suggestions.
- Feedback.

## PHASE 13 – Support Staff Portal

- Support dashboard.
- All tickets page.
- Search and filters.
- Support ticket details.
- Status management.
- Priority management.
- Assignment.
- Comments and resolution notes.
- AI analysis interface.
- AI recommendation decisions.
- AI feedback page.

## PHASE 14 – Full Integration and Final Demonstration

- Connect every page to the actual backend.
- Verify all role permissions.
- Verify database persistence.
- Run all tests.
- Execute all six demonstration scenarios.
- Fix integration issues.
- Capture screenshots.
- Finalize README.
- Prepare the project for GitHub submission.

---

# 22. STRICT RULES

Follow these rules throughout the project:

1. Do not remove any required capstone functionality.
2. Do not add unrelated features.
3. Do not use paid AI APIs.
4. Do not use SQLite.
5. Do not use hardcoded mock data in the completed application.
6. Do not let AI automatically resolve tickets.
7. Do not allow employees to access other employees' tickets.
8. Do not allow employees to modify their own ticket status or priority.
9. Do not store passwords in plain text.
10. Do not expose secrets in source code or GitHub.
11. Do not skip database persistence.
12. Do not skip testing.
13. Do not skip the required six demonstration scenarios.
14. Do not combine all backend code into one file.
15. Do not generate incomplete or inconsistent code.
16. Do not move ahead without my confirmation at each phase.
17. Use exact commands for Windows PowerShell and PyCharm.
18. Explain the complete workflow, including how frontend, backend, database, and AI communicate.

The project should be clean, maintainable, secure, and understandable enough for me to explain during a technical review or project demonstration.

---

# 23. EXPECTED FIRST RESPONSE

Start with **PHASE 1 – PROJECT SETUP**.

In your first response:

1. Briefly explain the final architecture.
2. Show the complete high-level project folder structure.
3. Tell me where to create the project.
4. Give exact PowerShell commands for the backend setup.
5. Create the initial requirements.txt.
6. Create the initial FastAPI application.
7. Implement a root endpoint and health-check endpoint.
8. Explain each file and command.
9. Show how to run the backend.
10. Show how to test the endpoints in the browser and Swagger.

Do not start PostgreSQL integration or frontend development yet.

Wait for my confirmation that Phase 1 works before proceeding.

**FINAL EXPECTATION: Build a complete, functional Employee Helpdesk application with two role-based portals, PostgreSQL persistence, FastAPI backend, React frontend, local AI-powered ticket analysis, human-in-the-loop decisions, comprehensive testing, and professional documentation.**

---

## Initial backend scaffold

The backend scaffold is in `backend/`. The FastAPI app currently provides
`GET /` and `GET /health`. The additional modules, migration setup, seed script,
and test modules establish locations for future implementation; their presence
does not mean those features are implemented yet.

```text
backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── ticket.py
│   │   ├── ticket_activity.py
│   │   ├── ai_suggestion.py
│   │   └── ai_feedback.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── ticket.py
│   │   ├── activity.py
│   │   ├── ai.py
│   │   └── feedback.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── tickets.py
│   │   ├── activities.py
│   │   ├── ai.py
│   │   ├── feedback.py
│   │   └── dashboard.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   ├── ticket_service.py
│   │   ├── ai_service.py
│   │   ├── feedback_service.py
│   │   └── dashboard_service.py
│   ├── dependencies/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── permissions.py
│   └── utils/
│       ├── __init__.py
│       ├── security.py
│       └── logging_config.py
├── alembic/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
├── scripts/
│   └── seed_data.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_health.py
│   ├── test_auth.py
│   ├── test_tickets.py
│   ├── test_activities.py
│   ├── test_ai.py
│   ├── test_feedback.py
│   └── test_dashboard.py
├── .env
├── .env.example
├── .gitignore
├── .python-version
├── alembic.ini
├── requirements.in
└── requirements.txt
```

Use Python 3.14.x, matching `backend/.python-version` and the dependency lock.
From the repository root in PowerShell:

```powershell
cd backend
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --require-hashes -r requirements.txt
Copy-Item .env.example .env
python -m uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/`, `http://127.0.0.1:8000/health`, or the
interactive API docs at `http://127.0.0.1:8000/docs`. Run the initial tests from
`backend/` with `python -m pytest -q`.

`requirements.in` contains the direct dependency ranges. `requirements.txt` is
the generated, hash-pinned lockfile used for installs. To intentionally update
dependencies, install the lock-generation tool in your development environment
with `python -m pip install pip-tools==7.7.0`, then run
`pip-compile --generate-hashes --output-file requirements.txt requirements.in`
from `backend/`. Review and test the resulting lockfile before committing it.
The dependency list uses plain Uvicorn instead of its optional `standard`
extras so the generated lock does not omit platform-specific extras when
compiled on one operating system; Uvicorn's built-in `--reload` remains
available.
CI verifies the locked install and tests on Windows, Linux, and macOS.

The `.env` file is local-only and ignored by Git. Set `DATABASE_URL` to a
working PostgreSQL connection before adding database-backed features, and
replace `SECRET_KEY` with a securely generated value before enabling
authentication. The initial liveness endpoint does not connect to PostgreSQL.
PostgreSQL and Ollama are separate services; their required versions and
availability must be set up separately when those integrations are implemented.

## Collaborator setup (Windows PowerShell)

Follow these steps for a clean, consistent backend setup. The project pins
Python to the 3.14 minor release in `backend/.python-version` and commits a
hash-locked dependency file. Do not install backend packages globally or use a
different Python version for this project.

### 1. Install and verify Python

Install Python 3.14 (64-bit) and the Python launcher if they are not already
installed. Open a new PowerShell window and verify the launcher can find it:

```powershell
py -3.14 --version
```

The output must start with `Python 3.14.`. If the launcher cannot find Python
3.14, install it before continuing. Do not substitute another Python version;
the lock and CI are currently validated for Python 3.14.

### 2. Clone the repository

Choose a folder for your local checkout, then clone the GitHub repository:

```powershell
New-Item -ItemType Directory -Force "$HOME\source" | Out-Null
Set-Location "$HOME\source"
git clone https://github.com/joyal-pasricha-gollm/ai-employee-helpdesk.git
Set-Location .\ai-employee-helpdesk
git status
```

If you already cloned the repository, open PowerShell in that checkout and
update your local `main` before creating a work branch:

```powershell
git switch main
git pull --ff-only origin main
```

### 3. Create an isolated backend environment

Run these commands from the repository root. Each collaborator should create
their own virtual environment; do not copy or share `.venv` between machines.

```powershell
py -3.14 -m venv backend\.venv
```

Install dependencies using the committed lock file and verify the environment:

```powershell
backend\.venv\Scripts\python.exe -m pip install --require-hashes -r backend\requirements.txt
backend\.venv\Scripts\python.exe -m pip check
```

`--require-hashes` makes pip verify package artifacts against the hashes in the
lock. If installation fails, confirm that you are using Python 3.14 and that
your network or package index allows access to PyPI; do not work around the
failure by installing unpinned packages. Share the complete error with the
team and fix the shared lock or setup instructions through a reviewed change.

### 4. Set up local configuration

Create your own ignored `.env` file from the example. This command preserves an
existing local `.env`:

```powershell
if (-not (Test-Path backend\.env)) {
    Copy-Item backend\.env.example backend\.env
}
```

Never commit `.env`, passwords, tokens, or machine-specific settings. Only
update `.env.example` with safe placeholder values when the team agrees on new
configuration requirements. PostgreSQL and Ollama are separate services; the
current health-only backend does not need them running, but future database and
AI features will need their setup documented here.

### 5. Run checks and start the backend

Run tests from the repository root:

```powershell
backend\.venv\Scripts\python.exe -m pytest -q backend\tests
```

Start the development server:

```powershell
backend\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --app-dir backend
```

In a browser, check:

- `http://127.0.0.1:8000/` — API welcome response
- `http://127.0.0.1:8000/health` — health response
- `http://127.0.0.1:8000/docs` — interactive OpenAPI documentation

Stop the server with `Ctrl+C`.

### 6. Work without overwriting collaborators

Create a separate branch for each task. Do not commit directly to `main`:

```powershell
git switch -c feature/short-task-name
```

Before starting work and before opening a pull request, sync with the latest
`main` and run the checks again:

```powershell
git fetch origin
git merge origin/main
backend\.venv\Scripts\python.exe -m pip check
backend\.venv\Scripts\python.exe -m pytest -q backend\tests
git status
```

Commit only the files for your task, push your branch, and open a pull request
for review:

```powershell
git add path\to\your\changed-file
git diff --cached --check
git diff --cached
git commit -m "Describe the change"
git push -u origin feature/short-task-name
```

Do not stage `.env`, `.venv`, local database files, or the assessment PDF.
Coordinate database model and Alembic migration changes with the team; avoid
editing the same migration or shared API schema in parallel without agreement.

### 7. Updating dependencies (maintainers)

Do not independently upgrade packages or edit generated pins by hand. To
intentionally change dependencies, start from the agreed Python 3.14
environment, update `backend/requirements.in`, then regenerate and test the
lock:

```powershell
Set-Location backend
.\.venv\Scripts\python.exe -m pip install pip-tools==7.7.0
.\.venv\Scripts\python.exe -m piptools compile --generate-hashes --output-file requirements.txt requirements.in
.\.venv\Scripts\python.exe -m pip install --require-hashes -r requirements.txt
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m pytest -q
Set-Location ..
git diff -- backend\requirements.in backend\requirements.txt
```

Include both dependency files in the same reviewed pull request. CI also checks
the locked install, dependency consistency, and tests on Windows, Linux, and
macOS. These safeguards reduce Python dependency drift; they cannot guarantee
that unrelated local services (PostgreSQL or Ollama) are configured identically.

---

# Modules 2, 6, 7, 8 – Login, AI Suggestions and AI Feedback (end-to-end test guide)

This section explains, from zero, what these parts of the backend do and how to
prove they work using Swagger (the API test page), the real database and the
local AI. Every step shows what to type, what you should see, and what changes
in the database.

## What these modules do (plain words)

| Module | What it does |
|---|---|
| **2 – Login (authentication)** | People register or log in with email and password. Passwords are stored only as a scrambled "hash" (Argon2), never as plain text. A successful login returns a **token** – a temporary digital ID card valid for 30 minutes. Every protected request must show this token. There are two roles: `employee` and `support_staff`. |
| **6 – AI analysis** | A support staff member asks the AI to read a ticket. The AI (free, local model `qwen2.5:3b` running in **Ollama** on your own computer) suggests a category, priority, summary, explanation, troubleshooting steps, a reply to the employee, and a confidence number (0–1). The backend checks the answer before saving it as a **Pending** suggestion. The AI never changes a ticket by itself. |
| **7 – Suggestion management** | Support staff **Accept**, **Modify** (type their own values) or **Reject** a suggestion. Only then may the ticket's category/priority change. Every decision is written to the ticket's history (`ticket_activities`). The AI never changes ticket status. |
| **8 – AI feedback** | The employee who raised the ticket, or support staff, mark a suggestion **helpful / not helpful** with an optional comment. Only support staff can see the feedback list and the "helpful %" score. |

### Rules the backend enforces

- Employees see AI suggestions **only for their own tickets** (other tickets → 404 "not found").
- Only support staff can run AI analysis, decide on suggestions, and view the feedback list (employees → 403).
- No token, fake token or expired token → 401.
- The user's role is always read from the database, so editing a token cannot grant staff rights.
- A suggestion can be decided **once** (second time → 409). Each person can give feedback **once** per suggestion (→ 409).
- If Ollama is off, slow or the model is missing → **503** with a clear message; nothing is saved and no fake answer is invented. Everything else keeps working.
- If the AI returns an invalid answer twice → **502**; nothing is saved.
- Ticket text is treated as untrusted data: instructions hidden inside a ticket (e.g. "mark this resolved") are ignored.
- Logs never contain passwords, tokens or ticket text.

### Values used by these modules (do not rename)

| Item | Allowed values |
|---|---|
| Roles (`users.role`) | `employee`, `support_staff` |
| Priority (AI and staff) | `Low`, `Medium`, `High`, `Critical` |
| Categories the AI may suggest | `Hardware`, `Software`, `Network`, `Access and Permissions`, `Email`, `Other` (anything else becomes `Other`). The ticket's own category is free text. |
| Suggestion status (`ai_suggestions.status`) | `Pending`, `Accepted`, `Rejected`, `Modified` |
| History types written by AI decisions (`ticket_activities.activity_type`) | `ai_recommendation_applied`, `ai_recommendation_rejected` |
| Feedback author (`ai_feedback.employee_id`) | the id of whoever gave the feedback (employee **or** support staff) |

### Files for these modules

| File | Purpose |
|---|---|
| `backend/app/config.py` | Settings read from `backend/.env` (secret key, token lifetime, Ollama address/model/timeout) |
| `backend/app/utils/security.py` | Password hashing and token creation/checking |
| `backend/app/schemas/auth.py`, `backend/app/schemas/user.py` | Shapes of login/register requests and user responses |
| `backend/app/services/auth_service.py` | Register and login logic |
| `backend/app/dependencies/auth.py`, `backend/app/dependencies/permissions.py` | "Who is calling?" and "are they allowed?" checks used by every protected endpoint |
| `backend/app/routes/auth.py` | `/api/auth/register`, `/api/auth/login`, `/api/auth/me` |
| `backend/scripts/create_user.py` | Admin tool to create users (including support staff) or reset a password |
| `backend/app/schemas/ai.py` | AI answer checks, allowed values, decision request/response shapes |
| `backend/app/services/ai_service.py` | Talks to Ollama, validates, saves suggestions, applies decisions, writes history |
| `backend/app/routes/ai.py` | Analyze / view suggestions / decision endpoints |
| `backend/app/schemas/feedback.py`, `backend/app/services/feedback_service.py`, `backend/app/routes/feedback.py` | Feedback endpoints and helpful % |
| `backend/tests/test_auth.py`, `backend/tests/test_ai.py`, `backend/tests/test_feedback.py` | Automated tests (AI is faked, so Ollama is not needed) |

### Endpoints

| Method and path | Who can call it | Purpose |
|---|---|---|
| `POST /api/auth/register` | anyone | Create an **employee** account (staff cannot self-register) |
| `POST /api/auth/login` | anyone | Get a token |
| `GET /api/auth/me` | logged in | Show who you are |
| `POST /api/tickets/{ticket_id}/analyze` | support staff | Ask the AI to analyze a ticket |
| `GET /api/tickets/{ticket_id}/ai-suggestions` | support staff, or the employee who owns the ticket | List the ticket's suggestions (newest first) |
| `PATCH /api/ai-suggestions/{suggestion_id}/decision` | support staff | Accept / Modify / Reject |
| `POST /api/ai-suggestions/{suggestion_id}/feedback` | ticket's employee or support staff | Helpful / not helpful + comment |
| `GET /api/ai-feedback` | support staff | All feedback + helpful % |

---

## Part A – One-time setup

All commands are typed in **VS Code → Terminal → New Terminal** (PowerShell), starting in the project folder. First complete the "Collaborator setup" section above (Python 3.14 virtual environment and `pip install`).

### A1. Install the local AI

1. Download and install Ollama from https://ollama.com (it runs in the Windows system tray).
2. Download the model (about 1.9 GB, one time):
   ```
   ollama pull qwen2.5:3b
   ```
   Expected last line: `success`
3. Check:
   ```
   ollama list
   ```
   Expected: a row starting with `qwen2.5:3b`.

### A2. Settings file `backend\.env`

Copy `backend\.env.example` to `backend\.env` (never commit `.env`) and make sure it contains:

```
DATABASE_URL=<the team's Supabase connection string>
SECRET_KEY=<any random text of at least 32 characters>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:3b
OLLAMA_TIMEOUT_SECONDS=120
```

To generate a SECRET_KEY:
```
backend\.venv\Scripts\python.exe -c "import secrets; print(secrets.token_urlsafe(48))"
```

> **Important (VS Code):** this project's VS Code settings copy `.env` into a terminal **when the terminal is opened**. After changing `.env`, close all terminals (trash-can icon) and open a new one, otherwise the server keeps the old values.

### A3. Create the demo accounts

The sample users already in the database have placeholder passwords and cannot log in until a real password is set. Support staff accounts can only be created with this admin script (there is no public sign-up for staff). The script asks for the password twice (typing is hidden).

```
cd backend
.\.venv\Scripts\python.exe -m scripts.create_user --email arjun@example.com --full-name "Arjun Mehta" --role support_staff
.\.venv\Scripts\python.exe -m scripts.create_user --email rahul@helpdesk.com
```

Expected output:
```
Created user id=22 email=arjun@example.com role=support_staff        (or "Updated password for ..." if he already exists)
Updated password for user id=1 email=rahul@helpdesk.com role=employee
```

This guide calls the passwords you chose `<STAFF_PASSWORD>` and `<EMPLOYEE_PASSWORD>`.
Rahul Sharma (user id 1) is used because he owns sample tickets **1, 3 and 5**; ticket **2** belongs to Priya (user id 2).

**Database change:** `users.password_hash` (and `updated_at`) for these two users.

---

## Part B – Automated tests (no AI needed)

```
cd backend
.\.venv\Scripts\python.exe -m pytest -q
```

Expected: `45 passed` (plus 1 harmless warning). These tests use a fake AI and leave no data behind (each test is undone automatically).

---

## Part C – Start the server

```
cd backend
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Expected: `Application startup complete.`
Open **http://127.0.0.1:8000/docs** in a browser – this is Swagger.

**How to call an endpoint in Swagger:** click the row → **Try it out** → fill the fields / paste the body (delete old text first) → **Execute** → read **Server response** (Code and Response body).

**How to log in inside Swagger:** after a login call, copy the `access_token` value (without quotes) → click the green **Authorize 🔒** button at the top → paste into **Value** (do not type "Bearer") → **Authorize** → **Close**. To switch user: **Authorize → Logout → Close**, then log in as the other person. Tokens expire after 30 minutes (you will get 401 – just log in again).

> Steps C3–C16 create real rows in the shared database. Suggestion numbers are given by the database, so this guide calls them **N1** and **N2** – write down the real numbers you get.

### C1. Register a new employee (module 2)

`POST /api/auth/register`
```json
{"full_name": "Test Employee", "email": "test.employee1@example.com", "password": "TestPass123"}
```
Expected **201**:
```json
{"id": <number>, "full_name": "Test Employee", "email": "test.employee1@example.com", "role": "employee", "created_at": "...", "updated_at": "..."}
```
- No password or hash is ever returned.
- Run it again → **409** `"An account with this email already exists"` (also with the email in CAPITALS).
- Body with `"password": "short"` → **422**. Body with `"email": "not-an-email"` → **422**.
- Adding `"role": "support_staff"` to the body is ignored – the account is still `employee`.

**Database change:** one new row in `users` with `role = employee` and an Argon2 `password_hash` (starts with `$argon2`).

### C2. Login checks (module 2)

`POST /api/auth/login`

| Body | Expected |
|---|---|
| `{"email": "arjun@example.com", "password": "<STAFF_PASSWORD>"}` | **200**, `"token_type": "bearer"`, `"user": {"id": 22, "role": "support_staff", ...}` |
| `{"email": "arjun@example.com", "password": "wrong-password"}` | **401** `"Incorrect email or password"` |
| `{"email": "nobody@example.com", "password": "whatever123"}` | **401** with the **same** message (so nobody can discover which emails exist) |
| `{"email": "arjun@example.com"}` | **422** (password missing) |

Now log in as Arjun (first row) and **Authorize** with his token.

`GET /api/auth/me` → **200** with Arjun's details. After **Logout** → **401** `"Not authenticated"`. With token value `abc.def.ghi` → **401** `"Invalid or expired token"`. Log back in as Arjun and Authorize.

**Database change:** none (logins only read).

### C3. AI analysis of ticket 1 (module 6) – as Arjun

Check Ollama is idle first (second terminal): `ollama ps` → only headings, no rows.

`POST /api/tickets/{ticket_id}/analyze` with `ticket_id` = `1` → click **Execute once** and wait 20–90 seconds.

Expected **201** (wording varies – it is the AI's own text):
```json
{
  "id": N1, "ticket_id": 1,
  "suggested_category": "Hardware", "suggested_priority": "Medium",
  "summary": "Employee laptop fails to turn on after pressing the power button.",
  "explanation": "...", "suggested_response": "...",
  "troubleshooting_steps": ["...", "..."],
  "confidence": 0.9, "model_name": "qwen2.5:3b", "status": "Pending", "created_at": "..."
}
```

Proof the real AI answered:
- `ollama ps` now shows a `qwen2.5:3b` row.
- The uvicorn window shows:
  ```
  INFO app.services.ai_service: AI analysis started: ticket_id=1 actor_id=22 model=qwen2.5:3b
  INFO httpx: HTTP Request: POST http://localhost:11434/api/chat "HTTP/1.1 200 OK"
  INFO app.services.ai_service: AI suggestion saved: suggestion_id=N1 ticket_id=1 seconds=34.7
  ```
- The ticket itself is **not** changed (still its old category/priority).
- `confidence` is the AI's own guess, not a measured accuracy.

**Database change:** one new row in `ai_suggestions` (ticket_id 1, status `Pending`, model_name `qwen2.5:3b`). `tickets` unchanged.

### C4. AI analysis of ticket 3

Same endpoint, `ticket_id` = `3` → **201**, text about a VPN connection, category `Network`. Write down its id as **N2**.

**Database change:** one new `ai_suggestions` row for ticket 3.

### C5. View suggestions (module 7)

`GET /api/tickets/{ticket_id}/ai-suggestions`, `ticket_id` = `1` → **200**, a list, newest first, including N1. Older suggestions are kept for history.

### C6. Invalid decisions are refused

`PATCH /api/ai-suggestions/{suggestion_id}/decision`, `suggestion_id` = **N1**:

| Body | Expected |
|---|---|
| `{"decision": "Modified"}` | **422** "Modified needs final_category and/or final_priority" |
| `{"decision": "Modified", "final_priority": "Urgent"}` | **422** (must be Low/Medium/High/Critical) |
| `{"decision": "Maybe"}` | **422** |
| `{"decision": "Accepted", "final_priority": "High"}` | **422** (final values only with Modified) |

**Database change:** none.

### C7. Modify (human corrects the AI)

Same endpoint, `suggestion_id` = **N1**:
```json
{"decision": "Modified", "final_category": "Laptop Power", "final_priority": "High", "note": "Checked with employee"}
```
Expected **200**:
```json
{"suggestion": {"id": N1, "suggested_category": "Hardware", "suggested_priority": "Medium", "status": "Modified", ...},
 "ticket_id": 1, "ticket_category": "Laptop Power", "ticket_priority": "High", "activities_recorded": 2}
```
(`activities_recorded` is 1 per field that really changed; if the ticket already had these values you get 1 row saying so.)

Execute again → **409** `"This suggestion was already decided (status: Modified)"`.

**Database changes:**
- `ai_suggestions` row N1: `status` → `Modified` (the AI's own values are kept).
- `tickets` row 1: `category` → `Laptop Power`, `priority` → `High`, `updated_at` → now. **`status` is not touched.**
- `ticket_activities`: new rows, e.g.
  | ticket_id | actor_id | activity_type | old_value | new_value | comment |
  |---|---|---|---|---|---|
  | 1 | 22 | ai_recommendation_applied | (previous category, e.g. Hardware) | Laptop Power | Category set from AI suggestion #N1 (modified). Note: Checked with employee |
  | 1 | 22 | ai_recommendation_applied | (previous priority, e.g. Critical) | High | Priority set from AI suggestion #N1 (modified). Note: Checked with employee |

  (A row is written only for a value that actually changed.)

### C8. Reject

`suggestion_id` = **N2**:
```json
{"decision": "Rejected", "note": "Not correct"}
```
Expected **200**, `"suggestion": {"status": "Rejected"}`, ticket 3 values unchanged, `"activities_recorded": 1`.

**Database changes:** N2 `status` → `Rejected`; one `ticket_activities` row `ai_recommendation_rejected` with comment "AI suggestion #N2 rejected; ticket unchanged. Note: Not correct". `tickets` row 3 unchanged.

### C9. Accept (optional)

Analyze ticket 5 (as in C3) → note id **N3**, then decision:
```json
{"decision": "Accepted", "apply_category": false}
```
Expected **200**: only the priority is copied from the AI; the category stays. Use `{"decision": "Accepted"}` to copy both.

### C10. Missing records

`POST /api/tickets/999999/analyze` → **404** `"Ticket not found"` (instant, no AI call).
`PATCH /api/ai-suggestions/999999/decision` → **404** `"AI suggestion not found"`.

### C11. Staff feedback (module 8)

`POST /api/ai-suggestions/{suggestion_id}/feedback`, `suggestion_id` = **N1**:
```json
{"is_helpful": false, "feedback_comment": "Category too generic"}
```
Expected **201**: `{"id": ..., "suggestion_id": N1, "employee_id": 22, "is_helpful": false, "feedback_comment": "Category too generic", "created_at": "..."}`.
Execute again → **409** `"You have already given feedback on this suggestion"`.

**Database change:** one new `ai_feedback` row (`employee_id` = 22 = the staff member who gave it).

### C12. Switch to the employee (Rahul)

**Authorize → Logout → Close**. `POST /api/auth/login`:
```json
{"email": "rahul@helpdesk.com", "password": "<EMPLOYEE_PASSWORD>"}
```
Expected **200**, `"user": {"id": 1, "role": "employee"}`. Authorize with this token.

### C13. What the employee can and cannot do

| Call | Input | Expected | Why |
|---|---|---|---|
| `GET /api/tickets/{ticket_id}/ai-suggestions` | `1` | **200** list | his own ticket |
| same | `2` | **404** | Priya's ticket is hidden |
| `POST /api/tickets/{ticket_id}/analyze` | `1` | **403** | staff only |
| `PATCH /api/ai-suggestions/{suggestion_id}/decision` | N2, `{"decision": "Accepted"}` | **403** | staff only |
| `POST /api/ai-suggestions/{suggestion_id}/feedback` | N1, `{"is_helpful": true, "feedback_comment": "Useful steps"}` | **201**, `"employee_id": 1` | his own ticket |
| same again | same | **409** | one feedback per person |
| `GET /api/ai-feedback` | – | **403** | staff only |

**Database change:** one new `ai_feedback` row with `employee_id` = 1.

### C14. Staff feedback report

Log in again as Arjun and Authorize. `GET /api/ai-feedback` → **200**:
```json
{"total": <all feedback>, "helpful_count": ..., "not_helpful_count": ..., "helpful_percentage": ...,
 "items": [{"given_by_name": "Rahul Sharma", "given_by_role": "employee", "is_helpful": true, "ticket_id": 1, "ticket_subject": "Laptop not starting", "suggested_category": "...", "suggestion_status": "Modified", ...}, ...]}
```
`helpful_percentage` = helpful ÷ total × 100 (one decimal), over all feedback in the database.

### C15. AI switched off (failure handling)

1. Right-click the Ollama tray icon → **Quit Ollama**.
2. `POST /api/tickets/5/analyze` → **503** `"The AI service is not reachable. Make sure Ollama is running."` The uvicorn window shows `WARNING ... AI analysis failed: ticket_id=5 error=AIServiceUnavailableError`.
3. `GET /api/tickets/5/ai-suggestions` → no new suggestion was added. `GET /api/auth/me` → still **200** (the rest of the app works).
4. Start Ollama again from the Start menu (the first AI request afterwards takes about a minute while the model loads).

**Database change:** none.

### C16. Check the database

In the Supabase **SQL Editor** (or pgAdmin), run:

```sql
-- AI suggestions and their decisions
select id, ticket_id, suggested_category, suggested_priority, status, model_name, confidence, created_at
from ai_suggestions order by id;

-- Ticket history written by AI decisions
select ticket_id, actor_id, activity_type, old_value, new_value, comment, created_at
from ticket_activities where activity_type like 'ai_%' order by id;

-- Ticket values after decisions (status must be unchanged)
select id, category, priority, status, updated_at from tickets where id in (1, 3, 5) order by id;

-- Feedback with who gave it
select f.id, f.suggestion_id, u.full_name, u.role, f.is_helpful, f.feedback_comment, f.created_at
from ai_feedback f join users u on u.id = f.employee_id order by f.id;
```

Expected: N1 `Modified`, N2 `Rejected`; `ai_recommendation_applied` rows for ticket 1 and an `ai_recommendation_rejected` row for ticket 3, all with `actor_id` 22; ticket 1 shows your Modify values and its original `status`; ticket 3 unchanged; your two feedback rows (support_staff and employee).

To put sample ticket 1 back afterwards: `update tickets set category = 'Hardware', priority = 'High' where id = 1;` (history rows are kept on purpose – history is never deleted).

---

## Troubleshooting

| You see | Meaning | Fix |
|---|---|---|
| 503 `The AI model 'llama3.2' is not installed` | Server is using old settings | Fix `OLLAMA_MODEL` in `.env`, close **all** terminals, open a new one, restart uvicorn |
| 503 `The AI service is not reachable` | Ollama is not running | Start Ollama, wait ~10 s |
| 503 `took too long to respond` | Slow first load | Try again, or raise `OLLAMA_TIMEOUT_SECONDS` |
| 502 `The AI returned an invalid answer` | AI answered badly twice | Try again; nothing was saved |
| 401 | Not logged in / token expired (30 min) | Log in again and Authorize |
| 403 | Wrong role (e.g. employee on a staff endpoint) | Authorize with a support_staff token |
| 404 on someone else's ticket | Employees only see their own tickets | Expected behaviour |
| 409 | Already decided / feedback already given | Expected – analyze again to get a new suggestion |
| 422 | Input not valid | Read the message; clear old text from the body box |
| `Failed to fetch` in Swagger | Server not running | Start uvicorn (Part C) |
