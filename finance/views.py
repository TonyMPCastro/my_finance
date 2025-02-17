import random
import json
import locale
import pprint  # Módulo para imprimir dicionários de forma organizada

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from datetime import datetime, timedelta, date
from django.contrib.auth.models import User
from django.contrib import messages
from . import forms
from django.views.decorators.cache import never_cache
from . import models
from collections import defaultdict
from datetime import datetime, date
from decimal import Decimal
from django.db.models import Q, Sum

# Define o locale para português
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

@login_required
@never_cache
def home(request):
    
    today = datetime.today()

    movements = models.MovementFinancial.objects.filter(due_at__year=today.year, due_at__month=today.month)
    # Criar dicionário para agrupar os movimentos por categoria e somar os valores
    total_general = Decimal(0)

    for movement in movements:
        if(movement.category.type_category.id == 2):
            total_general -= movement.value  # Soma geral
        else:
            total_general += movement.value  # Soma geral

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

    entradas = models.MovementFinancial.objects.filter(category__type_category=1).aggregate(total=Sum('value'))
    saidas = models.MovementFinancial.objects.filter(category__type_category=2).aggregate(total=Sum('value'))
    
    if entradas['total']:
        valor_total_entradas =  entradas['total'] 
    else:
        valor_total_entradas =  0  # Lida com o caso de não haver registros

    if saidas['total']:
        valor_total_saidas = saidas['total'] 
    else:
        valor_total_saidas = 0  # Lida com o caso de não haver registros


    entradas_mes = models.MovementFinancial.objects.filter(category__type_category=1, due_at__year=today.year, due_at__month=today.month).aggregate(total=Sum('value'))

    if entradas_mes['total']:
        valor_entradas_mes = entradas_mes['total'] 
    else:
        valor_entradas_mes = 0  # Lida com o caso de não haver registros
    
    despesas_mes = models.MovementFinancial.objects.filter(category__type_category=2, due_at__year=today.year, due_at__month=today.month).aggregate(total=Sum('value'))

    if despesas_mes['total']:
        valor_despesas_mes = despesas_mes['total'] 
    else:
        valor_despesas_mes = 0  # Lida com o caso de não haver registros

    thirty_days_from_now = today + timedelta(days=30)

    despesas_30_dias = models.MovementFinancial.objects.filter(
        category__type_category=2,
        due_at__range=(today, thirty_days_from_now)  # Filtra entre hoje e 30 dias no futuro
    ).aggregate(total=Sum('value'))

    if despesas_30_dias['total']:
        despesas_30_dias = despesas_30_dias['total'] 
    else:
        despesas_30_dias = 0  # Lida com o caso de não haver registros


    saldo_atual = valor_total_entradas - valor_total_saidas

    saldo_mes = valor_entradas_mes - valor_despesas_mes



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
        "movements": movements,
        "sales_labels": meses,
        "sales_data": json.dumps(sales_data),
        "traffic_labels": meses,
        "traffic_data": json.dumps(traffic_data) ,
        "categoryData" : categoryData,
        "categorias":categorias,
        'saldo_atual': saldo_atual,
        'saldo_mes': saldo_mes,
        'valor_despesas_mes': valor_despesas_mes,
        'despesas_30_dias':despesas_30_dias,
        'total_general': total_general
    }

    return render(request, 'home.html', context)

def home_public(request):
    return render(request, "home_public.html")

def login(request):
    if request.user.is_authenticated:
        return redirect('home')  # Redireciona se não estiver logado
    return render(request, "login/login.html")

@login_required
@never_cache
def logout_view(request):
    logout(request)
    return redirect('/login/') # Replace 'login' with the name of your login page URL

