from django.contrib import admin
from import_export.admin import ExportMixin
from import_export import resources
from .models import (
    Filial, Colaborador, Sistema, Credencial, Email, HistoricoEmail, Maquina, Equipamento, Inventario
)
from import_export.formats.base_formats import XLSX
from django import forms

# Customização do Admin
admin.site.site_header = "Gestão de TI"
admin.site.site_title = "Administração - Gestão de TI"
admin.site.index_title = "Painel de Controle"

class SenhaInputForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = '__all__'
        widgets = {
            'senha': forms.PasswordInput(render_value=True)
        }

# Mixin para bloquear exclusão por usuários normais
class SomenteSuperuserDeleteMixin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.is_superuser:
            if 'delete_selected' in actions:
                del actions['delete_selected']
        return actions

# Recursos para exportação
class FilialResource(resources.ModelResource):
    class Meta:
        model = Filial

class ColaboradorResource(resources.ModelResource):
    class Meta:
        model = Colaborador

class SistemaResource(resources.ModelResource):
    class Meta:
        model = Sistema

class CredencialResource(resources.ModelResource):
    class Meta:
        model = Credencial

class EmailResource(resources.ModelResource):
    class Meta:
        model = Email

class HistoricoEmailResource(resources.ModelResource):
    class Meta:
        model = HistoricoEmail

class MaquinaResource(resources.ModelResource):
    class Meta:
        model = Maquina

class EquipamentoResource(resources.ModelResource):
    class Meta:
        model = Equipamento

class InventarioResource(resources.ModelResource):
    class Meta:
        model = Inventario

@admin.register(Filial)
class FilialAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = FilialResource
    list_display = ('nome', 'endereco', 'cnpj', 'ativo')
    search_fields = ('nome', 'cnpj')

@admin.register(Colaborador)
class ColaboradorAdmin(ExportMixin, SomenteSuperuserDeleteMixin, admin.ModelAdmin):
    resource_class = ColaboradorResource
    list_display = ('nome', 'email_pessoal', 'filial', 'ativo')
    list_filter = ('ativo', 'filial')

@admin.register(Sistema)
class SistemaAdmin(ExportMixin, SomenteSuperuserDeleteMixin, admin.ModelAdmin):
    resource_class = SistemaResource
    list_display = ('nome', 'tipo_vencimento', 'ativo', 'filial')
    list_filter = ('ativo', 'tipo_vencimento', 'filial')
    search_fields = ('nome',)

@admin.register(Credencial)
class CredencialAdmin(ExportMixin, SomenteSuperuserDeleteMixin, admin.ModelAdmin):
    resource_class = CredencialResource
    list_display = ('nome', 'sistema', 'login', 'ativo')
    list_filter = ('ativo', 'sistema')
    search_fields = ('nome', 'login')

@admin.register(Email)
class EmailAdmin(ExportMixin, SomenteSuperuserDeleteMixin, admin.ModelAdmin):
    resource_class = EmailResource
    list_display = ('email', 'colaborador', 'ativo')
    list_filter = ('ativo',)
    search_fields = ('email',)

@admin.register(HistoricoEmail)
class HistoricoEmailAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = HistoricoEmailResource
    list_display = ('email', 'colaborador', 'data_inicio', 'data_fim')
    list_filter = ('email', 'colaborador')
    search_fields = ('email__email', 'colaborador__nome')

@admin.register(Maquina)
class MaquinaAdmin(ExportMixin, SomenteSuperuserDeleteMixin, admin.ModelAdmin):
    resource_class = MaquinaResource
    list_display = ('nome', 'processador', 'memoria')  
    list_filter = ('processador', 'memoria')
    search_fields = ('nome', 'endereco_mac', 'ip')

@admin.register(Equipamento)
class EquipamentoAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = EquipamentoResource
    list_display = ('tipo', 'descricao')  
    search_fields = ('tipo', 'descricao')

@admin.register(Inventario)
class InventarioAdmin(ExportMixin, SomenteSuperuserDeleteMixin, admin.ModelAdmin):
    resource_class = InventarioResource
    list_display = ('nome', 'numero_serie', 'filial', 'colaborador', 'tipo_item', 'ativo', 'setor', 'funcionando')
    list_filter = ('ativo', 'filial', 'funcionando', 'setor')
    search_fields = ('nome', 'numero_serie')

    def tipo_item(self, obj):
        if obj.maquina:
            return "Máquina"
        elif obj.equipamento:
            return "Equipamento"
        return "Não definido"
    tipo_item.short_description = "Tipo do Item"
