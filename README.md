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
