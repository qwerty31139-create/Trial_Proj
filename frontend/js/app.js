/**
 * Requirements to ADO Artifacts System - Frontend JavaScript
 */

// Configuration
const API_BASE_URL = 'http://localhost:8000/api/v1';
const POLL_INTERVAL = 1000; // 1 second

// DOM Elements
const requirementInput = document.getElementById('requirement-input');
const processBtn = document.getElementById('process-btn');
const autoSyncCheckbox = document.getElementById('auto-sync');
const includeDiagramCheckbox = document.getElementById('include-diagram');

// State
let currentProcessingId = null;
let currentArtifacts = null;

// ===== EVENT LISTENERS =====
processBtn.addEventListener('click', handleProcessRequirement);

// ===== MAIN FUNCTIONS =====
async function handleProcessRequirement() {
    const requirement = requirementInput.value.trim();
    
    if (!requirement) {
        showError('Please enter a requirement');
        return;
    }
    
    try {
        processBtn.disabled = true;
        processBtn.textContent = '⏳ Processing...';
        
        if (autoSyncCheckbox.checked) {
            // Use combined process and sync endpoint
            await handleProcessAndSync(requirement);
        } else {
            // Just process without syncing
            await handleProcessOnly(requirement);
        }
    } catch (error) {
        showError(`Processing failed: ${error.message}`);
    } finally {
        processBtn.disabled = false;
        processBtn.textContent = '🚀 Process Requirement';
    }
}

async function handleProcessOnly(requirement) {
    const response = await fetch(`${API_BASE_URL}/process-requirement`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            requirement: requirement,
            include_architecture_diagram: includeDiagramCheckbox.checked,
            include_code_skeleton: false
        })
    });
    
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Processing failed');
    }
    
    const artifacts = await response.json();
    currentArtifacts = artifacts;
    
    // Show preview
    displayPreview(artifacts);
    scrollToStep('preview-step');
    
    // Show success message
    showSuccess('Requirement processed successfully! Review the artifacts below.');
}

async function handleProcessAndSync(requirement) {
    const response = await fetch(`${API_BASE_URL}/process-and-sync`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            requirement: requirement,
            auto_sync: true
        })
    });
    
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Processing failed');
    }
    
    const result = await response.json();
    currentProcessingId = result.processing_id;
    currentArtifacts = result.artifacts;
    
    // Display preview
    displayPreview(result.artifacts);
    
    // Poll for sync status
    pollSyncStatus();
}

async function pollSyncStatus() {
    const maxAttempts = 30;
    let attempts = 0;
    
    const pollInterval = setInterval(async () => {
        attempts++;
        
        try {
            const response = await fetch(`${API_BASE_URL}/status/${currentProcessingId}`);
            if (!response.ok) throw new Error('Failed to get status');
            
            const status = await response.json();
            displaySyncStatus(status);
            
            // Stop polling if complete or failed
            if (status.status === 'completed' || status.status === 'failed' || attempts >= maxAttempts) {
                clearInterval(pollInterval);
            }
        } catch (error) {
            console.error('Error polling status:', error);
            clearInterval(pollInterval);
        }
    }, POLL_INTERVAL);
}

// ===== DISPLAY FUNCTIONS =====
function displayPreview(artifacts) {
    const previewStep = document.getElementById('preview-step');
    const previewContent = document.getElementById('preview-content');
    
    let html = '';
    
    // Epic
    html += generateArtifactCard('Epic', artifacts.epic);
    
    // Features
    if (artifacts.features.length > 0) {
        html += '<h3 style="margin-top: 20px; color: #464feb;">Features</h3>';
        artifacts.features.forEach(feature => {
            html += generateArtifactCard('Feature', feature);
        });
    }
    
    // User Stories
    if (artifacts.user_stories.length > 0) {
        html += '<h3 style="margin-top: 20px; color: #464feb;">User Stories</h3>';
        artifacts.user_stories.forEach(story => {
            html += generateArtifactCard('User Story', story);
        });
    }
    
    // Tasks
    if (artifacts.tasks.length > 0) {
        html += '<h3 style="margin-top: 20px; color: #464feb;">Tasks</h3>';
        artifacts.tasks.forEach(task => {
            html += generateArtifactCard('Task', task);
        });
    }
    
    // Test Cases
    if (artifacts.test_cases.length > 0) {
        html += '<h3 style="margin-top: 20px; color: #464feb;">Test Cases</h3>';
        artifacts.test_cases.forEach(test => {
            html += generateArtifactCard('Test Case', test);
        });
    }
    
    previewContent.innerHTML = html;
    previewStep.style.display = 'block';
}

