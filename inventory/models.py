# inventory/models.py

from django.db import models
from simple_history.models import HistoricalRecords

class Device(models.Model):
    # Opções para o tipo de dispositivo
    DEVICE_TYPE_CHOICES = [
        ('desktop', 'Desktop'),
        ('notebook', 'Notebook'),
    ]

    device_type = models.CharField(
        max_length=10,
        choices=DEVICE_TYPE_CHOICES,
        default='desktop',
        verbose_name="Tipo de Dispositivo"
    )
    brand = models.CharField(max_length=100, verbose_name="Marca")
    model = models.CharField(max_length=100, verbose_name="Modelo")
    service_tag = models.CharField(max_length=100, unique=True, verbose_name="Service Tag")
    processor = models.CharField(max_length=100, verbose_name="Processador")
    ram = models.CharField(max_length=50, verbose_name="Memória RAM")
    ssd = models.CharField(max_length=50, verbose_name="SSD/Armazenamento")
    is_new = models.BooleanField(default=False, verbose_name="Marcar como novo")
    observation = models.TextField(blank=True, null=True, verbose_name="Observação")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Cadastro")
    history = HistoricalRecords()


    def __str__(self):
        return f"{self.get_device_type_display()} {self.brand} {self.model} - {self.service_tag}"

    class Meta:
        verbose_name = "Dispositivo"
        verbose_name_plural = "Dispositivos"

class Client(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nome / Razão Social")
    document = models.CharField(max_length=50, unique=True, verbose_name="CPF/CNPJ")
    address = models.CharField(max_length=300, blank=True, null=True, verbose_name="Endereço")
    email = models.EmailField(unique=True, verbose_name="E-mail")
    contact_name = models.CharField(max_length=200, blank=True, null=True, verbose_name="Contato")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefone")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Cadastro")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

class Movimentacao(models.Model):
    MOVEMENT_TYPE_CHOICES = [
        ('locacao', 'Nova Locação'),
        ('aditivo', 'Aditivo'),
        ('devolucao', 'Devolução'),
        ('manutencao', 'Manutenção'),
        ('venda', 'Venda'),
        ('outros', 'Outros'),
    ]
    device = models.ForeignKey(Device, on_delete=models.CASCADE, verbose_name="Dispositivo")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Cliente")
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPE_CHOICES, verbose_name="Tipo de Movimentação")
    movement_date = models.DateField(verbose_name="Data da Movimentação")
    details = models.TextField(blank=True, null=True, verbose_name="Detalhes/Observação")
    issue_description = models.TextField(verbose_name="Descrição do Problema")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Movimentação")

    def __str__(self):
        return f"Movimentação do {self.device} para {self.client} em {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        verbose_name = "Movimentação"
        verbose_name_plural = "Movimentações"

class Inspection(models.Model):
    # Relacionamento com o Dispositivo
    device = models.ForeignKey(Device, on_delete=models.CASCADE, verbose_name="Dispositivo")
    inspection_date = models.DateTimeField(auto_now_add=True, verbose_name="Data da Inspeção")

    # Campos do Checklist
    PHYSICAL_STATE_CHOICES = [
        ('com_marcas', 'Seminovo com marcas de uso'),
        ('bom', 'Bom estado - sem marcas'),
        ('riscos', 'Riscos profundos'),
        ('outros', 'Outros'),
    ]
    physical_state = models.CharField(max_length=10, choices=PHYSICAL_STATE_CHOICES, verbose_name="Estado Físico")
    physical_state_other = models.CharField(max_length=255, blank=True, null=True, verbose_name="Outro Estado Físico")

    has_charger = models.BooleanField(verbose_name="Possui Carregador?")
    CHARGER_CONDITION_CHOICES = [
        ('usado', 'Usado'),
        ('novo', 'Novo'),
    ]
    charger_condition = models.CharField(max_length=10, choices=CHARGER_CONDITION_CHOICES, blank=True, null=True, verbose_name="Condição do Carregador")

    CONFIG_CHOICES = [
        ('conforme', 'Conforme'),
        ('modificado', 'Modificado'),
    ]
    configuration = models.CharField(max_length=10, choices=CONFIG_CHOICES, verbose_name="Configurações")
    configuration_mods = models.CharField(max_length=255, blank=True, null=True, verbose_name="Modificações")
    
    os_installed = models.BooleanField(verbose_name="Sistema Operacional Instalado?")
    has_office = models.BooleanField(verbose_name="Possui Office?")
    office_version = models.CharField(max_length=100, blank=True, null=True, verbose_name="Versão do Office")
    office_key = models.CharField(max_length=100, blank=True, null=True, verbose_name="Chave do Office")

    notes = models.TextField(blank=True, null=True, verbose_name="Notas Adicionais")

    def __str__(self):
        return f"Inspeção de {self.device} em {self.inspection_date.strftime('%d/%m/%Y %H:%M')}"

    class Meta:
        verbose_name = "Checklist"
        verbose_name_plural = "Checklists"
        ordering = ['-inspection_date']