from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [ 
    
     path('', views.home_public, name='home_public'),
     path('home/', views.home, name='home'),     
     path('login/', auth_views.LoginView.as_view(template_name='login/login.html'), name='login'),
     path('logout/', views.logout_view , name='logout'),  # Rota para logout     
     path('despesas/', views.listar_despesas, name='listar_despesas'),
     path('recebimentos/', views.listar_recebimentos, name='listar_recebimentos'),     
     path('cadastro/', views.cadastro, name='cadastro'),  
     path('extrato/', views.listar_extrato, name='listar_extrato'),    
]