function generateArtifactCard(type, artifact) {
    let html = `<div class="artifact">
        <span class="artifact-type">${type}</span>
        <h3>${artifact.title || artifact.name || 'Untitled'}</h3>`;
    
    if (artifact.description) {
        html += `<p>${artifact.description}</p>`;
    }
    
    if (artifact.as_a) {
        html += `<p><strong>As a:</strong> ${artifact.as_a}</p>
                 <p><strong>I want:</strong> ${artifact.i_want}</p>
                 <p><strong>So that:</strong> ${artifact.so_that}</p>`;
    }
    
    if (artifact.acceptance_criteria && Array.isArray(artifact.acceptance_criteria)) {
        html += '<p><strong>Acceptance Criteria:</strong></p><ul class="artifact-list">';
        artifact.acceptance_criteria.forEach(criteria => {
            html += `<li>${criteria}</li>`;
        });
        html += '</ul>';
    }
    
    if (artifact.story_points) {
        html += `<p><strong>Story Points:</strong> ${artifact.story_points}</p>`;
    }
    
    if (artifact.priority) {
        html += `<p><strong>Priority:</strong> <span class="status ${artifact.priority.toLowerCase()}">${artifact.priority}</span></p>`;
    }
    
    html += '</div>';
    return html;
}

function displaySyncStatus(status) {
    const syncStep = document.getElementById('sync-step');
    const syncContent = document.getElementById('sync-content');
    
    let html = `
        <div style="padding: 30px;">
            <div class="info-message">
                <strong>Status:</strong> ${capitalize(status.status)}
            </div>
            
            <div class="progress">
                <div class="progress-bar" style="width: ${status.progress_percent}%"></div>
            </div>
            
            <p><strong>Progress:</strong> ${status.progress_percent}% complete</p>
            <p><strong>Current Step:</strong> ${status.current_step}</p>
            <p><strong>ADO Sync:</strong> <span class="status ${status.ado_sync_status}">${capitalize(status.ado_sync_status)}</span></p>
            <p><strong>Artifacts:</strong> ${status.artifacts_count}</p>
    `;
    
    if (status.error_message) {
        html += `<div class="error-message"><strong>Error:</strong> ${status.error_message}</div>`;
    }
    
    if (status.status === 'completed') {
        html += `<div class="success-message">✅ Processing and sync completed successfully!</div>`;
    }
    
    html += '</div>';
    
    syncContent.innerHTML = html;
    syncStep.style.display = 'block';
}

// ===== UTILITY FUNCTIONS =====
function showError(message) {
    const notification = document.createElement('div');
    notification.className = 'error-message';
    notification.textContent = message;
    notification.style.position = 'fixed';
    notification.style.top = '20px';
    notification.style.right = '20px';
    notification.style.zIndex = '9999';
    notification.style.maxWidth = '400px';
    document.body.appendChild(notification);
    
    setTimeout(() => notification.remove(), 5000);
}

function showSuccess(message) {
    const notification = document.createElement('div');
    notification.className = 'success-message';
    notification.textContent = message;
    notification.style.position = 'fixed';
    notification.style.top = '20px';
    notification.style.right = '20px';
    notification.style.zIndex = '9999';
    notification.style.maxWidth = '400px';
    document.body.appendChild(notification);
    
    setTimeout(() => notification.remove(), 5000);
}

function scrollToStep(stepId) {
    const element = document.getElementById(stepId);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

function capitalize(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

// ===== INITIALIZATION =====
document.addEventListener('DOMContentLoaded', () => {
    console.log('Requirements to ADO System initialized');
});
