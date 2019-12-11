from django.urls import path
from .views import *

urlpatterns = [
    path('', Tasks.as_view(), name='tasks_url'),
    path('add/', TaskAdd.as_view(), name='task_add_url'),
    path('delete/', TaskDelete.as_view(), name='task_delete_url'),
    path('complite/', TaskComplited.as_view(), name='task_complite_url'),
    path('login/', Login.as_view(), name='login_url'),
    path('logout/', logout_view, name='logout_url'),
    path('register/', Register.as_view(), name='register_url'),
]