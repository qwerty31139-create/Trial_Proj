# Examples

Practical examples for using the Requirements to ADO Artifacts System.

## Example 1: Simple Feature Processing

### Requirement
```
"We need a user profile page that displays name, email, and avatar. 
Users should be able to edit their information and save changes."
```

### API Call
```bash
curl -X POST http://localhost:8000/api/v1/process-requirement \
  -H "Content-Type: application/json" \
  -d '{
    "requirement": "We need a user profile page that displays name, email, and avatar. Users should be able to edit their information and save changes.",
    "include_architecture_diagram": false
  }'
```

### Generated Artifacts
- **Epic:** User Profile Management
- **Features:** 
  - Display User Profile
  - Edit User Information
- **User Stories:**
  - User views their profile
  - User edits profile information
  - User saves changes
- **Tasks:**
  - Create profile UI component
  - Implement profile API endpoint
  - Add form validation
  - Write unit tests

---

## Example 2: Complex E-Commerce System

### Requirement
```
"Build a complete e-commerce platform with:
- Product catalog with search and filtering
- Shopping cart with persistent storage
- Secure checkout with multiple payment methods
- Order tracking and history
- User reviews and ratings"
```

### Processing with Auto-Sync to ADO

```bash
curl -X POST http://localhost:8000/api/v1/process-and-sync \
  -H "Content-Type: application/json" \
  -d '{
    "requirement": "Build a complete e-commerce platform with: Product catalog with search and filtering, Shopping cart with persistent storage, Secure checkout with multiple payment methods, Order tracking and history, User reviews and ratings",
    "auto_sync": true,
    "assign_to_team": "Platform Team"
  }'
```

### Expected Response
```json
{
  "processing_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "artifacts": {
    "epic": {
      "id": "epic_1",
      "title": "E-Commerce Platform",
      "description": "Complete online marketplace with catalog, cart, checkout, tracking, and reviews",
      "business_value": "New revenue stream, customer engagement",
      "priority": "High",
      "estimated_effort": "Large",
      "success_criteria": [
        "Support 1000+ products",
        "Process payments securely",
        "Order tracking in real-time"
      ]
    },
    "features": [
      {
        "id": "feature_1",
        "title": "Product Catalog & Search",
        "estimated_story_points": 13,
        "priority": "High"
      },
      {
        "id": "feature_2",
        "title": "Shopping Cart",
        "estimated_story_points": 8,
        "priority": "High"
      },
      {
        "id": "feature_3",
        "title": "Checkout & Payment",
        "estimated_story_points": 13,
        "priority": "Critical"
      },
      {
        "id": "feature_4",
        "title": "Order Tracking",
        "estimated_story_points": 8,
        "priority": "High"
      },
      {
        "id": "feature_5",
        "title": "Reviews & Ratings",
        "estimated_story_points": 5,
        "priority": "Medium"
      }
    ],
    "user_stories": [
      {
        "id": "story_1",
        "title": "User searches for products",
        "as_a": "customer",
        "i_want": "to search and filter products",
        "so_that": "I can find what I need quickly",
        "story_points": 5,
        "feature_id": "feature_1"
      },
      {
        "id": "story_2",
        "title": "User adds items to cart",
        "as_a": "customer",
        "i_want": "to add products to my cart",
        "so_that": "I can purchase multiple items",
        "story_points": 3,
        "feature_id": "feature_2"
      }
    ],
    "tasks": [
      {
        "title": "Design product database schema",
        "task_type": "Development",
        "estimated_hours": 4
      },
      {
        "title": "Implement search algorithm",
        "task_type": "Development",
        "estimated_hours": 8
      },
      {
        "title": "Create product listing UI",
        "task_type": "Development",
        "estimated_hours": 6
      }
    ],
    "test_cases": [
      {
        "title": "Search returns correct products",
        "scenario": "User searches for 'laptop'",
        "steps": [
          "1. Navigate to catalog",
          "2. Enter 'laptop' in search",
          "3. Click search"
        ],
        "expected_result": "All laptops are displayed",
        "priority": "Critical"
      }
    ]
  }
}
```

---

## Example 3: API Integration Feature

### Requirement
```
"Integrate with Stripe payment API to support:
- One-time payments
- Recurring subscriptions
- Payment refunds
- Webhook notifications for payment events"
```

### Step-by-Step Processing

```bash
# Step 1: Process requirement
curl -X POST http://localhost:8000/api/v1/process-requirement \
  -H "Content-Type: application/json" \
  -d '{
    "requirement": "Integrate with Stripe payment API to support: One-time payments, Recurring subscriptions, Payment refunds, Webhook notifications for payment events"
  }' > artifacts.json

# Step 2: Review artifacts (in artifacts.json)

# Step 3: Sync to ADO manually
curl -X POST http://localhost:8000/api/v1/sync-to-ado \
  -H "Content-Type: application/json" \
  -d '{
    "epic_id": "epic_1",
    "auto_create_links": true,
    "send_notifications": true,
    "assign_to_team": "Backend Team"
  }'
```

