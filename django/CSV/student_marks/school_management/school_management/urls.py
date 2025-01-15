from django.contrib import admin
from django.urls import path, include
from school_app.views import home  # Import the home view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # Map root URL to the home view
    path('', include('school_app.urls')),  # Include school_app URLs
]