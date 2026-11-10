# ----------------------------------------
# FILE: backend/query_api/views.py
# ----------------------------------------
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .database_service import DatabaseService
from .ai_service import AIService

@api_view(['GET'])
def home(request):
    return Response({"message": "NL2SQL API is running!"})

@api_view(['GET'])
def health_check(request):
    return Response({
        'status': 'OK',
        'message': 'Django NL2SQL API is running',
        'ai_provider': settings.AI_PROVIDER
    })

@api_view(['GET'])
def test_connection(request):
    result = DatabaseService.test_connection()
    
    if result['success']:
        return Response(result)
    else:
        return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_schema(request):
    try:
        schema = DatabaseService.get_database_schema()
        return Response({'success': True, 'schema': schema})
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def process_query(request):
    try:
        question = request.data.get('question', '').strip()
        
        if not question:
            return Response({'success': False, 'error': 'Question is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        schema = DatabaseService.get_database_schema()
        sql_query = AIService.natural_language_to_sql(question, schema)
        
        if not DatabaseService.validate_select_query(sql_query):
            return Response({
                'success': False,
                'error': 'Only SELECT queries are allowed for security',
                'generatedQuery': sql_query
            }, status=status.HTTP_400_BAD_REQUEST)
        
        results = DatabaseService.execute_query(sql_query)
        
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
    try:
        sql_query = request.data.get('sql', '').strip()
        
        if not sql_query:
            return Response({'success': False, 'error': 'SQL query is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not DatabaseService.validate_select_query(sql_query):
            return Response({'success': False, 'error': 'Only SELECT queries are allowed'}, status=status.HTTP_400_BAD_REQUEST)
        
        results = DatabaseService.execute_query(sql_query)
        
        return Response({'success': True, 'data': results, 'rowCount': len(results)})
        
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)