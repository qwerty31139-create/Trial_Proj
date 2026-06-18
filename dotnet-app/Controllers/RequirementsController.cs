using System;
using System.Collections.Generic;
using Microsoft.AspNetCore.Mvc;
using dotnet_app.Models;

namespace dotnet_app.Controllers
{
    [ApiController]
    [Route("api/v1")]
    public class RequirementsController : ControllerBase
    {
        private static readonly Dictionary<string, ProcessingStatus> ProcessingStatusStore = new();

        [HttpPost("process-requirement")]
        public ActionResult<ArtifactPreview> ProcessRequirement([FromBody] ProcessRequirementRequest request)
        {
            var epic = new Epic(
                Id: Guid.NewGuid().ToString(),
                Title: request.EpicTitle ?? "User Authentication System",
                Description: "Implement secure authentication with MFA",
                BusinessValue: "Improved security and user experience",
                SuccessCriteria: new List<string> { "MFA support", "OAuth integration", "Audit logs" },
                EstimatedEffort: EffortLevel.Large,
                Priority: PriorityLevel.High,
                TechnicalTags: new List<string> { "authentication", "security" },
                CreatedAt: DateTime.UtcNow.ToString("o"),
                UpdatedAt: DateTime.UtcNow.ToString("o"),
                AdoWorkItemId: null
            );

            var feature = new Feature(
                Id: Guid.NewGuid().ToString(),
                Title: "Email-based MFA",
                Description: "Multi-factor authentication via email",
                EpicId: epic.Id,
                AcceptanceCriteria: new List<string> { "Email sent within 30 seconds", "OTP expires after 10 minutes" },
                Dependencies: new List<string>(),
                EstimatedStoryPoints: 5,
                Priority: PriorityLevel.High,
                CreatedAt: DateTime.UtcNow.ToString("o"),
                UpdatedAt: DateTime.UtcNow.ToString("o"),
                AdoWorkItemId: null
            );

            var userStory = new UserStory(
                Id: Guid.NewGuid().ToString(),
                Title: "User receives MFA code via email",
                AsA: "User",
                IWant: "to receive an MFA code via email",
                SoThat: "I can verify my identity securely",
                AcceptanceCriteria: new List<string> { "Code delivered within 30 seconds" },
                StoryPoints: 3,
                Priority: PriorityLevel.Medium,
                FeatureId: feature.Id,
                Dependencies: new List<string>(),
                CreatedAt: DateTime.UtcNow.ToString("o"),
                UpdatedAt: DateTime.UtcNow.ToString("o"),
                AdoWorkItemId: null
            );

            var task = new TaskItem(
                Id: Guid.NewGuid().ToString(),
                Title: "Implement email service integration",
                Description: "Integrate with SendGrid/AWS SES",
                TaskType: TaskType.Development,
                EstimatedHours: 8,
                UserStoryId: userStory.Id,
                Dependencies: new List<string>(),
                AssignedTo: null,
                Checklist: new List<string> { "Configure SMTP", "Send test email", "Add retry logic" },
                CreatedAt: DateTime.UtcNow.ToString("o"),
                UpdatedAt: DateTime.UtcNow.ToString("o"),
                AdoWorkItemId: null
            );

            var testCase = new TestCase(
                Id: Guid.NewGuid().ToString(),
                Title: "Verify MFA code is sent",
                Scenario: "User logs in and requests MFA code",
                Steps: new List<string> { "1. Log in", "2. Request MFA code", "3. Check email" },
                ExpectedResult: "Email received with valid code",
                Priority: PriorityLevel.High,
                UserStoryId: userStory.Id,
                CreatedAt: DateTime.UtcNow.ToString("o"),
                UpdatedAt: DateTime.UtcNow.ToString("o"),
                AdoWorkItemId: null
            );

            return Ok(new ArtifactPreview(
                Epic: epic,
                Features: new List<Feature> { feature },
                UserStories: new List<UserStory> { userStory },
                Tasks: new List<TaskItem> { task },
                TestCases: new List<TestCase> { testCase }
            ));
        }

        [HttpPost("sync-to-ado")]
        public ActionResult<SyncResponse> SyncToAdo([FromBody] SyncToADORequest request)
        {
            var epicAdoId = 101;
            var featureAdoIds = new List<int> { 201 };
            var storyAdoIds = new List<int> { 301 };
            var taskAdoIds = new List<int> { 401 };
            var testCaseAdoIds = new List<int> { 501 };

            return Ok(new SyncResponse(
                Success: true,
                EpicAdoId: epicAdoId,
                FeatureAdoIds: featureAdoIds,
                StoryAdoIds: storyAdoIds,
                TaskAdoIds: taskAdoIds,
                TestCaseAdoIds: testCaseAdoIds,
                Errors: new List<string>(),
                AdoDashboardUrl: $"https://dev.azure.com/example/project/_workitems/edit/{epicAdoId}"
            ));
        }

        [HttpPost("process-and-sync")]
        public ActionResult<object> ProcessAndSync([FromBody] ProcessAndSyncRequest request)
        {
            var processingId = Guid.NewGuid().ToString();
            var status = new ProcessingStatus(
                ProcessingId: processingId,
                Status: "processing",
                ProgressPercent: 100,
                CurrentStep: "completed",
                ArtifactsCount: 5,
                AdoSyncStatus: "completed"
            );
            ProcessingStatusStore[processingId] = status;

            return Ok(new
            {
                processing_id = processingId,
                status = "completed",
                artifacts = new
                {
                    epic = new { title = "User Authentication System" },
                    features = new[] { new { title = "Email-based MFA" } },
                    user_stories = new[] { new { title = "User receives MFA code via email" } },
                    tasks = new[] { new { title = "Implement email service integration" } },
                    test_cases = new[] { new { title = "Verify MFA code is sent" } }
                }
            });
        }

        [HttpGet("status/{processingId}")]
        public ActionResult<ProcessingStatus> GetProcessingStatus(string processingId)
        {
            if (!ProcessingStatusStore.TryGetValue(processingId, out var status))
            {
                return NotFound(new { detail = "Processing ID not found" });
            }

            return Ok(status);
        }

        [HttpGet("health")]
        public ActionResult<object> HealthCheck()
        {
            return Ok(new
            {
                status = "healthy",
                version = "1.0.0",
                components = new
                {
                    llm = "ready",
                    ado = "ready",
                    database = "ready"
                }
            });
        }
    }
}