@login_required
@never_cache
def listar_despesas(request):

    today = datetime.today()
    despesas = models.MovementFinancial.objects.filter(category__type_category=2)

    categories_list = models.Category.objects.filter(type_category=2)  # Pegando todas as categorias

    # Pegando filtros da request
    start_date = request.POST.get("start_date")  # Data inicial (due_at)
    end_date = request.POST.get("end_date")  # Data final (due_at)
    start_payment = request.POST.get("start_payment")  # Data inicial (payment_at)
    end_payment = request.POST.get("end_payment")  # Data final (payment_at)
    categorys = request.POST.getlist("category")  # Lista de categorias selecionadas

    titulo = "Despesas"

    # Se nenhum filtro for aplicado, usar mês atual
    if not (start_date or end_date or start_payment or end_payment or categorys):
        despesas = despesas.filter(due_at__year=today.year, due_at__month=today.month)
        
        # Data do mês atual
        hoje = date.today()
        titulo = "Despesas de "+hoje.strftime('%B %Y').upper()
    else:
        # Filtro por intervalo de data de vencimento (due_at)
        if start_date and end_date:
            despesas = despesas.filter(due_at__range=[start_date, end_date])
        elif start_date:
            despesas = despesas.filter(due_at__gte=start_date)
        elif end_date:
            despesas = despesas.filter(due_at__lte=end_date)

        # Filtro por intervalo de data de pagamento (payment_at)
        if start_payment and end_payment:
            despesas = despesas.filter(payment_at__range=[start_payment, end_payment])
        elif start_payment:
            despesas = despesas.filter(payment_at__gte=start_payment)
        elif end_payment:
            despesas = despesas.filter(payment_at__lte=end_payment)

        # Filtro por categorias (caso seja enviado)
        if categorys:
            despesas = despesas.filter(category_id__in=categorys)

    # Criar dicionário para agrupar os movimentos por categoria e somar os valores
    grouped_movements = defaultdict(lambda: {"movements": [], "total": Decimal(0)})
    total_general = Decimal(0)

    for movement in despesas:
        category_name = movement.category.name
        grouped_movements[category_name]["movements"].append(movement)
        grouped_movements[category_name]["total"] += movement.value
        total_general += movement.value  # Soma geral

    # 🔹 Exibir no terminal do servidor
    #pprint.pprint(dict(grouped_movements))

    return render(request, 'pages/contas_pagar/list.html', {
        "grouped_movements": dict(grouped_movements),
        "total_general": total_general,
        "categories": categories_list,
        'categorys' :categorys,
        'titulo': titulo
    })

@login_required
@never_cache
def listar_recebimentos(request):
    today = datetime.today()
    recebimentos = models.MovementFinancial.objects.filter(category__type_category=1)

    categories_list = models.Category.objects.filter(type_category=1)  # Pegando todas as categorias

    # Pegando filtros da request
 
    start_payment = request.POST.get("start_payment")  # Data inicial (payment_at)
    end_payment = request.POST.get("end_payment")  # Data final (payment_at)
    categorys = request.POST.getlist("category")  # Lista de categorias selecionadas

    titulo = "Recebimentos"

    # Se nenhum filtro for aplicado, usar mês atual
    if not (start_payment or end_payment or categorys):
        recebimentos = recebimentos.filter(due_at__year=today.year, due_at__month=today.month)
        
        # Data do mês atual
        hoje = date.today()
        titulo = "Recebimentos de "+hoje.strftime('%B %Y').upper()
    else:
        # Filtro por intervalo de data de pagamento (payment_at)
        if start_payment and end_payment:
            recebimentos = recebimentos.filter(payment_at__range=[start_payment, end_payment])
        elif start_payment:
            recebimentos = recebimentos.filter(payment_at__gte=start_payment)
        elif end_payment:
            recebimentos = recebimentos.filter(payment_at__lte=end_payment)

        # Filtro por categorias (caso seja enviado)
        if categorys:
            recebimentos = recebimentos.filter(category_id__in=categorys)

    # Criar dicionário para agrupar os movimentos por categoria e somar os valores
    grouped_movements = defaultdict(lambda: {"movements": [], "total": Decimal(0)})
    total_general = Decimal(0)

    for movement in recebimentos:
        category_name = movement.category.name
        grouped_movements[category_name]["movements"].append(movement)
        grouped_movements[category_name]["total"] += movement.value
        total_general += movement.value  # Soma geral

    # 🔹 Exibir no terminal do servidor
    #pprint.pprint(dict(grouped_movements))

    return render(request, 'pages/recebimentos/list.html', {
        "grouped_movements": dict(grouped_movements),
        "total_general": total_general,
        "categories": categories_list,
        'categorys' :categorys,
        'titulo': titulo
    })


