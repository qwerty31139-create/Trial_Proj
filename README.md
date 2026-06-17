# Stakeholder Requirements to ADO Artifacts System

A comprehensive system that converts natural language stakeholder requirements into structured engineering artifacts and automatically integrates them into **Azure DevOps (ADO)**.

---

## 🧭 1. Define Scope & Target Outputs

### ✅ Input
- Natural language stakeholder requirements (emails, docs, meetings, tickets)
- Unstructured feedback and specifications

### ✅ Output (target artifacts)
- **Epics** — High-level business initiatives
- **Features** — Deliverable capabilities
- **User Stories** — Actionable requirements with acceptance criteria
- **Acceptance Criteria** — Gherkin-formatted scenarios
- **Tasks/Subtasks** — Development work items
- **Test Cases** — QA validation steps
- **Architecture Diagrams** — System design (optional)
- **Code Skeletons** — Starter templates (optional)

### ✅ Mapping Example
```
Requirement → Epic → Features → User Stories → Tasks → Test Cases
```

---

## 🏗️ 2. Design the Architecture

### Core Components

#### 1. **Input Layer**
- Web UI (React/Vue)
- Teams Bot integration
- CLI tool
- Document ingestion (PDF, Word, Confluence)

#### 2. **GenAI Processing Layer**
- LLM (Azure OpenAI / GPT-4)
- Prompt templates (structured prompting)
- Orchestration logic (LangChain/LlamaIndex)

#### 3. **Structuring Layer**
- LLM output → JSON schema conversion
- Schema validation (Pydantic)
- Consistency checks

#### 4. **ADO Integration Layer**
- Azure DevOps REST API client
- Work item creation/update
- Link management (parent-child relationships)

#### 5. **Storage & Traceability**
- Database (Cosmos DB / PostgreSQL)
- Audit logs
- Version history

---

## 📁 Project Structure

```
Trial_Proj/
├── README.md (this file)
├── requirements.txt
├── .env.example
├── docker-compose.yml
├── config/
│   ├── settings.py
│   └── prompt_templates/
│       ├── epic_prompt.txt
│       ├── feature_prompt.txt
│       ├── story_prompt.txt
│       └── task_prompt.txt
├── backend/
│   ├── main.py
│   ├── api/
│   │   ├── routes.py
│   │   └── schemas.py
│   ├── services/
│   │   ├── llm_service.py
│   │   ├── structuring_service.py
│   │   ├── ado_service.py
│   │   └── storage_service.py
│   └── models/
│       ├── artifacts.py
│       └── work_items.py
├── frontend/
│   ├── index.html
│   ├── css/
│   │   └── styles.css
│   ├── js/
│   │   └── app.js
│   └── components/
│       ├── input-form.js
│       ├── preview.js
│       └── sync-status.js
├── tests/
│   ├── test_llm_service.py
│   ├── test_structuring.py
│   └── test_ado_integration.py
└── docs/
    ├── api-spec.md
    ├── deployment.md
    └── examples/
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Azure OpenAI API key
- Azure DevOps Personal Access Token (PAT)
- PostgreSQL or Cosmos DB connection string

### Installation

```bash
# 1. Clone and navigate
cd Trial_Proj

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your credentials
```

### Running the System

```bash
# Start backend server
uvicorn backend.main:app --reload --port 8000

# Frontend will be available at http://localhost:3000
```

---

## 📊 Workflow Example

### 1. **Input Phase**
```
Input: "We need to build a user authentication system with multi-factor 
authentication, supporting email, SMS, and authenticator apps."
```

### 2. **Processing Phase**
- LLM extracts entities and relationships
- Converts to structured JSON
- Validates against schema

### 3. **Output Phase**
```json
{
  "epic": {
    "title": "User Authentication & Authorization",
    "description": "Implement secure authentication system with MFA support",
    "acceptance_criteria": ["...", "..."]
  },
  "features": [
    {
      "title": "Email-based MFA",
      "user_stories": ["..."]
    },
    {
      "title": "SMS-based MFA",
      "user_stories": ["..."]
    }
  ],
  "tasks": ["...", "..."],
  "test_cases": ["...", "..."]
}
```

### 4. **Integration Phase**
- Create Epic in ADO
- Create Features as child items
- Link User Stories to Features
- Link Tasks and Test Cases
- Update traceability matrix

---

## 🔌 Azure DevOps Integration

### Supported Work Item Types
- Epic
- Feature
- User Story
- Task
- Test Case
- Bug (optional)

### Linking Strategy
```
Epic (Parent)
├── Feature 1 (Child of Epic)
│   ├── User Story 1.1 (Child of Feature)
│   │   ├── Task 1.1.1 (Child of User Story)
│   │   └── Task 1.1.2
│   │   └── Test Case 1.1.1
│   └── User Story 1.2
└── Feature 2
    └── User Story 2.1
```

---

## 🔐 Security Considerations

- Store API keys in Azure Key Vault
- Validate all LLM outputs before ADO sync
- Implement role-based access control (RBAC)
- Audit log all artifact creation/modifications
- Rate limit API calls

---

## 📈 Advanced Features (Phase 2)

- Custom prompt templates per organization
- Integration with Jira, Monday.com, Linear
- AI-powered test case generation
- Architecture diagram auto-generation
- Slack/Teams notifications
- Batch requirement processing
- Feedback loop for continuous improvement

---

## 🤝 Contributing

See [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

---

## 📝 License

MIT License - See LICENSE file

---

## 🆘 Support

For issues and questions:
- GitHub Issues: [Link]
- Documentation: [docs/](docs/)
- Email: support@example.com