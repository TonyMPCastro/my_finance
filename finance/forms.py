from django import forms
from django.contrib.auth.models import User
import re
import pprint  # Módulo para imprimir dicionários de forma organizada
from django.core.validators import EmailValidator
from . import models
from django.utils import timezone



class CadastroForm(forms.ModelForm):
    senha = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'}), required=True, min_length=8)  # Senha obrigatória, mínimo 8 caracteres
    confirmar_senha = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirme a senha'}), required=True)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'}), required=True, error_messages={'required': 'Este campo é obrigatório.', 'invalid': 'Digite um endereço de e-mail válido.'})  # Email is now required and unique

    class Meta:
        model = User
        fields = ['username', 'first_name']  # Include the fields you want
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome de usuário', }),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome completo'}),
        }

        labels = {  # Optional: Customize labels
            'username': 'Nome de usuário',
            'first_name': 'Nome',
        }
        help_texts = {  # Optional: Add help text
            'username': 'Nome de usuário valido'
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nome de usuário já está em uso.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        validator = EmailValidator()
        try:
            validator(email)  # Verifica se o email é válido
        except forms.ValidationError:
            raise forms.ValidationError("Este endereço de e-mail não é válido.")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este e-mail já está cadastrado.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get("senha")
        confirmar_senha = cleaned_data.get("confirmar_senha")

        if senha and confirmar_senha and senha != confirmar_senha:
            self.add_error('confirmar_senha', "As senhas não coincidem.")

        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["senha"]) # Hash da senha
        if commit:
            user.save()
        return user

