from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('transaction/<str:pk>/', views.transaction_detail, name='transaction_detail'),
    path('transaction/<str:pk>/update-status/', views.update_status, name='update_status'),
    path('transaction/<str:pk>/update-flag/', views.update_flag, name='update_flag'),
    path('add-transaction/', views.add_transaction, name='add_transaction'),
    path('all-history/', views.all_transaction_history, name='all_history'),
    path('delete-transaction/<str:pk>/', views.delete_transaction, name='delete_transaction'),
    path('delete-transactions/', views.multiple_delete_transaction, name='multiple_delete_transaction'),
    path('analytics/', views.analytics_view, name='analytics'),
]

