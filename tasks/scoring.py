from datetime import date, datetime
from django.utils import timezone

def calculate_task_score(task_data, strategy="smart_balance"):
    """
    Calculate priority score based on multiple factors
    Higher score = Higher priority
    """
    score = 0
    today = timezone.now().date()
    
    # Handle date conversion if it's a string
    if isinstance(task_data['due_date'], str):
        due_date = datetime.strptime(task_data['due_date'], '%Y-%m-%d').date()
    else:
        due_date = task_data['due_date']
    
    days_until_due = (due_date - today).days
    
    # Strategy-based scoring
    if strategy == "smart_balance":
        # Urgency: Exponential scoring for closer deadlines
        if days_until_due < 0:
            # Overdue tasks get highest priority
            score += 100 + abs(days_until_due) * 2
        elif days_until_due == 0:
            score += 80
        elif days_until_due <= 1:
            score += 70
        elif days_until_due <= 3:
            score += 50
        elif days_until_due <= 7:
            score += 30
        
        # Importance: Linear scaling
        score += task_data['importance'] * 6
        
        # Effort: Quick wins bonus
        if task_data['estimated_hours'] <= 1:
            score += 25
        elif task_data['estimated_hours'] <= 2:
            score += 15
        elif task_data['estimated_hours'] >= 8:
            score -= 10
            
        # Dependencies: Tasks that block others get priority
        if task_data.get('dependencies'):
            score += len(task_data['dependencies']) * 3
            
    elif strategy == "fastest_wins":
        # Prioritize quick tasks
        score = 100 - task_data['estimated_hours'] * 8
        score += task_data['importance'] * 2
        
    elif strategy == "high_impact":
        # Prioritize important tasks
        score = task_data['importance'] * 10
        if days_until_due <= 3:
            score += 20
            
    elif strategy == "deadline_driven":
        # Prioritize by due date
        if days_until_due < 0:
            score = 100 + abs(days_until_due) * 5
        else:
            score = max(0, 100 - days_until_due * 3)
        score += task_data['importance'] * 2
    
    return max(0, score)  # Ensure score is not negative

def detect_circular_dependencies(tasks):
    """
    Detect circular dependencies in tasks
    """
    def has_cycle(task_id, visited, rec_stack, task_map):
        visited[task_id] = True
        rec_stack[task_id] = True
        
        for dep_id in task_map.get(task_id, []):
            if not visited.get(dep_id):
                if has_cycle(dep_id, visited, rec_stack, task_map):
                    return True
            elif rec_stack.get(dep_id):
                return True
                
        rec_stack[task_id] = False
        return False
    
    # Create task map for dependency checking
    task_map = {}
    for task in tasks:
        task_id = task.get('id', tasks.index(task))
        task_map[task_id] = task.get('dependencies', [])
    
    visited = {}
    rec_stack = {}
    
    for task_id in task_map:
        if not visited.get(task_id):
            if has_cycle(task_id, visited, rec_stack, task_map):
                return True
    return False