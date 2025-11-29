from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    priority_score = serializers.FloatField(read_only=True)
    explanation = serializers.CharField(read_only=True)
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'due_date', 'estimated_hours', 
                 'importance', 'dependencies', 'priority_score', 'explanation']

class TaskInputSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    due_date = serializers.DateField()
    estimated_hours = serializers.IntegerField(min_value=1, max_value=100)
    importance = serializers.IntegerField(min_value=1, max_value=10)
    dependencies = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        default=list
    )