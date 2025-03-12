from django.urls import path
from .import views

urlpatterns = [
    path('', views.chatbot_view, name='chatbot'),
    path('upload/', views.upload_image, name='upload_image'),
    path('clear/', views.ClearChathistory, name="clear-chat-history"),
    path('generate-audio/', views.generate_audio, name='generate_audio'),
    path('upload_audio/', views.upload_audio, name='upload_audio'),
    path('select-object/', views.select_object, name='select_object'),  
    path('quick_qa/', views.quick_qa, name='quick-qa')
] 

 