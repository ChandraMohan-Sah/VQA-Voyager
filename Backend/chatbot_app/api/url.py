from django.urls import path
from . import views

urlpatterns = [
    path('', views.chatbot_view, name='chatbot'),
    path('upload', views.upload_image, name='upload_image'),
    path('clear', views.clear_chat_history, name='clear-chat-history'),
    path('inference-bart', views.inference_bart, name='inference_bart'),
    path('inference-yolo', views.inference_yolo, name='inference_yolo'),
    path('download-chat', views.download_chat, name='download_chat'),
    path('open-camera', views.open_camera, name='open_camera'),
    path('voice-input', views.voice_input, name='voice_input'),
]
