# ========================================
# COMPLETE DJANGO BACKEND - ALL PYTHON FILES
# ========================================

# ========================================
# FILE: backend/manage.py
# ========================================
#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nl2sql_project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()


# ========================================
# FILE: backend/nl2sql_project/__init__.py
# ========================================
# NL2SQL Django Project


# ========================================
# FILE: backend/nl2sql_project/settings.py
# ========================================
"""
Django settings for nl2sql_project.
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Secret key
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-dev-key-change-in-production')

# Debug mode
DEBUG = os.getenv('DEBUG', 'True') == 'True'

# Allowed hosts
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'rest_framework',
    'corsheaders',
    
    # Local apps
    'query_api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'nl2sql_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'nl2sql_project.wsgi.application'

# Database (SQLite for Django admin only)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# SQL Server Configuration (for our queries)
SQL_SERVER_CONFIG = {
    'DRIVER': '{ODBC Driver 17 for SQL Server}',
    'SERVER': os.getenv('DB_SERVER', 'localhost'),
    'DATABASE': os.getenv('DB_NAME', 'master'),
    'UID': os.getenv('DB_USER', 'sa'),
    'PWD': os.getenv('DB_PASSWORD', ''),
    'TrustServerCertificate': 'yes',
    'Encrypt': 'yes',
}

# AI Configuration
AI_PROVIDER = os.getenv('AI_PROVIDER', 'openai')  # 'openai' or 'anthropic'
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'

# Default primary key
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS Settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
CORS_ALLOW_CREDENTIALS = True

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
}


# ========================================
# FILE: backend/nl2sql_project/urls.py
# ========================================
"""
URL configuration for nl2sql_project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('query_api.urls')),
]


# ========================================
# FILE: backend/nl2sql_project/wsgi.py
# ========================================
"""
WSGI config for nl2sql_project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nl2sql_project.settings')

application = get_wsgi_application()


# ========================================
# FILE: backend/nl2sql_project/asgi.py
# ========================================
"""
ASGI config for nl2sql_project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nl2sql_project.settings')

application = get_asgi_application()


# ========================================
# FILE: backend/query_api/__init__.py
# ========================================
# Query API App


# ========================================
# FILE: backend/query_api/apps.py
# ========================================
from django.apps import AppConfig


class QueryApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'query_api'


# ========================================
# FILE: backend/query_api/models.py
# ========================================
from django.db import models

# No models needed - querying external SQL Server database


# ========================================
# FILE: backend/query_api/admin.py
# ========================================
from django.contrib import admin

# No models to register


# ========================================
# FILE: backend/query_api/database_service.py
# ========================================
"""
Database Service for SQL Server operations
"""
import pyodbc
from django.conf import settings


