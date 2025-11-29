# Smart Task Analyzer

[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/eshwarpresi/task-analyzer)

A Django-based web application that intelligently prioritizes tasks using custom scoring algorithms. Features multiple sorting strategies, RESTful APIs, and a responsive frontend.

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8+
- Git

### Installation & Running

1. **Clone the repository**
   ```bash
   git clone https://github.com/eshwarpresi/task-analyzer.git
   cd task-analyzer
Set up virtual environment

bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux
Install dependencies

bash
pip install -r requirements.txt
Run migrations

bash
python manage.py migrate
Start development server

bash
python manage.py runserver
Access application
Open http://127.0.0.1:8000 in your browser

🧠 Algorithm Explanation
The Smart Task Analyzer uses a sophisticated scoring system that evaluates tasks based on four key factors: urgency, importance, effort, and dependencies. Each factor is weighted differently depending on the selected strategy.

Core Scoring Factors:
1. Urgency (Time Sensitivity)

Overdue tasks: +100 + (days overdue × 2)

Due today: +80 points

Due in 1-3 days: +50-70 points

Due in 4-7 days: +30 points
This exponential decay ensures imminent deadlines receive significantly higher priority.

2. Importance (User-Defined Value)

Linear scaling: importance × 6

High importance (8-10): Major priority boost

Low importance (1-3): Minimal impact

3. Effort (Quick Wins)

≤1 hour: +25 points (significant quick win bonus)

≤2 hours: +15 points (moderate bonus)

≥8 hours: -10 points (penalty for time-consuming tasks)
This encourages completing smaller tasks that can be finished quickly.

4. Dependencies (Blocking Tasks)

+3 points per dependent task

Tasks blocking others receive higher priority

Circular dependency detection prevents infinite loops

Strategy Variations:
Smart Balance: Balanced weighting of all factors

Fastest Wins: Prioritizes low-effort tasks (100 - hours × 8)

High Impact: Focuses on importance (importance × 10)

Deadline Driven: Emphasizes due dates (100 - days_until × 3)

The algorithm ensures overdue and urgent tasks receive immediate attention while balancing importance and available time.

🎯 Design Decisions
Backend Architecture
Django REST Framework: Chosen for rapid development and built-in security

SQLite Database: Sufficient for demo purposes, easy setup

Class-Based Views: Better organization and code reuse

Separate Scoring Module: Algorithm decoupled from business logic

Frontend Approach
Vanilla JavaScript: No framework dependencies, demonstrates core skills

Responsive CSS Grid: Works on all device sizes

Dual Input Methods: Both form and JSON input for flexibility

Trade-offs Made
No User Authentication: Simplified for assignment scope

In-Memory Task Storage: No database persistence for demo tasks

Basic Error Handling: Focus on core functionality over edge cases

Simple Dependency System: Linear dependencies rather than complex graphs

⏱️ Time Breakdown
Project Setup: 30 minutes

Backend Development: 2 hours

Django setup and models: 30 minutes

Scoring algorithm: 45 minutes

API endpoints: 45 minutes

Frontend Development: 1.5 hours

HTML structure: 30 minutes

JavaScript functionality: 45 minutes

CSS styling: 15 minutes

Testing & Debugging: 45 minutes

Documentation: 30 minutes

Total: Approximately 5 hours

🏆 Bonus Challenges Attempted
Circular Dependency Detection ✅

Implemented graph traversal to detect dependency cycles

Prevents infinite loops in task prioritization

Unit Tests ✅

Comprehensive test suite for scoring algorithm

API endpoint testing

Edge case coverage

🔮 Future Improvements
With more time, I would implement:

User Authentication & Persistence

User accounts with task saving

Database persistence for tasks

Advanced Visualization

Eisenhower Matrix view

Gantt chart for task timelines

Dependency graph visualization

Enhanced Algorithm

Machine learning for personalized weighting

Consideration of weekends/holidays

Energy-level based scheduling

Collaboration Features

Team task assignment

Progress tracking

Comments and attachments

Mobile Application

React Native mobile app

Push notifications for deadlines
