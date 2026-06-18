using System.Collections.Generic;

namespace dotnet_app.Models
{
    public enum PriorityLevel
    {
        Critical,
        High,
        Medium,
        Low
    }

    public enum EffortLevel
    {
        Small,
        Medium,
        Large
    }

    public enum TaskType
    {
        Development,
        Testing,
        Documentation,
        DevOps
    }

    public record Epic(
        string Id,
        string Title,
        string Description,
        string BusinessValue,
        List<string> SuccessCriteria,
        EffortLevel EstimatedEffort,
        PriorityLevel Priority,
        List<string> TechnicalTags,
        string CreatedAt,
        string UpdatedAt,
        string? AdoWorkItemId
    );

    public record Feature(
        string Id,
        string Title,
        string Description,
        string EpicId,
        List<string> AcceptanceCriteria,
        List<string> Dependencies,
        int EstimatedStoryPoints,
        PriorityLevel Priority,
        string CreatedAt,
        string UpdatedAt,
        string? AdoWorkItemId
    );

    public record UserStory(
        string Id,
        string Title,
        string AsA,
        string IWant,
        string SoThat,
        List<string> AcceptanceCriteria,
        int StoryPoints,
        PriorityLevel Priority,
        string FeatureId,
        List<string> Dependencies,
        string CreatedAt,
        string UpdatedAt,
        string? AdoWorkItemId
    );

    public record TaskItem(
        string Id,
        string Title,
        string Description,
        TaskType TaskType,
        int EstimatedHours,
        string UserStoryId,
        List<string> Dependencies,
        string? AssignedTo,
        List<string> Checklist,
        string CreatedAt,
        string UpdatedAt,
        string? AdoWorkItemId
    );

    public record TestCase(
        string Id,
        string Title,
        string Scenario,
        List<string> Steps,
        string ExpectedResult,
        PriorityLevel Priority,
        string UserStoryId,
        string CreatedAt,
        string UpdatedAt,
        string? AdoWorkItemId
    );

    public record ProcessRequirementRequest(
        string Requirement,
        string? EpicTitle = null,
        bool IncludeArchitectureDiagram = false,
        bool IncludeCodeSkeleton = false
    );

    public record SyncToADORequest(
        string EpicId,
        bool AutoCreateLinks = true,
        bool SendNotifications = true,
        string? AssignToTeam = null
    );

    public record ProcessAndSyncRequest(
        string Requirement,
        bool AutoSync = true,
        string? AssignToTeam = null
    );

    public record ArtifactPreview(
        Epic Epic,
        List<Feature> Features,
        List<UserStory> UserStories,
        List<TaskItem> Tasks,
        List<TestCase> TestCases
    );

    public record SyncResponse(
        bool Success,
        int? EpicAdoId,
        List<int> FeatureAdoIds,
        List<int> StoryAdoIds,
        List<int> TaskAdoIds,
        List<int> TestCaseAdoIds,
        List<string> Errors,
        string? AdoDashboardUrl
    );

    public record ProcessingStatus(
        string ProcessingId,
        string Status,
        int ProgressPercent,
        string CurrentStep,
        int ArtifactsCount,
        string AdoSyncStatus,
        string? ErrorMessage = null
    );
}