class DatabaseService:
    """Handle all SQL Server database operations"""
    
    @staticmethod
    def get_connection_string():
        """Build SQL Server connection string from settings"""
        config = settings.SQL_SERVER_CONFIG
        
        conn_string = (
            f"DRIVER={config['DRIVER']};"
            f"SERVER={config['SERVER']};"
            f"DATABASE={config['DATABASE']};"
            f"UID={config['UID']};"
            f"PWD={config['PWD']};"
            f"TrustServerCertificate={config['TrustServerCertificate']};"
            f"Encrypt={config['Encrypt']};"
        )
        
        return conn_string
    
    @staticmethod
    def get_database_schema():
        """
        Retrieve complete database schema (tables and columns)
        
        Returns:
            str: Formatted schema string
        """
        try:
            conn_string = DatabaseService.get_connection_string()
            conn = pyodbc.connect(conn_string)
            cursor = conn.cursor()
            
            # Get all tables and their columns
            query = """
                SELECT 
                    t.TABLE_NAME,
                    c.COLUMN_NAME,
                    c.DATA_TYPE,
                    c.IS_NULLABLE
                FROM 
                    INFORMATION_SCHEMA.TABLES t
                INNER JOIN 
                    INFORMATION_SCHEMA.COLUMNS c ON t.TABLE_NAME = c.TABLE_NAME
                WHERE 
                    t.TABLE_TYPE = 'BASE TABLE'
                ORDER BY 
                    t.TABLE_NAME, c.ORDINAL_POSITION
            """
            
            cursor.execute(query)
            rows = cursor.fetchall()
            
            # Format schema
            schema = 'Database Schema:\n\n'
            current_table = ''
            
            for row in rows:
                table_name = row[0]
                column_name = row[1]
                data_type = row[2]
                is_nullable = row[3]
                
                if current_table != table_name:
                    current_table = table_name
                    schema += f'\nTable: {table_name}\nColumns:\n'
                
                nullable = ' (nullable)' if is_nullable == 'YES' else ''
                schema += f'  - {column_name} ({data_type}){nullable}\n'
            
            cursor.close()
            conn.close()
            
            return schema
            
        except Exception as e:
            raise Exception(f"Failed to retrieve database schema: {str(e)}")
    
    @staticmethod
    def execute_query(sql_query):
        """
        Execute SQL query and return results
        
        Args:
            sql_query (str): SQL query to execute
            
        Returns:
            list: List of dictionaries with results
        """
        try:
            conn_string = DatabaseService.get_connection_string()
            conn = pyodbc.connect(conn_string)
            cursor = conn.cursor()
            
            # Execute query
            cursor.execute(sql_query)
            
            # Get column names
            columns = [column[0] for column in cursor.description]
            
            # Fetch results
            rows = cursor.fetchall()
            
            # Convert to list of dictionaries
            results = []
            for row in rows:
                result_dict = {}
                for i, column in enumerate(columns):
                    value = row[i]
                    
                    # Handle different data types
                    if value is None:
                        result_dict[column] = None
                    elif isinstance(value, (int, float, str, bool)):
                        result_dict[column] = value
                    else:
                        # Convert dates, decimals, etc. to strings
                        result_dict[column] = str(value)
                
                results.append(result_dict)
            
            cursor.close()
            conn.close()
            
            return results
            
        except Exception as e:
            raise Exception(f"Failed to execute query: {str(e)}")
    
    @staticmethod
    def validate_select_query(sql_query):
        """
        Validate that query is a safe SELECT statement
        
        Args:
            sql_query (str): SQL query to validate
            
        Returns:
            bool: True if valid and safe
        """
        sql_upper = sql_query.strip().upper()
        
        # Must start with SELECT
        if not sql_upper.startswith('SELECT'):
            return False
        
        # Block dangerous keywords
        forbidden_keywords = [
            'INSERT', 'UPDATE', 'DELETE', 'DROP', 'CREATE',
            'ALTER', 'TRUNCATE', 'EXEC', 'EXECUTE', 'MERGE',
            'GRANT', 'REVOKE', 'BACKUP', 'RESTORE'
        ]
        
        for keyword in forbidden_keywords:
            if keyword in sql_upper:
                return False
        
        return True
    
    @staticmethod
    def test_connection():
        """
        Test database connection
        
        Returns:
            dict: Connection status
        """
        try:
            conn_string = DatabaseService.get_connection_string()
            conn = pyodbc.connect(conn_string)
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
            conn.close()
            
            return {
                'success': True,
                'message': 'Database connection successful'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Database connection failed: {str(e)}'
            }


# ========================================
# FILE: backend/query_api/ai_service.py
# ========================================
"""
AI Service for Natural Language to SQL conversion
Supports both OpenAI and Anthropic Claude
"""
from django.conf import settings
from openai import OpenAI
from anthropic import Anthropic


