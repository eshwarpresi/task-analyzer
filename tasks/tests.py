from django.test import TestCase
from datetime import date, timedelta
from .scoring import calculate_task_score, detect_circular_dependencies

class ScoringAlgorithmTests(TestCase):
    def test_basic_scoring(self):
        task = {
            'title': 'Test Task',
            'due_date': date.today() + timedelta(days=1),
            'estimated_hours': 2,
            'importance': 8,
            'dependencies': []
        }
        
        score = calculate_task_score(task)
        self.assertIsInstance(score, (int, float))
        self.assertGreater(score, 0)
    
    def test_overdue_task(self):
        task = {
            'title': 'Overdue Task',
            'due_date': date.today() - timedelta(days=5),
            'estimated_hours': 3,
            'importance': 5,
            'dependencies': []
        }
        
        score = calculate_task_score(task)
        self.assertGreater(score, 100)  # Overdue tasks should get high scores
    
    def test_quick_win_task(self):
        task = {
            'title': 'Quick Task',
            'due_date': date.today() + timedelta(days=7),
            'estimated_hours': 1,
            'importance': 6,
            'dependencies': []
        }
        
        score = calculate_task_score(task)
        self.assertGreater(score, 50)  # Quick wins should get decent scores
    
    def test_high_importance_task(self):
        task = {
            'title': 'Important Task',
            'due_date': date.today() + timedelta(days=14),
            'estimated_hours': 4,
            'importance': 10,
            'dependencies': []
        }
        
        score = calculate_task_score(task)
        self.assertGreater(score, 40)  # High importance should boost score
    
    def test_circular_dependencies(self):
        tasks_with_circular_deps = [
            {'id': 1, 'dependencies': [2]},
            {'id': 2, 'dependencies': [1]},
            {'id': 3, 'dependencies': []}
        ]
        
        self.assertTrue(detect_circular_dependencies(tasks_with_circular_deps))
    
    def test_no_circular_dependencies(self):
        tasks_without_circular_deps = [
            {'id': 1, 'dependencies': [2]},
            {'id': 2, 'dependencies': [3]},
            {'id': 3, 'dependencies': []}
        ]
        
        self.assertFalse(detect_circular_dependencies(tasks_without_circular_deps))

class ViewTests(TestCase):
    def test_analyze_endpoint(self):
        response = self.client.post('/api/tasks/analyze/', 
            content_type='application/json',
            data='{"tasks": []}'
        )
        self.assertEqual(response.status_code, 400)
    
    def test_suggest_endpoint(self):
        response = self.client.get('/api/tasks/suggest/')
        self.assertEqual(response.status_code, 200)