class MovementPaymentForm(forms.ModelForm):

    value_payment = forms.CharField(  # Pode ser DecimalField, mas TextInput ajuda na máscara
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'R$ 0,00', 'id': 'value_generic'}),
        required=False
    )


    value = forms.CharField(  # Pode ser DecimalField, mas TextInput ajuda na máscara
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'R$ 0,00', 'id': 'value_generic'})
    )

    due_at = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        input_formats=['%Y-%m-%d']
    )

    payment_at = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        input_formats=['%Y-%m-%d'],
        required=False
    )

    class Meta:
        model = models.MovementFinancial
        fields = ['description', 'category', 'bank', 'value', 'value_payment', 'file',  'status', 'due_at',  'payment_at', 'is_installment']
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'value': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'bank': forms.Select(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_value(self):
        """Remove 'R$', pontos e ajusta vírgula para ponto antes de salvar"""
        value = self.cleaned_data['value']

        # Remove tudo que não for número, vírgula ou ponto
        value = re.sub(r"[^\d,]", "", value)

        # Substitui a vírgula decimal por ponto (padrão Python)
        value = value.replace(",", ".")

        try:
            return float(value)  # Converte para número decimal
        except ValueError:
            raise forms.ValidationError("Insira um valor numérico válido.")
        
    def clean_value_payment(self):
        """Remove 'R$', pontos e ajusta vírgula para ponto antes de salvar"""
        value = self.cleaned_data['value_payment']

        # Remove tudo que não for número, vírgula ou ponto
        value = re.sub(r"[^\d,]", "", value)

        # Se o valor estiver vazio, retorna None (ou pode retornar 0 se preferir)
        if not value.strip():
            return None  # Ou return 0 se quiser um valor padrão

        # Substitui a vírgula decimal por ponto (padrão Python)
        value = value.replace(",", ".")

        try:
            return float(value)  # Converte para número decimal
        except ValueError:
            raise forms.ValidationError("Insira um valor numérico válido.")
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

         # Define a data de hoje como valor padrão
        today = timezone.now().date()  # Obtém a data atual (sem a parte de hora)

        # Definindo valores padrão para os campos
        self.fields['value'].initial = 'R$ 0,00'  # Valor padrão no campo 'value'
        self.fields['due_at'].initial = today.strftime('%Y-%m-%d')   # Data padrão para 'due_at'

        self.fields['bank'].initial = '3'  # Valor padrão no campo 'value'
        self.fields['status'].initial = '2'   # Data padrão para 'due_at'
        
        # Filtra categorias com tipo=1
        self.fields['category'].queryset = models.Category.objects.filter(type_category=1)
        self.fields['status'].queryset = models.StatusMovement.objects.filter(type=1)

        # Certifique-se de formatar as datas corretamente ao carregar o formulário
        if self.instance.pk:  # Verifique se a instância já existe (edição)
            if self.instance.due_at:
                self.initial['due_at'] = self.instance.due_at.strftime('%Y-%m-%d')  # Formato esperado
            if self.instance.payment_at:
                self.initial['payment_at'] = self.instance.payment_at.strftime('%Y-%m-%d')  # Formato esperado
             # Formatação do valor monetário ao carregar o formulário (edição)
            if self.instance.value_payment:
                formatted_value = "R$ {:,.2f}".format(self.instance.value_payment).replace(",", "X").replace(".", ",").replace("X", ".")
                self.initial['value_payment'] = formatted_value  # Exibe o valor no formato correto
            if self.instance.value:
                formatted_value = "R$ {:,.2f}".format(self.instance.value).replace(",", "X").replace(".", ",").replace("X", ".")
                self.initial['value'] = formatted_value  # Exibe o valor no formato correto

class MovementExpenseForm(forms.ModelForm):

    value_payment = forms.CharField(  # Pode ser DecimalField, mas TextInput ajuda na máscara
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'R$ 0,00', 'id': 'value_generic'}),
        required=False
    )


    value = forms.CharField(  # Pode ser DecimalField, mas TextInput ajuda na máscara
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'R$ 0,00', 'id': 'value_generic'})
    )

    due_at = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        input_formats=['%Y-%m-%d']
    )

    payment_at = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        input_formats=['%Y-%m-%d'],
        required=False
    )

    class Meta:
        model = models.MovementFinancial
        fields = ['description', 'category', 'bank', 'value', 'value_payment', 'file',  'status', 'due_at',  'payment_at', 'is_installment']
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'value': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'bank': forms.Select(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_value(self):
        """Remove 'R$', pontos e ajusta vírgula para ponto antes de salvar"""
        value = self.cleaned_data['value']

        # Remove tudo que não for número, vírgula ou ponto
        value = re.sub(r"[^\d,]", "", value)

        # Substitui a vírgula decimal por ponto (padrão Python)
        value = value.replace(",", ".")

        try:
            return float(value)  # Converte para número decimal
        except ValueError:
            raise forms.ValidationError("Insira um valor numérico válido.")
        
    def clean_value_payment(self):
        """Remove 'R$', pontos e ajusta vírgula para ponto antes de salvar"""
        value = self.cleaned_data['value_payment']

        # Remove tudo que não for número, vírgula ou ponto
        value = re.sub(r"[^\d,]", "", value)

        # Se o valor estiver vazio, retorna None (ou pode retornar 0 se preferir)
        if not value.strip():
            return None  # Ou return 0 se quiser um valor padrão

        # Substitui a vírgula decimal por ponto (padrão Python)
        value = value.replace(",", ".")

        try:
            return float(value)  # Converte para número decimal
        except ValueError:
            raise forms.ValidationError("Insira um valor numérico válido.")
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

         # Define a data de hoje como valor padrão
        today = timezone.now().date()  # Obtém a data atual (sem a parte de hora)

        # Definindo valores padrão para os campos
        self.fields['value'].initial = 'R$ 0,00'  # Valor padrão no campo 'value'
        self.fields['due_at'].initial = today.strftime('%Y-%m-%d')   # Data padrão para 'due_at'

        self.fields['bank'].initial = '3'  # Valor padrão no campo 'value'
        self.fields['status'].initial = '1'   # Data padrão para 'due_at'
        
        # Filtra categorias com tipo=1
        self.fields['category'].queryset = models.Category.objects.filter(type_category=2)
        self.fields['status'].queryset = models.StatusMovement.objects.filter(type=2)

        # Certifique-se de formatar as datas corretamente ao carregar o formulário
        if self.instance.pk:  # Verifique se a instância já existe (edição)
            if self.instance.due_at:
                self.initial['due_at'] = self.instance.due_at.strftime('%Y-%m-%d')  # Formato esperado
            if self.instance.payment_at:
                self.initial['payment_at'] = self.instance.payment_at.strftime('%Y-%m-%d')  # Formato esperado
             # Formatação do valor monetário ao carregar o formulário (edição)
            if self.instance.value_payment:
                formatted_value = "R$ {:,.2f}".format(self.instance.value_payment).replace(",", "X").replace(".", ",").replace("X", ".")
                self.initial['value_payment'] = formatted_value  # Exibe o valor no formato correto
            if self.instance.value:
                formatted_value = "R$ {:,.2f}".format(self.instance.value).replace(",", "X").replace(".", ",").replace("X", ".")
                self.initial['value'] = formatted_value  # Exibe o valor no formato correto