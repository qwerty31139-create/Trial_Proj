# API Specification

## Overview
The Requirements to ADO Artifacts System API provides endpoints to convert natural language requirements into structured engineering artifacts and sync them to Azure DevOps.

## Base URL
```
http://localhost:8000/api/v1
```

---

## Endpoints

### 1. Process Requirement

Convert a natural language requirement into structured artifacts (Epic, Features, User Stories, Tasks, Test Cases).

**Endpoint:** `POST /process-requirement`

**Request:**
```json
{
  "requirement": "We need to build a user authentication system with multi-factor authentication...",
  "epic_title": "Optional: Override auto-generated epic title",
  "include_architecture_diagram": false,
  "include_code_skeleton": false
}
```

**Response (200 OK):**
```json
{
  "epic": {
    "id": "epic_1",
    "title": "User Authentication & Authorization",
    "description": "Implement secure authentication system...",
    "priority": "High",
    "estimated_effort": "Large"
  },
  "features": [
    {
      "id": "feature_1",
      "title": "Email-based MFA",
      "description": "Multi-factor authentication via email",
      "epic_id": "epic_1",
      "story_points": 5,
      "priority": "High"
    }
  ],
  "user_stories": [
    {
      "id": "story_1",
      "title": "User receives MFA code via email",
      "as_a": "user",
      "i_want": "to receive an MFA code via email",
      "so_that": "I can verify my identity securely",
      "feature_id": "feature_1",
      "story_points": 3,
      "acceptance_criteria": [
        "Given the user is logging in, when they request MFA, then they receive an email within 30 seconds"
      ]
    }
  ],
  "tasks": [
    {
      "id": "task_1",
      "title": "Implement email service integration",
      "description": "Integrate with SendGrid or AWS SES",
      "task_type": "Development",
      "estimated_hours": 8,
      "user_story_id": "story_1"
    }
  ],
  "test_cases": [
    {
      "id": "test_1",
      "title": "Verify MFA code is sent",
      "scenario": "User logs in and requests MFA code",
      "priority": "Critical"
    }
  ]
}
```

---

### 2. Sync to Azure DevOps

Sync processed artifacts to Azure DevOps work items with proper linking.

**Endpoint:** `POST /sync-to-ado`

**Request:**
```json
{
  "epic_id": "epic_1",
  "auto_create_links": true,
  "send_notifications": true,
  "assign_to_team": "Development Team"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "epic_ado_id": 12345,
  "feature_ado_ids": [12346, 12347],
  "story_ado_ids": [12348, 12349, 12350],
  "task_ado_ids": [12351, 12352, 12353],
  "test_case_ado_ids": [12354, 12355],
  "errors": [],
  "ado_dashboard_url": "https://dev.azure.com/yourorg/project/_workitems"
}
```

---

### 3. Process and Sync Combined

Process requirement and automatically sync to ADO in one operation.

**Endpoint:** `POST /process-and-sync`

**Request:**
```json
{
  "requirement": "Natural language requirement...",
  "auto_sync": true,
  "assign_to_team": "Development Team"
}
```

**Response (200 OK):**
```json
{
  "processing_id": "uuid-here",
  "status": "completed",
  "artifacts": {
    "epic": {...},
    "features": [...],
    "user_stories": [...],
    "tasks": [...],
    "test_cases": [...]
  }
}
```

---

### 4. Get Processing Status

Poll the status of a requirement processing operation.

**Endpoint:** `GET /status/{processing_id}`

**Response (200 OK):**
```json
{
  "processing_id": "uuid-here",
  "status": "processing",
  "progress_percent": 50,
  "current_step": "Syncing to Azure DevOps",
  "artifacts_count": 12,
  "ado_sync_status": "in_progress",
  "error_message": null
}
```

**Status Values:**
- `pending` — Waiting to process
- `processing` — Currently processing
- `completed` — Successfully completed
- `failed` — Failed with error

---

### 5. Health Check

**Endpoint:** `GET /health`

**Response (200 OK):**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "components": {
    "llm": "ready",
    "ado": "ready",
    "database": "ready"
  }
}
```

---

## Data Models

### Epic
```json
{
  "id": "string",
  "title": "string",
  "description": "string",
  "business_value": "string",
  "success_criteria": ["string"],
  "estimated_effort": "Small|Medium|Large",
  "priority": "High|Medium|Low",
  "technical_tags": ["string"],
  "ado_work_item_id": "integer",
  "created_at": "datetime"
}
```

### Feature
```json
{
  "id": "string",
  "title": "string",
  "description": "string",
  "epic_id": "string",
  "acceptance_criteria": ["string"],
  "dependencies": ["string"],
  "estimated_story_points": "integer",
  "priority": "High|Medium|Low",
  "ado_work_item_id": "integer"
}
```

### User Story
```json
{
  "id": "string",
  "title": "string",
  "as_a": "string",
  "i_want": "string",
  "so_that": "string",
  "acceptance_criteria": ["string"],
  "story_points": "integer",
  "priority": "High|Medium|Low",
  "feature_id": "string",
  "ado_work_item_id": "integer"
}
```

### Task
```json
{
  "id": "string",
  "title": "string",
  "description": "string",
  "task_type": "Development|Testing|Documentation|DevOps",
  "estimated_hours": "integer",
  "user_story_id": "string",
  "dependencies": ["string"],
  "assigned_to": "string",
  "ado_work_item_id": "integer"
}
```

### Test Case
```json
{
  "id": "string",
  "title": "string",
  "scenario": "string",
  "steps": ["string"],
  "expected_result": "string",
  "priority": "High|Medium|Low",
  "user_story_id": "string",
  "ado_work_item_id": "integer"
}
```

---

## Error Handling

All errors return a JSON response with appropriate HTTP status code:

```json
{
  "detail": "Error message describing what went wrong"
}
```

**Common Status Codes:**
- `200` — Success
- `400` — Bad request (invalid input)
- `404` — Resource not found
- `500` — Server error
- `503` — Service unavailable

---

## Rate Limiting

- **Processing requests:** 10 per minute per IP
- **ADO sync requests:** 5 per minute per IP
- **Status polling:** Unlimited

---

## Authentication

Current version uses Azure DevOps PAT (Personal Access Token) stored in environment variables. Future versions will support OAuth2.

---

## Examples

### Example 1: Process Requirement Only

```bash
curl -X POST http://localhost:8000/api/v1/process-requirement \
  -H "Content-Type: application/json" \
  -d '{
    "requirement": "Build a payment processing system that accepts credit cards, PayPal, and cryptocurrency",
    "include_architecture_diagram": true
  }'
```

### Example 2: Process and Sync

```bash
curl -X POST http://localhost:8000/api/v1/process-and-sync \
  -H "Content-Type: application/json" \
  -d '{
    "requirement": "Implement real-time notifications for order status updates",
    "auto_sync": true,
    "assign_to_team": "Platform Team"
  }'
```

### Example 3: Poll Status

```bash
curl http://localhost:8000/api/v1/status/123e4567-e89b-12d3-a456-426614174000
```

---

## Webhooks (Planned)

Future release will support webhooks for:
- Artifact creation completion
- ADO sync completion
- Processing errors

---

## Changelog

### v1.0.0
- Initial release
- Basic requirement processing
- Azure DevOps integration
- Frontend UI
