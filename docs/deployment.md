# Deployment Guide

## Local Development

### Prerequisites
- Python 3.11+
- PostgreSQL or Cosmos DB
- Azure OpenAI API key
- Azure DevOps PAT token

### Setup

```bash
# 1. Clone repository
git clone <repo-url>
cd Trial_Proj

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your credentials

# 5. Run backend
uvicorn backend.main:app --reload --port 8000

# 6. Frontend
# Open http://localhost:3000 or serve frontend from static server
```

---

## Docker Deployment

### Build Image

```bash
docker build -t requirements-to-ado:1.0 .
```

### Run Container

```bash
docker run -p 8000:8000 \
  -e AZURE_OPENAI_API_KEY=<key> \
  -e AZURE_OPENAI_ENDPOINT=<endpoint> \
  -e ADO_ORGANIZATION=<org-url> \
  -e ADO_PAT=<pat> \
  -e DATABASE_URL=<db-url> \
  requirements-to-ado:1.0
```

### Docker Compose

```bash
docker-compose up -d
```

---

## Azure Deployment

### App Service

```bash
# 1. Create resource group
az group create --name rg-req-ado --location eastus

# 2. Create App Service Plan
az appservice plan create --name req-ado-plan \
  --resource-group rg-req-ado --sku B2

# 3. Create Web App
az webapp create --resource-group rg-req-ado \
  --plan req-ado-plan --name req-ado-app --runtime "PYTHON|3.11"

# 4. Configure deployment
az webapp deployment source config-zip \
  --resource-group rg-req-ado --name req-ado-app \
  --src app.zip
```

### Environment Variables

Set these in App Service Configuration:

- `AZURE_OPENAI_API_KEY`
- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_DEPLOYMENT_NAME`
- `ADO_ORGANIZATION`
- `ADO_PROJECT`
- `ADO_PAT`
- `DATABASE_URL`
- `ENVIRONMENT=production`

---

## Kubernetes Deployment

### Prerequisites
- kubectl configured
- Docker image pushed to registry

### Deployment YAML

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: requirements-to-ado
spec:
  replicas: 2
  selector:
    matchLabels:
      app: requirements-to-ado
  template:
    metadata:
      labels:
        app: requirements-to-ado
    spec:
      containers:
      - name: api
        image: acr.azurecr.io/requirements-to-ado:1.0
        ports:
        - containerPort: 8000
        env:
        - name: AZURE_OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: azure-secrets
              key: openai-key
        - name: ADO_PAT
          valueFrom:
            secretKeyRef:
              name: azure-secrets
              key: ado-pat
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
```

---

## Security Best Practices

1. **API Keys:** Store in Azure Key Vault
2. **Database:** Use encrypted connections (SSL/TLS)
3. **CORS:** Configure for specific domains only
4. **Rate Limiting:** Implement per IP/user
5. **Audit Logs:** Enable for all ADO operations
6. **Secrets Management:** Use Azure Managed Identity
7. **HTTPS:** Always use HTTPS in production
8. **Input Validation:** Validate all user inputs

---

## Performance Tuning

### Backend
- Enable response caching for repeated requests
- Use connection pooling for database
- Implement request batching for ADO API
- Set appropriate timeouts (default 30s)

### Frontend
- Minify CSS/JS
- Enable gzip compression
- Cache static assets
- Lazy load components

### Database
- Index frequently queried fields
- Archive old processing records
- Regular maintenance jobs

---

## Monitoring

### Key Metrics
- API response time
- Processing success rate
- LLM API usage
- ADO sync failures
- Database connection pool usage
- Memory/CPU utilization

### Alerting
- Alert on error rates > 5%
- Alert on processing time > 60s
- Alert on LLM quota exhaustion
- Alert on database connection errors

---

## Backup & Recovery

### Database Backups
```bash
# PostgreSQL
pg_dump -U user -h host database > backup.sql

# Restore
psql -U user -h host database < backup.sql
```

### Disaster Recovery Plan
- Daily automated backups
- 7-day backup retention
- RTO: 4 hours
- RPO: 1 hour

---

## Troubleshooting

### Common Issues

**1. LLM Rate Limiting**
```
Error: Rate limit exceeded for Azure OpenAI
Solution: Check API quota, implement retry logic with exponential backoff
```

**2. ADO Authentication Fails**
```
Error: Invalid Personal Access Token
Solution: Verify PAT is not expired, has correct scopes
```

**3. Database Connection Issues**
```
Error: Cannot connect to database
Solution: Check connection string, verify firewall rules
```

**4. Frontend Not Loading**
```
Error: CORS policy blocked request
Solution: Update CORS configuration in API
```

---

## Scaling Considerations

- **Horizontal:** Deploy multiple API instances behind load balancer
- **Vertical:** Increase instance resources (CPU, memory)
- **Caching:** Implement Redis for prompt templates
- **Async Processing:** Use Azure Service Bus for background jobs

---

## Maintenance

### Regular Tasks
- Monitor API logs
- Review LLM token usage
- Update dependencies
- Perform security patches
- Clean up old processing records
- Verify backup integrity

### Scheduled Maintenance
- Database optimization: Weekly
- Certificate renewal: Quarterly
- Security audit: Monthly
- Capacity planning: Quarterly
