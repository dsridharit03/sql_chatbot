# ----------------------------------------
# FILE: backend/query_api/urls.py
# ----------------------------------------
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # homepage
    path('health/', views.health_check, name='health_check'),
    path('test-connection/', views.test_connection, name='test_connection'),
    path('schema/', views.get_schema, name='get_schema'),
    path('query/', views.process_query, name='process_query'),
    path('test-sql/', views.test_sql, name='test_sql'),
]
