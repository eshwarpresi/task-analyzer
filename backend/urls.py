from django.contrib import admin
from django.urls import path, include
from tasks.views import FrontendView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/tasks/', include('tasks.urls')),
    path('', FrontendView.as_view(), name='frontend'),
]