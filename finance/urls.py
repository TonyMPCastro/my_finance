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
     path('cadastro_despesa/', views.cadastro_despesa, name='cadastro_despesa'),   
     path('cadastro_recebimento/', views.cadastro_recebimento, name='cadastro_recebimento'),    
     path("despesa/editar/<int:pk>/", views.editar_despesa, name="editar_despesa"),
     path("despesa/deletar/<int:pk>/", views.deletar_despesa, name="deletar_despesa"),

]
