# Engineering Planning Agent — Purpose, Inputs & Outputs

## What is the Agent?
The Engineering Planning Agent is the AI brain of DevProject AI.
It is powered by Claude (claude-sonnet-4-6) and acts as a **senior engineer collaborator**
that thinks through scope, architecture, risks, and sequencing before implementation starts.

---

## Purpose
Convert a rough product requirement into a structured, implementation-ready engineering plan.

Instead of:
> "Add JWT authentication"

You get a full plan covering architecture, API design, data models, risks, and step-by-step tasks.

---

## What it specialises in
- Requirement analysis
- Scope definition
- Architecture planning
- API contract drafting
- Task decomposition
- Risk review
- Implementation sequencing

---

## Sample Input

```json
{
  "requirement": "Add JWT authentication to this FastAPI project"
}
```

With MCP context:
```json
{
  "requirement": "Add JWT authentication to this FastAPI project",
  "directory": "https://github.com/Shine-23/agentic-ai-hands-on",
  "sources": ["https://fastapi.tiangolo.com"],
  "commands": ["pip list"]
}
```

---

## Sample Output

```json
{
  "requirement_summary": "Add stateless JWT-based authentication to an existing FastAPI project. All /plan/* endpoints will be protected. Users register with username/email/password and receive a bearer token on login.",

  "clarifying_questions": [
    "Should all existing /plan endpoints require authentication?",
    "Do you need refresh token support or is access token only acceptable for MVP?",
    "Should user registration be open or invite-only?"
  ],

  "assumptions": [
    "JWT token only (no refresh token) is acceptable for MVP",
    "All existing /plan/* endpoints should be protected",
    "Access tokens expire after 24 hours",
    "Password hashing will use passlib with bcrypt"
  ],

  "suggested_mvp_scope": [
    "User model with id, username, email, hashed_password",
    "POST /auth/register — open registration",
    "POST /auth/login — returns JWT access token",
    "GET /auth/me — returns current user info",
    "Protect all /plan/* endpoints with JWT dependency"
  ],

  "proposed_architecture": [
    "Database: PostgreSQL with SQLAlchemy ORM",
    "Auth library: python-jose[cryptography] for JWT",
    "Password hashing: passlib[bcrypt]",
    "Dependency injection: FastAPI Depends(get_current_user)",
    "New module: app/auth/ with routes, schemas, service, dependencies"
  ],

  "data_model_entities": [
    "User: id, username (unique), email (unique), hashed_password, is_active, created_at"
  ],

  "api_draft": [
    "POST /auth/register — Body: {username, email, password} → {user_id, username, email}",
    "POST /auth/login — Body: {username, password} → {access_token, token_type}",
    "GET /auth/me — Header: Authorization: Bearer <token> → {user_id, username, email}"
  ],

  "implementation_plan": [
    "Phase 1: Install python-jose, passlib, sqlalchemy, alembic",
    "Phase 2: Add JWT_SECRET_KEY and DATABASE_URL to .env and config.py",
    "Phase 3: Create app/db/models.py with User model",
    "Phase 4: Run Alembic migration to create users table",
    "Phase 5: Create app/auth/service.py with hash_password, create_access_token, get_user",
    "Phase 6: Create app/auth/dependencies.py with get_current_user()",
    "Phase 7: Create app/auth/routes.py with /register, /login, /me",
    "Phase 8: Add Depends(get_current_user) to all /plan routes"
  ],

  "risks_and_dependencies": [
    "JWT_SECRET_KEY must be strong and never committed to version control",
    "Adding auth is a breaking change — existing API consumers will need tokens",
    "No rate limiting on login endpoint — vulnerable to brute force",
    "No email verification in MVP — email addresses are not validated"
  ],

  "recommended_next_steps": [
    "Generate a strong JWT secret: openssl rand -hex 32",
    "Set up PostgreSQL locally and add DATABASE_URL to .env",
    "Install dependencies: python-jose[cryptography] passlib[bcrypt] sqlalchemy alembic",
    "Create User model and run Alembic migration",
    "Implement auth routes and protect /plan endpoints",
    "Test full auth flow before deployment"
  ]
}
```

---

## Default Stack the Agent assumes
| Layer | Default |
|-------|---------|
| Backend | FastAPI (Python) |
| AI | Claude API |
| Database | PostgreSQL |
| Auth | JWT |
| Frontend | Plain HTML / CSS / JS |
| Deployment | Docker + Railway |

---

## Working Style
- Practical and implementation-focused
- Makes assumptions explicit (never hides them)
- Identifies ambiguity instead of guessing
- Outputs structured JSON ready to convert into tickets or docs
- When MCP context is provided — inspects real code and docs before recommending
- When repo or doc context is provided — the plan is grounded in that specific codebase, not in any assumed project identity
