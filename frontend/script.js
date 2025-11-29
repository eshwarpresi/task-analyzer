let tasks = [];

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    // Set minimum date to today
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('dueDate').min = today;
    document.getElementById('dueDate').value = today;
    
    // Add form submit handler
    document.getElementById('singleTaskForm').addEventListener('submit', function(e) {
        e.preventDefault();
        addTaskFromForm();
    });
});

function addTaskFromForm() {
    const task = {
        title: document.getElementById('title').value,
        due_date: document.getElementById('dueDate').value,
        estimated_hours: parseInt(document.getElementById('estimatedHours').value),
        importance: parseInt(document.getElementById('importance').value),
        dependencies: []
    };
    
    tasks.push(task);
    updateCurrentTasksList();
    
    // Reset form but keep today's date
    document.getElementById('title').value = '';
    document.getElementById('estimatedHours').value = '1';
    document.getElementById('importance').value = '5';
    document.getElementById('dueDate').value = new Date().toISOString().split('T')[0];
    
    console.log('Form task added. Total tasks:', tasks.length);
}

function updateCurrentTasksList() {
    const container = document.getElementById('currentTasksList');
    container.innerHTML = '';
    
    if (tasks.length === 0) {
        container.innerHTML = '<p>No tasks added yet.</p>';
        return;
    }
    
    tasks.forEach((task, index) => {
        const taskElement = document.createElement('div');
        taskElement.className = 'task-item';
        taskElement.innerHTML = `
            <strong>${index + 1}. ${task.title}</strong><br>
            Due: ${task.due_date} | Hours: ${task.estimated_hours} | Importance: ${task.importance}
        `;
        container.appendChild(taskElement);
    });
}

async function analyzeTasks() {
    let tasksToAnalyze = [];
    
    // Check if JSON input has data
    const jsonInput = document.getElementById('jsonInput').value.trim();
    if (jsonInput) {
        try {
            const jsonTasks = JSON.parse(jsonInput);
            console.log('Using JSON tasks:', jsonTasks.length);
            
            // COMBINE form tasks + JSON tasks for analysis (ONLY if not already added)
            // Check if JSON tasks are already in the tasks array
            const newJsonTasks = jsonTasks.filter(jsonTask => 
                !tasks.some(existingTask => existingTask.title === jsonTask.title)
            );
            
            tasksToAnalyze = [...tasks, ...newJsonTasks];
            
            // Also update current tasks to show both (only add new JSON tasks)
            tasks = [...tasks, ...newJsonTasks];
            updateCurrentTasksList();
            
            // Clear JSON input after using it to prevent duplicates
            document.getElementById('jsonInput').value = '';
            
        } catch (e) {
            showError('Invalid JSON format. Please check your input.');
            return;
        }
    } else {
        // Use only form tasks
        if (tasks.length === 0) {
            showError('Please add some tasks first.');
            return;
        }
        tasksToAnalyze = tasks;
        console.log('Using form tasks:', tasksToAnalyze.length);
    }
    
    console.log('Total tasks to analyze:', tasksToAnalyze.length);
    
    showLoading();
    hideError();
    
    try {
        const response = await fetch('/api/tasks/analyze/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                tasks: tasksToAnalyze,
                strategy: document.getElementById('strategy').value
            })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Analysis failed');
        }
        
        displayResults(data.tasks, data.strategy);
        
    } catch (error) {
        showError('Failed to analyze tasks: ' + error.message);
    } finally {
        hideLoading();
    }
}

async function getSuggestions() {
    showLoading();
    hideError();
    
    try {
        const response = await fetch('/api/tasks/suggest/');
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to get suggestions');
        }
        
        displayResults(data.suggested_tasks, 'smart_balance');
        
    } catch (error) {
        showError('Failed to get suggestions: ' + error.message);
    } finally {
        hideLoading();
    }
}

function displayResults(analyzedTasks, strategy) {
    const resultsContainer = document.getElementById('results');
    resultsContainer.innerHTML = '';
    
    if (!analyzedTasks || analyzedTasks.length === 0) {
        resultsContainer.innerHTML = '<p>No tasks to display.</p>';
        return;
    }
    
    const strategyNames = {
        'smart_balance': 'Smart Balance',
        'fastest_wins': 'Fastest Wins', 
        'high_impact': 'High Impact',
        'deadline_driven': 'Deadline Driven'
    };
    
    resultsContainer.innerHTML = `
        <div class="strategy-info">
            <h3>Strategy: ${strategyNames[strategy] || strategy}</h3>
            <p>Sorted by priority score (higher = more important)</p>
        </div>
    `;
    
    analyzedTasks.forEach((task, index) => {
        const priorityClass = getPriorityClass(task.priority_score);
        const priorityText = getPriorityText(task.priority_score);
        
        const taskCard = document.createElement('div');
        taskCard.className = `task-card ${priorityClass}`;
        taskCard.innerHTML = `
            <div class="task-header">
                <div class="task-title">${index + 1}. ${task.title}</div>
                <div class="priority-badge priority-${priorityText}">${priorityText.toUpperCase()}</div>
            </div>
            
            <div class="task-details">
                <div class="detail-item">
                    <div class="detail-label">Due Date</div>
                    <div class="detail-value">${task.due_date}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Effort</div>
                    <div class="detail-value">${task.estimated_hours}h</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Importance</div>
                    <div class="detail-value">${task.importance}/10</div>
                </div>
            </div>
            
            <div class="task-explanation">
                ${task.explanation || 'No explanation available'}
            </div>
            
            <div class="score-display">
                Priority Score: ${Math.round(task.priority_score)}
            </div>
        `;
        
        resultsContainer.appendChild(taskCard);
    });
}

function getPriorityClass(score) {
    if (score >= 80) return 'high-priority';
    if (score >= 50) return 'medium-priority';
    return 'low-priority';
}

function getPriorityText(score) {
    if (score >= 80) return 'high';
    if (score >= 50) return 'medium';
    return 'low';
}

function clearAll() {
    tasks = [];
    document.getElementById('jsonInput').value = '';
    document.getElementById('results').innerHTML = '';
    updateCurrentTasksList();
    hideError();
}

function showLoading() {
    document.getElementById('loading').classList.remove('hidden');
}

function hideLoading() {
    document.getElementById('loading').classList.add('hidden');
}

function showError(message) {
    const errorDiv = document.getElementById('error');
    errorDiv.textContent = message;
    errorDiv.classList.remove('hidden');
}

function hideError() {
    document.getElementById('error').classList.add('hidden');
}