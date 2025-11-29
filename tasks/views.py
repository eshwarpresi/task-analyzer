from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
from datetime import date
from .scoring import calculate_task_score, detect_circular_dependencies

# ADD THIS VIEW - serves the frontend
class FrontendView(View):
    def get(self, request):
        return render(request, 'index.html')

@method_decorator(csrf_exempt, name='dispatch')
class AnalyzeTasksView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            tasks = data.get('tasks', [])
            strategy = data.get('strategy', 'smart_balance')
            
            # Validate input
            if not tasks:
                return JsonResponse({'error': 'No tasks provided'}, status=400)
            
            # Check for circular dependencies
            if detect_circular_dependencies(tasks):
                return JsonResponse({'error': 'Circular dependencies detected'}, status=400)
            
            # Calculate scores and add explanations
            for task in tasks:
                task['priority_score'] = calculate_task_score(task, strategy)
                task['explanation'] = self._generate_explanation(task, strategy)
            
            # Sort by priority score (descending)
            sorted_tasks = sorted(tasks, key=lambda x: x['priority_score'], reverse=True)
            
            return JsonResponse({'tasks': sorted_tasks, 'strategy': strategy})
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    def _generate_explanation(self, task, strategy):
        explanations = []
        
        if isinstance(task['due_date'], str):
            due_date = date.fromisoformat(task['due_date'])
        else:
            due_date = task['due_date']
        
        days_until_due = (due_date - date.today()).days
        
        if days_until_due < 0:
            explanations.append(f"Overdue by {abs(days_until_due)} days")
        elif days_until_due == 0:
            explanations.append("Due today")
        elif days_until_due <= 3:
            explanations.append("Due soon")
            
        if task['importance'] >= 8:
            explanations.append("High importance")
        elif task['importance'] <= 3:
            explanations.append("Low importance")
            
        if task['estimated_hours'] <= 2:
            explanations.append("Quick task")
        elif task['estimated_hours'] >= 6:
            explanations.append("Time-consuming")
            
        if task.get('dependencies'):
            explanations.append(f"Blocks {len(task['dependencies'])} other tasks")
            
        return ", ".join(explanations) if explanations else "Moderate priority"

@method_decorator(csrf_exempt, name='dispatch')
class SuggestTasksView(View):
    def get(self, request):
        try:
            # For demo purposes, we'll use sample data
            # In a real app, this would fetch from database
            sample_tasks = [
                {
                    'id': 1,
                    'title': 'Complete project documentation',
                    'due_date': date.today().isoformat(),
                    'estimated_hours': 2,
                    'importance': 7,
                    'dependencies': []
                },
                {
                    'id': 2,
                    'title': 'Fix critical bug in login system',
                    'due_date': (date.today()).isoformat(),
                    'estimated_hours': 4,
                    'importance': 9,
                    'dependencies': [1]
                },
                {
                    'id': 3,
                    'title': 'Setup development environment',
                    'due_date': (date.today()).isoformat(),
                    'estimated_hours': 1,
                    'importance': 6,
                    'dependencies': []
                }
            ]
            
            # Calculate scores
            for task in sample_tasks:
                task['priority_score'] = calculate_task_score(task)
                task['explanation'] = AnalyzeTasksView._generate_explanation(None, task, 'smart_balance')
            
            # Get top 3
            top_tasks = sorted(sample_tasks, key=lambda x: x['priority_score'], reverse=True)[:3]
            
            return JsonResponse({'suggested_tasks': top_tasks})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)