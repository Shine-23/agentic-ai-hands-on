# Engineering Planning Skill — Purpose, Workflow & Outputs

## What is a Skill?
A skill is a set of instructions that tells the agent **how to behave** for a specific type of task.
The Engineering Planning skill defines the step-by-step process the agent follows when converting a requirement into a plan.

---

## Purpose
Give the agent a repeatable, structured workflow so every plan it produces is:
- Consistent in structure
- Practical and immediately actionable
- Grounded in the actual project stack

---

## Who it's for
- Solo developers
- Startup teams
- Tech leads and engineering managers
- Hackathon builders

---

## When the Skill is triggered
The skill is used when the user wants to:
- Turn a product idea into a technical plan
- Break down features into engineering tasks
- Generate architecture notes
- Draft API contracts
- Identify technical risks before coding starts
- Get a risk review before committing to a design

---

## The 9-Step Workflow

### Step 1 — Requirement Analysis
Read the input and extract:
- Product goal
- Target users
- Core features
- Constraints (time, budget, team size)
- Technical preferences

Identify missing or ambiguous information.

### Step 2 — Assumptions
State all assumptions explicitly.
Never hide uncertainty — label every assumption clearly.

### Step 3 — Scope Definition
Split into:
- **MVP scope** — must-have for first version
- **Future enhancements** — nice-to-have
- **Out of scope** — explicitly excluded

### Step 4 — Architecture Planning
Propose architecture using the default stack:
| Layer | Default |
|-------|---------|
| Frontend | Plain HTML / CSS / JS |
| Backend | FastAPI (Python) |
| AI | Claude API |
| Database | PostgreSQL |
| Auth | JWT |
| Deployment | Docker + Railway |

### Step 5 — Data & Entity Planning
Identify core data models and how they relate to the requirements.

### Step 6 — API Contract Drafting
For each major feature, draft:
- Endpoint path + HTTP method
- Request and response payloads
- Auth requirement
- Possible error cases

### Step 7 — Task Decomposition
Break implementation into:
- Milestones (logical phases)
- Tasks (concrete units of work)
- Dependencies between tasks

### Step 8 — Risk Review
Identify:
- Requirement ambiguity
- Technical unknowns
- Auth/security concerns
- Integration risks
- Scaling concerns
- Deployment risks (Docker, Railway-specific)
- Database migration risks (schema changes, data loss, rollback strategy)
- Dependency version conflicts or breaking changes

### Step 9 — Final Output
Return the structured plan in 10 sections:
1. Requirement Summary
2. Clarifying Questions
3. Assumptions
4. Suggested MVP Scope
5. Proposed Architecture
6. Data Model / Entities
7. API Draft
8. Implementation Plan
9. Risks and Dependencies
10. Recommended Next Steps

Output must be **valid JSON only** — no prose, no markdown fences, no commentary before or after.

---

## Sample Input

```
Build a bug tracking SaaS for internal engineering teams
with auth, projects, issue intake, and Slack alerts
```

## Sample Output (abbreviated)

**Clarifying Questions:**
- Single tenant or multi-tenant?
- SSO needed or username/password is enough?
- Should Slack alerts be real-time or batched?

**Assumptions:**
- PostgreSQL for database
- JWT for authentication
- Single tenant for MVP

**MVP Scope:**
- User registration and login
- Create and manage projects
- Create, assign, and close issues
- Slack webhook notification on issue creation

**Architecture:**
- Backend: FastAPI
- Database: PostgreSQL + SQLAlchemy
- Auth: JWT via python-jose
- Notifications: Slack Incoming Webhooks
- Deployment: Docker + Railway

**Data Model:**
- User: id, username, email, hashed_password
- Project: id, name, description, owner_id
- Issue: id, title, description, status, project_id, assignee_id
- Notification: id, issue_id, channel, sent_at

**API Draft:**
- POST /auth/register — create user
- POST /auth/login — return JWT
- POST /projects — create project
- GET /projects/{id}/issues — list issues
- POST /issues — create issue + trigger Slack alert

**Risks:**
- Permissions model complexity if multi-tenant is added later
- Slack webhook reliability — needs retry logic
- No rate limiting on issue creation in MVP

**Next Steps:**
- Set up PostgreSQL and create tables via SQLAlchemy
- Implement auth routes
- Build issue CRUD endpoints
- Integrate Slack webhook
- Deploy to Railway

---

## Output Quality Rules
- Be specific, not vague
- Anchor recommendations to the project stack
- Never invent repo-specific details unless codebase context is provided
- When MCP context is provided, the plan must be grounded in that codebase — not in assumed project identity
- Keep output clean and easy to convert into tickets or GitHub issues
