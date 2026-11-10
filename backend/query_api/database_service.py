# ----------------------------------------
# FILE: backend/query_api/database_service.py
# ----------------------------------------
# import pyodbc
# from django.conf import settings

# class DatabaseService:
    
#     @staticmethod
#     def get_connection_string():
#         config = settings.SQL_SERVER_CONFIG
#         conn_string = (
#             f"DRIVER={config['DRIVER']};"
#             f"SERVER={config['SERVER']};"
#             f"DATABASE={config['DATABASE']};"
#             f"UID={config['UID']};"
#             f"PWD={config['PWD']};"
#             f"TrustServerCertificate={config['TrustServerCertificate']};"
#             f"Encrypt={config['Encrypt']};"
#         )
#         return conn_string

# ----------------------------------------
# FILE: backend/query_api/database_service.py
# ----------------------------------------

import pyodbc
from django.conf import settings


class DatabaseService:

    @staticmethod
    def get_connection_string():
        config = settings.SQL_SERVER_CONFIG

        # If UID is provided → use SQL Authentication
        if config.get("UID") and config.get("PWD"):
            conn_string = (
                f"DRIVER={config['DRIVER']};"
                f"SERVER={config['SERVER']};"
                f"DATABASE={config['DATABASE']};"
                f"UID={config['UID']};"
                f"PWD={config['PWD']};"
                f"TrustServerCertificate={config['TrustServerCertificate']};"
                f"Encrypt={config['Encrypt']};"
            )
        else:
            # Otherwise use Windows Authentication
            conn_string = (
                f"DRIVER={config['DRIVER']};"
                f"SERVER={config['SERVER']};"
                f"DATABASE={config['DATABASE']};"
                f"Trusted_Connection=yes;"
                f"TrustServerCertificate={config['TrustServerCertificate']};"
                f"Encrypt={config['Encrypt']};"
            )

        return conn_string
    
    @staticmethod
    def get_database_schema():
        try:
            conn_string = DatabaseService.get_connection_string()
            conn = pyodbc.connect(conn_string)
            cursor = conn.cursor()
            
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
        try:
            conn_string = DatabaseService.get_connection_string()
            conn = pyodbc.connect(conn_string)
            cursor = conn.cursor()
            
            cursor.execute(sql_query)
            columns = [column[0] for column in cursor.description]
            rows = cursor.fetchall()
            
            results = []
            for row in rows:
                result_dict = {}
                for i, column in enumerate(columns):
                    value = row[i]
                    if value is None:
                        result_dict[column] = None
                    elif isinstance(value, (int, float, str, bool)):
                        result_dict[column] = value
                    else:
                        result_dict[column] = str(value)
                results.append(result_dict)
            
            cursor.close()
            conn.close()
            
            return results
            
        except Exception as e:
            raise Exception(f"Failed to execute query: {str(e)}")
    
    @staticmethod
    def validate_select_query(sql_query):
        sql_upper = sql_query.strip().upper()
        
        if not sql_upper.startswith('SELECT'):
            return False
        
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
        try:
            conn_string = DatabaseService.get_connection_string()
            conn = pyodbc.connect(conn_string)
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
            conn.close()
            
            return {'success': True, 'message': 'Database connection successful'}
            
        except Exception as e:
            return {'success': False, 'message': f'Database connection failed: {str(e)}'}