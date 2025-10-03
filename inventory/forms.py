# inventory/forms.py

from django import forms
from .models import Device, Client, Movimentacao, Inspection

class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = [
            'device_type',
            'brand',
            'model',
            'service_tag',
            'processor',
            'ram',
            'ssd',
            'is_new',
            'observation'
        ]

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            'name',
            'document',
            'address',
            'email',
            'contact_name',
            'phone'
        ]

class MovimentacaoForm(forms.ModelForm):
    class Meta:
        model = Movimentacao
        fields = ['device', 'client', 'movement_type', 'movement_date', 'details']
        widgets = {
            'movement_date': forms.DateInput(attrs={'type': 'date'}),
        }

class InspectionForm(forms.ModelForm):
    class Meta:
        model = Inspection
        # Todos os campos exceto os que são preenchidos automaticamente
        exclude = ['device', 'inspection_date']