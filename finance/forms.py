from django import forms
from django.contrib.auth.models import User
import pprint  # Módulo para imprimir dicionários de forma organizada
from django.core.validators import EmailValidator



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
