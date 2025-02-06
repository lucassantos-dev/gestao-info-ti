from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Email, HistoricoEmail

@receiver(post_save, sender=Email)
def criar_historico_email(sender, instance, created, **kwargs):
    """Cria um histórico automaticamente ao adicionar um colaborador a um e-mail."""
    if instance.colaborador:
        # Fecha o histórico anterior, se houver, antes de criar um novo
        HistoricoEmail.objects.filter(email=instance, data_fim__isnull=True).update(data_fim=instance.data_criacao)
        
        # Cria um novo histórico
        HistoricoEmail.objects.create(
            email=instance,
            colaborador=instance.colaborador,
            data_inicio=instance.data_criacao
        )

@receiver(pre_delete, sender=Email)
def finalizar_historico_email(sender, instance, **kwargs):
    """Fecha o histórico quando o e-mail é excluído."""
    HistoricoEmail.objects.filter(email=instance, data_fim__isnull=True).update(data_fim=instance.data_exclusao)