class AIService:
    """AI-powered Natural Language to SQL conversion"""
    
    @staticmethod
    def natural_language_to_sql(question, database_schema):
        """
        Convert natural language question to SQL query
        
        Args:
            question (str): Natural language question
            database_schema (str): Database schema information
            
        Returns:
            str: Generated SQL query
        """
        provider = settings.AI_PROVIDER.lower()
        
        if provider == 'openai':
            return AIService._openai_to_sql(question, database_schema)
        elif provider == 'anthropic':
            return AIService._anthropic_to_sql(question, database_schema)
        else:
            raise Exception(f"Unknown AI provider: {provider}")
    
    @staticmethod
    def _openai_to_sql(question, database_schema):
        """
        Use OpenAI to convert question to SQL
        
        Args:
            question (str): Natural language question
            database_schema (str): Database schema
            
        Returns:
            str: SQL query
        """
        try:
            client = OpenAI(api_key=settings.OPENAI_API_KEY)
            
            prompt = f"""You are a SQL expert. Convert the following natural language question to a SQL Server query.

{database_schema}

Question: {question}

Important:
1. Return ONLY the SQL query, no explanations or markdown
2. Use TOP instead of LIMIT for SQL Server
3. Ensure the query is safe and read-only (SELECT only)
4. Use proper SQL Server syntax
5. Do not include code blocks or formatting

SQL Query:"""
            
            response = client.chat.completions.create(
                model="gpt-4",  # or "gpt-3.5-turbo" for lower cost
                messages=[
                    {
                        "role": "system",
                        "content": "You are a SQL expert that converts natural language to SQL Server queries. Return only the SQL query without any explanation."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0,
                max_tokens=500
            )
            
            sql_query = response.choices[0].message.content.strip()
            
            # Clean up response
            sql_query = sql_query.replace('```sql', '').replace('```', '').strip()
            
            return sql_query
            
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    @staticmethod
    def _anthropic_to_sql(question, database_schema):
        """
        Use Anthropic Claude to convert question to SQL
        
        Args:
            question (str): Natural language question
            database_schema (str): Database schema
            
        Returns:
            str: SQL query
        """
        try:
            client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
            
            prompt = f"""You are a SQL expert. Convert the following natural language question to a SQL Server query.

{database_schema}

Question: {question}

Important:
1. Return ONLY the SQL query, no explanations or markdown
2. Use TOP instead of LIMIT for SQL Server
3. Ensure the query is safe and read-only (SELECT only)
4. Use proper SQL Server syntax
5. Do not include code blocks or formatting

SQL Query:"""
            
            message = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                temperature=0,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            sql_query = message.content[0].text.strip()
            
            # Clean up response
            sql_query = sql_query.replace('```sql', '').replace('```', '').strip()
            
            return sql_query
            
        except Exception as e:
            raise Exception(f"Anthropic API error: {str(e)}")


# ========================================
# FILE: backend/query_api/views.py
# ========================================
"""
API Views for NL2SQL Query Interface
"""
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .database_service import DatabaseService
from .ai_service import AIService


@api_view(['GET'])
def health_check(request):
    """
    Health check endpoint
    GET /api/health/
    """
    return Response({
        'status': 'OK',
        'message': 'Django NL2SQL API is running',
        'ai_provider': settings.AI_PROVIDER
    })


@api_view(['GET'])
def test_connection(request):
    """
    Test database connection
    GET /api/test-connection/
    """
    result = DatabaseService.test_connection()
    
    if result['success']:
        return Response(result)
    else:
        return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_schema(request):
    """
    Get database schema
    GET /api/schema/
    """
    try:
        schema = DatabaseService.get_database_schema()
        return Response({
            'success': True,
            'schema': schema
        })
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def process_query(request):
    """
    Main endpoint: Convert natural language to SQL and execute
    
    POST /api/query/
    
    Request Body:
    {
        "question": "Top 10 employees from employee table"
    }
    
    Response:
    {
        "success": true,
        "question": "Top 10 employees from employee table",
        "sql": "SELECT TOP 10 * FROM Employee",
        "data": [...],
        "rowCount": 10
    }
    """
    try:
        # Get question from request
        question = request.data.get('question', '').strip()
        
        if not question:
            return Response({
                'success': False,
                'error': 'Question is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get database schema
        schema = DatabaseService.get_database_schema()
        
        # Convert natural language to SQL using AI
        sql_query = AIService.natural_language_to_sql(question, schema)
        
        # Validate query is SELECT only
        if not DatabaseService.validate_select_query(sql_query):
            return Response({
                'success': False,
                'error': 'Only SELECT queries are allowed for security',
                'generatedQuery': sql_query
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Execute query on SQL Server
        results = DatabaseService.execute_query(sql_query)
        
        # Return successful response
        return Response({
            'success': True,
            'question': question,
            'sql': sql_query,
            'data': results,
            'rowCount': len(results)
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e),
            'details': 'Failed to process query'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def test_sql(request):
    """
    Test SQL query directly (for debugging)
    
    POST /api/test-sql/
    
    Request Body:
    {
        "sql": "SELECT TOP 10 * FROM Employee"
    }
    
    Response:
    {
        "success": true,
        "data": [...],
        "rowCount": 10
    }
    """
    try:
        sql_query = request.data.get('sql', '').strip()
        
        if not sql_query:
            return Response({
                'success': False,
                'error': 'SQL query is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate query
        if not DatabaseService.validate_select_query(sql_query):
            return Response({
                'success': False,
                'error': 'Only SELECT queries are allowed'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Execute query
        results = DatabaseService.execute_query(sql_query)
        
        return Response({
            'success': True,
            'data': results,
            'rowCount': len(results)
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ========================================
# FILE: backend/query_api/urls.py
# ========================================
"""
URL configuration for query_api app
"""
from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.health_check, name='health_check'),
    path('test-connection/', views.test_connection, name='test_connection'),
    path('schema/', views.get_schema, name='get_schema'),
    path('query/', views.process_query, name='process_query'),
    path('test-sql/', views.test_sql, name='test_sql'),
]


# ========================================
# END OF ALL PYTHON FILES
# ========================================
