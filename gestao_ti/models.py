from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.forms import ValidationError

class Filial(models.Model):
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=200)
    cnpj = models.CharField(max_length=200, null=True, blank=True)
    ativo = models.BooleanField(default=True) 
    
    def __str__(self):
        return self.nome

class Colaborador(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20, null=True, blank=True)
    email_pessoal = models.EmailField(unique=True, null=True, blank=True)
    filial = models.ForeignKey(Filial, on_delete=models.CASCADE, related_name="colaboradores")
    data_admissao = models.DateField()
    data_demissao = models.DateField(null=True, blank=True)
    ativo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nome

class Sistema(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    data_aquisicao = models.DateField(null=True, blank=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    vencimento = models.DateField(null=True, blank=True)
    tipo_vencimento = models.CharField(
        max_length=50, 
        choices=[('anual', 'Anual'), ('mensal', 'Mensal'), ('pontual', 'Pontual')],
        null=True, blank=True
    )
    ativo = models.BooleanField(default=True)
    filial = models.ForeignKey(Filial, on_delete=models.SET_NULL, null=True, blank=True, related_name="sistemas")
    
    def __str__(self):
        return self.nome

class Credencial(models.Model):
    nome = models.CharField(max_length=100)
    sistema = models.ForeignKey(Sistema, on_delete=models.SET_NULL, null=True, blank=True, related_name="credenciais")
    login = models.CharField(max_length=100)
    senha = models.CharField(max_length=100)
    ativo = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.nome} ({self.sistema.nome if self.sistema else 'Sem sistema'})"

class Email(models.Model):
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=100)
    colaborador = models.ForeignKey(Colaborador, on_delete=models.SET_NULL, null=True, blank=True, related_name="emails")
    data_criacao = models.DateField(auto_now_add=True)
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
    

class Maquina(models.Model):
    nome = models.CharField(max_length=100,blank=True, null=True)
    processador = models.CharField(max_length=100, blank=True, null=True)
    memoria = models.CharField(max_length=100, blank=True, null=True)
    disco_rigido = models.CharField(max_length=100, blank=True, null=True)
    sistema_operacional = models.CharField(max_length=100, blank=True, null=True)
    endereco_mac = models.CharField(max_length=100, blank=True, null=True)
    endereco_mac_wifi = models.CharField(max_length=100, blank=True, null=True)
    ip = models.CharField(max_length=100, blank=True, null=True)
    usuario = models.CharField(max_length=100, blank=True, null=True)
    senha = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Máquina - {self.nome} ({self.processador}, {self.memoria})"


class Equipamento(models.Model):
    tipo = models.CharField(max_length=100, blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"Equipamento -  ({self.tipo} - {self.descricao})"
    
class Inventario(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    numero_serie = models.CharField(max_length=100, unique=True)
    filial = models.ForeignKey(Filial, on_delete=models.CASCADE, related_name="inventarios")
    colaborador = models.ForeignKey(Colaborador, on_delete=models.SET_NULL, null=True, blank=True, related_name="inventarios")
    data_aquisicao = models.DateField(null=True, blank=True)
    ativo = models.BooleanField(default=True)
    setor = models.CharField(max_length=100, blank=True, null=True)
    funcionando = models.BooleanField(default=True)
    defeito = models.TextField(blank=True, null=True)
    
    # Relacionamentos com Máquina e Equipamento
    maquina = models.OneToOneField(Maquina, on_delete=models.SET_NULL, null=True, blank=True, related_name="inventario")
    equipamento = models.OneToOneField(Equipamento, on_delete=models.SET_NULL, null=True, blank=True, related_name="inventario")

    def __str__(self):
        return f"{self.nome} - {self.numero_serie}"

    # Garantir que pelo menos um dos campos maquina ou equipamento seja preenchido
    def clean(self):
        if not self.maquina and not self.equipamento:
            raise ValidationError('Deve ser atribuído uma máquina ou um equipamento ao inventário.')



