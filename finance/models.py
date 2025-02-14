from django.db import models

class Bank(models.Model):
    is_active   = models.BooleanField(default=True, verbose_name='Ativo')
    name        = models.CharField(null=False, blank=False,max_length=255, verbose_name='Nome')
    code        = models.CharField(null=False, blank=False,max_length=100, verbose_name='Codigo')
    created_at  = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at  = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        ordering        = ['name']
        verbose_name    = 'Banco'

    def __str__(self):
        return self.name

class PaymentMethod(models.Model):
    is_active   = models.BooleanField(default=True, verbose_name='Ativo')
    name        = models.CharField(null=False, blank=False, max_length=255, verbose_name='Nome')
    created_at  = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at  = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        ordering        = ['name']
        verbose_name    = 'Forma de pagamento'

    def __str__(self):
        return self.name
    
class TypeMovement(models.Model):
    name        = models.CharField(null=False, blank=False, max_length=255, verbose_name='Nome')

    class Meta:
        ordering        = ['name']
        verbose_name    = 'Tipo de Movimentação'

    def __str__(self):
        return self.name

class Category(models.Model):
    name             = models.CharField(null=False, blank=False, max_length=255, verbose_name='Nome')
    type_category    = models.ForeignKey(TypeMovement, on_delete=models.PROTECT, related_name='categorys', verbose_name='Tipo de Movimentação')
    is_active        = models.BooleanField(default=True, verbose_name='Ativo')
    description      = models.TextField(null=True, blank=True, verbose_name='Descrição')
    created_at       = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at       = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        ordering        = ['name']
        verbose_name    = 'Categoria'

    def __str__(self):
        return self.name

class StatusMovement(models.Model):
    name        = models.CharField(null=False, blank=False, max_length=255, verbose_name='Nome')
    type        = models.ForeignKey(TypeMovement, on_delete=models.PROTECT, related_name='status', verbose_name='Tipo de Movimentação')

    class Meta:
        ordering        = ['name']
        verbose_name    = 'Status'

    def __str__(self):
        return self.name

class MovementFinancial(models.Model):
    bank                = models.ForeignKey(Bank, on_delete=models.PROTECT, related_name='movements', verbose_name='Banco')
    status              = models.ForeignKey(StatusMovement, on_delete=models.PROTECT, related_name='movements', verbose_name='Status')
    category            = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='movements', verbose_name='Categoria')
    value               = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor')
    value_payment       = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2, verbose_name='Valor do Pagamento')
    description         = models.TextField(null=False, blank=False, verbose_name='Descrição')
    file                = models.TextField(null=True, blank=True, verbose_name='Arquivo')
    is_installment      = models.BooleanField(default=False, verbose_name='Parcelamento')
    installment         = models.IntegerField(null=True, blank=True, verbose_name='Parcela')
    related_id          = models.IntegerField(null=True, blank=True, verbose_name='Movimentações Relacionadas')
    payment_at          = models.DateField(null=True, blank=True, verbose_name='Data de Pagamento')
    due_at              = models.DateField(null=False, blank=False, verbose_name='Data de Vencimento')
    created_at          = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at          = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        ordering = ['due_at']
        verbose_name = 'Movimentações'

    def __str__(self):
        return self.description
