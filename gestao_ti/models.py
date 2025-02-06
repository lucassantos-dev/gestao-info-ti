from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver


class Filial(models.Model):
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=200)
    cnpj = models.CharField(max_length=200,  null=True, blank=True)
    ativo = models.BooleanField(default=True) 
    def __str__(self):
        return self.nome

class Colaborador(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20, null=True, blank=True)
    email_pessoal = models.EmailField(unique=True, null=True, blank=True)  # Evita conflito com o modelo Email
    filial = models.ForeignKey(Filial, on_delete=models.CASCADE, related_name="colaboradores")
    data_admissao = models.DateField()
    data_demissao = models.DateField(null=True, blank=True)
    ativo = models.BooleanField(default=True) 
    def __str__(self):
        return self.nome

class Sistema(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    data_aquisicao = models.DateField( null=True, blank=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    vencimento = models.DateField(null=True, blank=True)
    tipo_vencimento = models.CharField(max_length=50, 
                                       choices=[('anual', 'Anual'), ('mensal', 
                                                                     'Mensal'), ('pontual', 'Pontual')],
                                       null=True, blank=True)
    login_mestre = models.CharField(max_length=100)  # Login master do sistema
    senha = models.CharField(max_length=100)  # Senha do login mestre
    ativo = models.BooleanField(default=True) 
    filial = models.ForeignKey(Filial, on_delete=models.SET_NULL, null=True, blank=True, related_name="sistemas")  

class Email(models.Model):
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=100)
    colaborador = models.ForeignKey(Colaborador, on_delete=models.SET_NULL, null=True, blank=True, related_name="emails")
    data_criacao = models.DateField(auto_now_add=True)
    ativo = models.BooleanField(default=True)
    data_exclusao = models.DateField(null=True, blank=True)
    ativo = models.BooleanField(default=True) 
    def __str__(self):
        return self.email

class HistoricoEmail(models.Model):
    email = models.ForeignKey(Email, on_delete=models.CASCADE, related_name="historicos")
    colaborador = models.ForeignKey(Colaborador, on_delete=models.CASCADE)
    data_inicio = models.DateField(auto_now_add=True)
    data_fim = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.colaborador.nome} - {self.email.email} ({self.data_inicio} a {self.data_fim or 'Atual'})"
