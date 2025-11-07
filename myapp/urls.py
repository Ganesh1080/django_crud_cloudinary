from django.urls import path
from . import views
urlpatterns = [
    path('userlist/',views.userlist),
    path('single_user/<int:user_id>',views.partial_user),
    path('register/',views.new_register),
    path('update/<int:user_id>',views.update),
    path('delete/<int:user_id>',views.delete),
    
]
