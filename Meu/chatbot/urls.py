from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/',views.signout, name='signout'),
    path('mypage/',views.mypage, name='mypage'),
    path('mypage/<int:diary_id>',views.mypage, name='mypage'),
    path('mypage/<int:diary_id>/delete/', views.delete, name='delete'),
    path('mypage/<int:diary_id>/edit/',views.edit, name='edit'),
    path('chat/',views.chat, name='chat'),
    path('chat2/',views.chat2, name='chat2'),
    path('chat2_2/',views.chat2_2, name='chat2_2'),
    path('chat3/',views.chat3, name='chat3'),
    path('chat/conversation/',views.conversation, name='chat_conversation'),
    path('chat2/conversation/',views.conversation, name='conversation'),
    path('chat3/conversation_2/',views.conversation_2, name='conversation_2'),
    path('explain_model/',views.explain_model, name='explain_model'),
    path('explain_web/',views.explain_web, name='explain_web'),
    path('about_us/',views.about_us, name='about_us'),
]
