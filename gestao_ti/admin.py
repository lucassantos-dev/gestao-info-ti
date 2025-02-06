from django.contrib import admin
from import_export.admin import ExportMixin
from import_export import resources
from .models import Colaborador, Sistema, Email, Filial, HistoricoEmail
from import_export.formats.base_formats import XLSX
from django import forms
# Customização do Admin
admin.site.site_header = "Gestão de TI"
admin.site.site_title = "Administração - Gestão de TI"
admin.site.index_title = "Painel de Controle"

class SenhaInputForm(forms.ModelForm):
    class Meta:
        model: Email
        fields = '__all__'
        widgets = {
            'senha': forms.PasswordInput(render_value=True)
        }

class CustomAdminSite(admin.AdminSite):
    site_header = "Gestão de TI"
    site_title = "Administração - Gestão de TI"
    index_title = "Painel de Controle"

    def get_urls(self):
        from django.conf.urls.static import static
        from django.conf import settings
        urls = super().get_urls()
        return urls + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
admin.site = CustomAdminSite()

# Mixin para bloquear exclusão por usuários normais
class SomenteSuperuserDeleteMixin(admin.ModelAdmin):
    """Mixin para impedir exclusão de registros por usuários normais."""
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser  # Apenas superusuário pode excluir

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.is_superuser:
            if 'delete_selected' in actions:
                del actions['delete_selected']  # Remove ação de exclusão em massa
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

class EmailResource(resources.ModelResource):
    class Meta:
        model = Email

class HistoricoEmailResource(resources.ModelResource):
    class Meta:
        model = HistoricoEmail

# Admin personalizado com exportação
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
    actions = ['desativar_colaboradores']

    @admin.action(description="Desativar colaboradores selecionados")
    def desativar_colaboradores(self, request, queryset):
        queryset.update(ativo=False)

@admin.register(Sistema)
class SistemaAdmin(ExportMixin, SomenteSuperuserDeleteMixin, admin.ModelAdmin):
    resource_class = SistemaResource
    list_display = ('nome', 'tipo_vencimento', 'ativo', 'filial')
    list_filter = ('ativo', 'tipo_vencimento', 'filial')
    search_fields = ('nome',)
    actions = ['desativar_sistemas']

    @admin.action(description="Desativar sistemas selecionados")
    def desativar_sistemas(self, request, queryset):
        queryset.update(ativo=False)

# Inline para histórico de e-mails
class HistoricoEmailInline(admin.TabularInline):  
    model = HistoricoEmail  
    extra = 0  # Não exibir linhas vazias  

@admin.register(Email)
class EmailAdmin(ExportMixin, SomenteSuperuserDeleteMixin, admin.ModelAdmin):
    resource_class = EmailResource
    list_display = ('email', 'colaborador', 'ativo')
    list_filter = ('ativo',)
    actions = ['desativar_emails']
    inlines = [HistoricoEmailInline] 

    @admin.action(description="Desativar e-mails selecionados")
    def desativar_emails(self, request, queryset):
        queryset.update(ativo=False)
    def get_export_formats(self):
            """Garante que XLSX seja incluído na lista de formatos de exportação"""
            formats = super().get_export_formats()
            if XLSX not in formats:  # Evita adicionar duplicado
                formats.append(XLSX)
            return formats
    
@admin.register(HistoricoEmail)
class HistoricoEmailAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = HistoricoEmailResource
    list_display = ('email', 'colaborador', 'data_inicio', 'data_fim')
    list_filter = ('email', 'colaborador')
    search_fields = ('email__email', 'colaborador__nome')
    
admin.site.register(Filial)
admin.site.register(Colaborador, ColaboradorAdmin)
admin.site.register(Sistema, SistemaAdmin)
admin.site.register(Email, EmailAdmin)
admin.site.register(HistoricoEmail, HistoricoEmailAdmin)