@login_required
@never_cache
def listar_extrato(request):
    today = datetime.today()
    recebimentos = models.MovementFinancial.objects.filter(due_at__year=today.year)

    # Pegando filtros da request
    start_payment = request.POST.get("start_payment")  # Data inicial (payment_at)
    end_payment = request.POST.get("end_payment")  # Data final (payment_at)

    titulo = "Extrato"

    # Se nenhum filtro for aplicado, usar mês atual
    if not (start_payment or end_payment):
        recebimentos = recebimentos.filter(due_at__year=today.year, due_at__month=today.month)
        
        # Data do mês atual
        hoje = date.today()
        titulo = "Extrato de "+hoje.strftime('%B %Y').upper()
    else:
        # Filtro por intervalo de data de pagamento (payment_at)
        if start_payment and end_payment:
            recebimentos = recebimentos.filter(payment_at__range=[start_payment, end_payment])
            recebimentos = recebimentos.filter(due_at__range=[start_payment, end_payment])
        elif start_payment:
            recebimentos = recebimentos.filter(payment_at__gte=start_payment)
            recebimentos = recebimentos.filter(due_at__gte=start_payment)
        elif end_payment:
            recebimentos = recebimentos.filter(payment_at__lte=end_payment)
            recebimentos = recebimentos.filter(due_at__lte=end_payment)

    # Criar dicionário para agrupar os movimentos por categoria e somar os valores
    total_general = Decimal(0)

    for movement in recebimentos:
        if(movement.category.type_category.id == 2):
            total_general -= movement.value  # Soma geral
        else:
            total_general += movement.value  # Soma geral

    # 🔹 Exibir no terminal do servidor
    #pprint.pprint(dict(grouped_movements))

    return render(request, 'pages/relatorios/extrato.html', {
        "movements": recebimentos,
        "total_general": total_general,
        'titulo': titulo
    })

def cadastro(request):
    if request.method == "POST":
        form = forms.CadastroForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['senha']
            )
            messages.success(request, "Cadastro realizado com sucesso!")
            return redirect('login')  # Altere para a URL de login

    else:
        form = forms.CadastroForm()

    return render(request, "cadastro/form.html", {"form": form})


@login_required
@never_cache
def cadastro_despesa(request):
    if request.method == "POST":
        form = forms.MovementExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Despesa cadastrada com sucesso!")
            return redirect('listar_despesas')  # Redireciona para uma lista de produtos
        else:
            messages.error(request, "Erro ao cadastrar despesa.")
    else:
        form = forms.MovementExpenseForm()

    return render(request, "pages/contas_pagar/form.html", {"form": form})

@login_required
@never_cache
def editar_despesa(request, pk):
    despesa = get_object_or_404(models.MovementFinancial, pk=pk)

    if request.method == "POST":
        form = forms.MovementExpenseForm(request.POST, instance=despesa)
        if form.is_valid():
            form.save()
            messages.success(request, "Despesa atualizada com sucesso!")
            return redirect("listar_despesas")  # Redireciona para a lista
        else:
            messages.error(request, "Erro ao atualizar despesa.")
    else:
        form = forms.MovementExpenseForm(instance = despesa)  # Preenche com os dados atuais

    return render(request, "pages/contas_pagar/form.html", {"form": form})


@login_required
@never_cache
def deletar_despesa(request, pk):

    despesa = get_object_or_404(models.MovementFinancial, pk=pk)

    if request.method == "POST":
        despesa.delete()
        messages.success(request, "Despesa excluída com sucesso!")
        return redirect("listar_despesas")

    return render(request, "pages/contas_pagar/confirm_delete.html", {"despesa": despesa})



@login_required
@never_cache
def cadastro_recebimento(request):
    if request.method == "POST":
        form = forms.MovementExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Recebimento cadastrada com sucesso!")
            return redirect('listar_listar_recebimentosdespesas')  # Redireciona para uma lista de produtos
        else:
            messages.error(request, "Erro ao cadastrar despesa.")
    else:
        form = forms.MovementExpenseForm()

    return render(request, "pages/recebimentos/form.html", {"form": form})

@login_required
@never_cache
def editar_despesa(request, pk):
    despesa = get_object_or_404(models.MovementFinancial, pk=pk)

    if request.method == "POST":
        form = forms.MovementExpenseForm(request.POST, instance=despesa)
        if form.is_valid():
            form.save()
            messages.success(request, "Despesa atualizada com sucesso!")
            return redirect("listar_despesas")  # Redireciona para a lista
        else:
            messages.error(request, "Erro ao atualizar despesa.")
    else:
        form = forms.MovementExpenseForm(instance = despesa)  # Preenche com os dados atuais

    return render(request, "pages/contas_pagar/form.html", {"form": form})


@login_required
@never_cache
def deletar_despesa(request, pk):

    despesa = get_object_or_404(models.MovementFinancial, pk=pk)

    if request.method == "POST":
        despesa.delete()
        messages.success(request, "Despesa excluída com sucesso!")
        return redirect("listar_despesas")

    return render(request, "pages/contas_pagar/confirm_delete.html", {"despesa": despesa})
