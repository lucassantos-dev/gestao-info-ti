# Gestão de Informações de TI

Este é um projeto desenvolvido em Django para gerenciar informações relacionadas ao departamento de Tecnologia da Informação (TI), incluindo colaboradores, e-mails e sistemas. O projeto utiliza o [Jazzmin](https://github.com/farridav/django-jazzmin) para customização da interface administrativa, proporcionando uma experiência mais intuitiva e agradável.

## 🚀 Funcionalidades

- **Gerenciamento de Colaboradores**: Cadastro, edição e exclusão de informações dos colaboradores da TI.
- **Gerenciamento de E-mails**: Controle e organização dos e-mails corporativos.
- **Gerenciamento de Sistemas**: Registro e acompanhamento dos sistemas utilizados pela equipe de TI.

## 🛠 Tecnologias Utilizadas

- **Django**: Framework web em Python para desenvolvimento do backend.
- **Jazzmin**: Tema para customização do Django Admin, melhorando a interface e usabilidade.

## 📌 Instalação

1. **Clone o repositório**:

   ```bash
   git clone https://github.com/lucassantos-dev/gestao-info-ti.git
   cd gestao-info-ti
   ```

2. **Crie um ambiente virtual**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # No Windows, use: venv\Scripts\activate
   ```

3. **Instale as dependências**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Realize as migrações do banco de dados**:

   ```bash
   python manage.py migrate
   ```

5. **Crie um superusuário para acessar o Django Admin**:

   ```bash
   python manage.py createsuperuser
   ```

6. **Inicie o servidor de desenvolvimento**:

   ```bash
   python manage.py runserver
   ```

   A aplicação estará disponível em `http://127.0.0.1:8000/`.

## 🎨 Configuração do Jazzmin

O Jazzmin já está configurado no projeto para aprimorar a interface administrativa do Django. Para personalizações adicionais, consulte a [documentação oficial do Jazzmin](https://django-jazzmin.readthedocs.io/).

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests para sugerir melhorias ou corrigir bugs.

## 📜 Licença

Este projeto está licenciado sob a licença MIT. Consulte o arquivo `LICENSE` para mais informações.
