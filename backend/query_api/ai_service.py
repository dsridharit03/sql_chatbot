# # ----------------------------------------
# # FILE: backend/query_api/ai_service.py
# # ----------------------------------------
# from django.conf import settings
# from openai import OpenAI
# from anthropic import Anthropic

# class AIService:
    
#     @staticmethod
#     def natural_language_to_sql(question, database_schema):
#         provider = settings.AI_PROVIDER.lower()
        
#         if provider == 'openai':
#             return AIService._openai_to_sql(question, database_schema)
#         elif provider == 'anthropic':
#             return AIService._anthropic_to_sql(question, database_schema)
#         else:
#             raise Exception(f"Unknown AI provider: {provider}")
    
#     @staticmethod
#     def _openai_to_sql(question, database_schema):
#         try:
#             client = OpenAI(api_key=settings.OPENAI_API_KEY)
            
#             prompt = f"""You are a SQL expert. Convert the following natural language question to a SQL Server query.

# {database_schema}

# Question: {question}

# Important:
# 1. Return ONLY the SQL query, no explanations or markdown
# 2. Use TOP instead of LIMIT for SQL Server
# 3. Ensure the query is safe and read-only (SELECT only)
# 4. Use proper SQL Server syntax
# 5. Do not include code blocks or formatting

# SQL Query:"""
            
#             response = client.chat.completions.create(
#                 model="gpt-4",
#                 messages=[
#                     {"role": "system", "content": "You are a SQL expert that converts natural language to SQL Server queries. Return only the SQL query without any explanation."},
#                     {"role": "user", "content": prompt}
#                 ],
#                 temperature=0,
#                 max_tokens=500
#             )
            
#             sql_query = response.choices[0].message.content.strip()
#             sql_query = sql_query.replace('```sql', '').replace('```', '').strip()
            
#             return sql_query
            
#         except Exception as e:
#             raise Exception(f"OpenAI API error: {str(e)}")
    
#     @staticmethod
#     def _anthropic_to_sql(question, database_schema):
#         try:
#             client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
            
#             prompt = f"""You are a SQL expert. Convert the following natural language question to a SQL Server query.

# {database_schema}

# Question: {question}

# Important:
# 1. Return ONLY the SQL query, no explanations or markdown
# 2. Use TOP instead of LIMIT for SQL Server
# 3. Ensure the query is safe and read-only (SELECT only)
# 4. Use proper SQL Server syntax
# 5. Do not include code blocks or formatting

# SQL Query:"""
            
#             message = client.messages.create(
#                 model="claude-sonnet-4-20250514",
#                 max_tokens=1000,
#                 temperature=0,
#                 messages=[{"role": "user", "content": prompt}]
#             )
            
#             sql_query = message.content[0].text.strip()
#             sql_query = sql_query.replace('```sql', '').replace('```', '').strip()
            
#             return sql_query
            
#         except Exception as e:
#             raise Exception(f"Anthropic API error: {str(e)}")

# ----------------------------------------
# FILE: backend/query_api/ai_service.py
# ----------------------------------------
from django.conf import settings
import openai
from anthropic import Anthropic

class AIService:

    @staticmethod
    def natural_language_to_sql(question, database_schema):
        provider = settings.AI_PROVIDER.lower()

        if provider == 'openai':
            return AIService._openai_to_sql(question, database_schema)
        elif provider == 'anthropic':
            return AIService._anthropic_to_sql(question, database_schema)
        else:
            raise Exception(f"Unknown AI provider: {provider}")

    @staticmethod
    def _openai_to_sql(question, database_schema):
        try:
            # ✅ Correct way to set API key for OpenAI
            openai.api_key = settings.OPENAI_API_KEY

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

            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a SQL expert that converts natural language to SQL Server queries. Return only the SQL query without any explanation."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0,
                max_tokens=500
            )

            sql_query = response.choices[0].message.content.strip()
            sql_query = sql_query.replace('```sql', '').replace('```', '').strip()

            return sql_query

        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")

    @staticmethod
    def _anthropic_to_sql(question, database_schema):
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
                messages=[{"role": "user", "content": prompt}]
            )

            sql_query = message.content[0].text.strip()
            sql_query = sql_query.replace('```sql', '').replace('```', '').strip()

            return sql_query

        except Exception as e:
            raise Exception(f"Anthropic API error: {str(e)}")
