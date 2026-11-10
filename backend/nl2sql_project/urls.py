# # ----------------------------------------
# # FILE: backend/nl2sql_project/urls.py
# # ----------------------------------------


# from django.contrib import admin
# from django.urls import path, include

# urlpatterns = [
#     path('admin/', admin.site.urls),              # Django admin
#     path('', include('query_api.urls')),         # Root and API paths from app
# ]
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('query_api.urls')),  # <-- add 'api/' prefix
]