---

## Example 4: Data Migration Project

### Requirement
```
"Migrate legacy customer database to new cloud infrastructure:
- Export 1 million+ customer records
- Transform and validate data
- Import to new database
- Verify data integrity
- Plan rollback strategy"
```

### Generated Breakdown

The system would generate:

**Epic:** Cloud Database Migration
- **Feature 1:** Data Export & Transformation
- **Feature 2:** Cloud Import & Validation
- **Feature 3:** Data Integrity Verification
- **Feature 4:** Rollback Planning

**Sample User Stories:**
1. "As a DBA, I want to export customer records so that I can migrate to the cloud"
2. "As a data engineer, I want to validate record counts so that I ensure no data loss"
3. "As an operations manager, I want automated rollback so that I can revert if issues occur"

**Sample Tasks:**
- Design export script
- Create data validation rules
- Set up cloud database
- Implement monitoring
- Write automated tests

---

## Example 5: Polling Status

### Monitor Async Processing

```bash
# Get processing ID from response
PROCESSING_ID="550e8400-e29b-41d4-a716-446655440000"

# Poll status
while true; do
  curl http://localhost:8000/api/v1/status/$PROCESSING_ID | jq .
  sleep 2
done
```

### Status Output
```json
{
  "processing_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "processing",
  "progress_percent": 65,
  "current_step": "Generating user stories for features",
  "artifacts_count": 8,
  "ado_sync_status": "in_progress",
  "error_message": null
}
```

---

## Example 6: Batch Processing

### Process Multiple Requirements

```bash
#!/bin/bash

requirements=(
  "Build user authentication with OAuth"
  "Create admin dashboard with analytics"
  "Implement notification service"
)

for req in "${requirements[@]}"; do
  echo "Processing: $req"
  
  RESULT=$(curl -s -X POST http://localhost:8000/api/v1/process-and-sync \
    -H "Content-Type: application/json" \
    -d "{\"requirement\": \"$req\", \"auto_sync\": true}")
  
  PROCESSING_ID=$(echo $RESULT | jq -r '.processing_id')
  echo "Processing ID: $PROCESSING_ID"
done
```

---

## Example 7: Error Handling

### Handle Common Errors

```bash
# Missing requirement
curl -X POST http://localhost:8000/api/v1/process-requirement \
  -H "Content-Type: application/json" \
  -d '{}'
# Response: 400 - {"detail": "Please enter a requirement"}

# Invalid JSON
curl -X POST http://localhost:8000/api/v1/process-requirement \
  -H "Content-Type: application/json" \
  -d 'invalid json'
# Response: 400 - Request validation failed

# ADO authentication failure
# Response: 500 - {"detail": "Azure DevOps integration failed: Invalid PAT"}

# LLM rate limiting
# Response: 429 - {"detail": "Rate limit exceeded"}
```

---

## Example 8: Frontend Usage

### HTML Form Integration

```html
<form id="requirementForm">
  <textarea name="requirement" 
            placeholder="Enter your requirement..."
            required></textarea>
  
  <label>
    <input type="checkbox" name="autoSync" checked>
    Auto-sync to Azure DevOps
  </label>
  
  <button type="submit">Process Requirement</button>
</form>

<script>
document.getElementById('requirementForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  
  const formData = new FormData(e.target);
  const response = await fetch('/api/v1/process-and-sync', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      requirement: formData.get('requirement'),
      auto_sync: formData.get('autoSync') === 'on'
    })
  });
  
  const result = await response.json();
  console.log('Processing ID:', result.processing_id);
});
</script>
```

---

## Best Practices

1. **Clear Requirements:** More detailed requirements = better artifacts
2. **Batch Requests:** Process multiple related requirements together
3. **Review Before Sync:** Always review generated artifacts before ADO sync
4. **Monitor Progress:** Use status endpoint for long-running operations
5. **Error Handling:** Implement retry logic for failed sync attempts
6. **Rate Limiting:** Respect API rate limits
7. **Logging:** Keep logs of all processing operations

---

## Troubleshooting

### Issue: Empty artifacts generated

**Solution:** Provide more detailed requirements with specific examples

### Issue: Incorrect story point estimates

**Solution:** Use project-specific prompt templates

### Issue: ADO sync failures

**Solution:** Verify Azure DevOps configuration and API access

### Issue: LLM response timeouts

**Solution:** Check API quota and implement timeout handling

---

## Performance Tips

- Process similar requirements in batches
- Enable caching for frequently used prompts
- Use async processing for large requirements
- Monitor API usage and optimize queries
