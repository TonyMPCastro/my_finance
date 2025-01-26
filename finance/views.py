from django.shortcuts import render, redirect
from django.contrib.auth import logout
import locale
from datetime import datetime, timedelta, date
import random
import json

# Define o locale para português
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

def home(request):
    if not request.user.is_authenticated:
        return redirect('/login/')  # Redireciona se não estiver logado
    # Usuários fictícios
    users = [
        {"name": "Yorgos Avramura", "country": "🇬🇷", "usage": 50, "last_login": "10 seconds ago"},
        {"name": "Avram Tsariscos", "country": "🇧🇷", "usage": 50, "last_login": "5 minutes ago"},
        {"name": "Quintin Ed", "country": "🇮🇳", "usage": 50, "last_login": "1 hour ago"},
        {"name": "Eneka Kwadwo", "country": "🇫🇷", "usage": 50, "last_login": "1 week ago"},
        {"name": "Aqquestas Tadeia", "country": "🇪🇸", "usage": 50, "last_login": "3 months ago"},
        {"name": "Fridrich David", "country": "🇩🇪", "usage": 50, "last_login": "1 year ago"},
    ]

    # Gerando os últimos 12 meses automaticamente
    meses = [(datetime.today() - timedelta(days=30*i)).strftime('%b') for i in range(11, -1, -1)]
    
    # Gerando valores aleatórios para receitas e despesas dos últimos 12 meses
    receitas = [random.randint(5000, 15000) for _ in range(12)]
    despesas = [random.randint(3000, 12000) for _ in range(12)]

    # Exemplo de dados
    categorias = ['Alimentação', 'Transporte', 'Saúde', 'Entretenimento', 'Educação']
    gastos = [200, 150, 100, 80, 120]

    categoryData = {
        "0":{
            "label": 'Gastos',
            "data": gastos,
            "backgroundColor": ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#FF9F40'],
            "hoverOffset": 4
        }
    }

    # Dados para os gráficos
    sales_data = {
        "0":{
        'label': 'Receitas',
        'data': receitas,
        'borderColor': 'green',
        'borderWidth': 2,
        'fill': 'false'
        },
        "1":{
        'label': 'Despesas',
        'data': despesas,
        'borderColor': 'red',
        'borderWidth': 2,
        'fill': 'false'
        }
    }

    # Dados para os gráficos
    sales_data = {
        "0":{
        'label': 'Receitas',
        'data': receitas,
        'borderColor': 'green',
        'borderWidth': 2,
        'fill': 'false'
        },
        "1":{
        'label': 'Despesas',
        'data': despesas,
        'borderColor': 'red',
        'borderWidth': 2,
        'fill': 'false'
        }
    }
    

    traffic_data = {
        "0": {
            "label": 'Receita',
            "data": receitas,
            "backgroundColor": 'green',
            "borderWidth": 1,
        },

        "1": {
            "label": 'Despesa',
            "data": despesas,
            "backgroundColor": 'red',
            "borderWidth": 1,
        },
    }
    
    context = {
        "users": users,
        "sales_labels": meses,
        "sales_data": json.dumps(sales_data),
        "traffic_labels": meses,
        "traffic_data": json.dumps(traffic_data) ,
        "categoryData" : categoryData,
        "categorias":categorias
    }

    return render(request, 'home.html', context)


def home_public(request):
    return render(request, "home_public.html")

def login(request):
    if request.user.is_authenticated:
        return redirect('home')  # Redireciona se não estiver logado
    return render(request, "login/login.html")

def logout_view(request):
    logout(request)
    return redirect('/login/') # Replace 'login' with the name of your login page URL

def listar_despesas(request):
    # Dados fixos das despesas (substitua com seus próprios dados)
    despesas = [
        {'categoria': 'Alimentação', 'valor': 200.00, 'descricao': 'Supermercado', 'data': '2025-01-05'},
        {'categoria': 'Transporte', 'valor': 150.00, 'descricao': 'Uber', 'data': '2025-01-10'},
        {'categoria': 'Saúde', 'valor': 100.00, 'descricao': 'Consulta médica', 'data': '2025-01-12'},
        {'categoria': 'Entretenimento', 'valor': 80.00, 'descricao': 'Cinema', 'data': '2025-01-15'},
        {'categoria': 'Educação', 'valor': 120.00, 'descricao': 'Curso online', 'data': '2025-01-18'},
        {'categoria': 'Alimentação', 'valor': 50.00, 'descricao': 'Lanche', 'data': '2025-02-01'},  # Exemplo de despesa de fevereiro
    ]

    # Data do mês atual
    hoje = date.today()
    inicio_do_mes = hoje.replace(day=1)
    fim_do_mes = hoje.replace(day=1, month=hoje.month + 1) if hoje.month < 12 else hoje.replace(day=1, month=1, year=hoje.year + 1)

    # Filtra as despesas do mês atual
    despesas_mes = [despesa for despesa in despesas if inicio_do_mes <= date.fromisoformat(despesa['data']) < fim_do_mes]

    return render(request, 'pages/contas_pagar/list.html', {
        'despesas': despesas_mes,
        'mes': hoje.strftime('%B %Y').upper()
    })



def listar_recebimentos(request):
    # Dados fixos das despesas (substitua com seus próprios dados)
    despesas = [
        {'categoria': 'Alimentação', 'valor': 200.00, 'descricao': 'Supermercado', 'data': '2025-01-05'},
        {'categoria': 'Transporte', 'valor': 150.00, 'descricao': 'Uber', 'data': '2025-01-10'},
        {'categoria': 'Saúde', 'valor': 100.00, 'descricao': 'Consulta médica', 'data': '2025-01-12'},
        {'categoria': 'Entretenimento', 'valor': 80.00, 'descricao': 'Cinema', 'data': '2025-01-15'},
        {'categoria': 'Educação', 'valor': 120.00, 'descricao': 'Curso online', 'data': '2025-01-18'},
        {'categoria': 'Alimentação', 'valor': 50.00, 'descricao': 'Lanche', 'data': '2025-02-01'},  # Exemplo de despesa de fevereiro
    ]

    # Data do mês atual
    hoje = date.today()
    inicio_do_mes = hoje.replace(day=1)
    fim_do_mes = hoje.replace(day=1, month=hoje.month + 1) if hoje.month < 12 else hoje.replace(day=1, month=1, year=hoje.year + 1)

    # Filtra as despesas do mês atual
    despesas_mes = [despesa for despesa in despesas if inicio_do_mes <= date.fromisoformat(despesa['data']) < fim_do_mes]

    return render(request, 'pages/recebimentos/list.html', {
        'despesas': despesas_mes,
        'mes': hoje.strftime('%B %Y').upper()
    })
