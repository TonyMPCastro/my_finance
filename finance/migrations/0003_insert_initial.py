# Generated by Django 5.0 on 2025-02-14 03:12

from django.db import migrations, models

def insert_default_data(apps, schema_editor):
    Bank = apps.get_model('finance', 'Bank')
    PaymentMethod = apps.get_model('finance', 'PaymentMethod')
    TypeMovement = apps.get_model('finance', 'TypeMovement')
    Category = apps.get_model('finance', 'Category')
    StatusMovement = apps.get_model('finance', 'StatusMovement')

    # Inserindo Bancos Padrões
    Bank.objects.get_or_create(name='Banco do Brasil', code='001')
    Bank.objects.get_or_create(name='Bradesco', code='237')
    Bank.objects.get_or_create(name='Itaú', code='341')
    Bank.objects.get_or_create(name='Caixa Econômica Federal', code='104')

    # Inserindo Formas de Pagamento Padrões
    PaymentMethod.objects.get_or_create(name='Cartão de Crédito')
    PaymentMethod.objects.get_or_create(name='Cartão de Débito')
    PaymentMethod.objects.get_or_create(name='Boleto')
    PaymentMethod.objects.get_or_create(name='Transferência')

    # Inserindo Tipos de Movimentação Padrões
    receita, _ = TypeMovement.objects.get_or_create(name='Receita')
    despesa, _ = TypeMovement.objects.get_or_create(name='Despesa')

    # Inserindo Categorias Padrões
    Category.objects.get_or_create(name='Alimentação', type_category=despesa)
    Category.objects.get_or_create(name='Educação', type_category=despesa)
    Category.objects.get_or_create(name='Salário', type_category=receita)
    Category.objects.get_or_create(name='Investimentos', type_category=receita)

    # Inserindo Status de Movimentação Padrões
    StatusMovement.objects.get_or_create(name='Pendente', type=despesa)
    StatusMovement.objects.get_or_create(name='Pago', type=despesa)
    StatusMovement.objects.get_or_create(name='Recebido', type=receita)

class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0002_alter_typemovement_options_and_more'),
    ]

    operations = [
        migrations.RunPython(insert_default_data),
    ]
