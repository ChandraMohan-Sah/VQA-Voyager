from django.contrib import admin
from django.urls import path, include

# Add media configuration to your URL patterns
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('chatbot_app.api.urls')),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
