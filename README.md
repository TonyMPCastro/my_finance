# MyFinance

Este repositório contém o projeto de um **Sistema de Finaças Pessoais**, desenvolvido como parte de um trabalho em grupo. O projeto foi implementado em **python** por meio do framework **Django**, e abrange todas as etapas do processo de construção de layout, prototipagem, desenvolvimento do font-end, desenvolvimento do back-end, banco de dados e testes de funcionalidades.

## 📚 Sobre o Projeto

MyFinance é um sistema de controle de finanças pessoais desenvolvido para ajudar usuários a gerenciar suas receitas e despesas de forma simples e eficiente.

Com uma interface intuitiva, o sistema permite que os usuários realizem cadastro e login seguro, registrem suas dívidas e recebimentos, e acompanhem suas finanças por meio de relatórios básicos.

O objetivo do MyFinance é proporcionar uma ferramenta prática para organização financeira, ajudando os usuários a manterem o equilíbrio entre gastos e ganhos.

O projeto foi desenvolvido em equipe para aplicar conceitos fundamentais de desenvolvimento web, incluindo:
- Arquitetura MVC para organização do código e separação de responsabilidades;
- Autenticação e segurança com hash de senhas e proteção contra acessos não autorizados;
- Banco de dados relacional para armazenamento das informações financeiras;
- Front-end responsivo para garantir uma boa experiência em diferentes dispositivos;
- Consumo de APIs para funcionalidades adicionais, como conversão de moedas ou gráficos interativos.

## 🚀 Como Executar

### Pré-requisitos
- Python 3.x (Download aqui)
- pip (gerenciador de pacotes do Python, já incluído no Python 3)
- Virtualenv (opcional, mas recomendado para isolamento do ambiente)
- Banco de dados (SQLite incluso no Django, mas pode ser PostgreSQL, MySQL, etc.)

### Passos
1. Clone este repositório:
   ```bash
   git clone https://github.com/TonyMPCastro/my_finance.git

2. Crie o VENV:
   ```bash
    python -m venv venv

    python3 -m venv venv  # Macbook

    python3 manage.py runserver #Executar

3. Rode o VENV:
   ```bash
    venv2/Scripts/activate

    source venv2/bin/activate # Macbook

    deactivate # Macbook

4. Inatall dependencia:
   ```bash
    pip install -r requirements.txt

    pip3 install -r requirements.txt # Macbook

5. CRETATE Migrations
   ```bash
   python .\manage.py makemigrations

6. Atualiza o DB 
   ```bash
   python .\manage.py migrate

7. CRETATE Super User
   ```bash
    python manage.py createsuperuser

## ✒️ Autores

* **ANTONIO MP CASTRO** - *ANTONIO MARCOS PATRICIO CASTRO* - [TonyMPCastro](https://github.com/TonyMPCastro)
* **NILTON MANGUEIRA** - *NILTON MACIEL MANGUEIRA* - [mangueiraDev](https://github.com/mangueiraDev)
