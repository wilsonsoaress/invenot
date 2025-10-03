# inventory/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .forms import DeviceForm, ClientForm, MovimentacaoForm, InspectionForm
from .models import Device, Client, Movimentacao, Inspection

# --- Views para Dispositivos (Devices) ---

def device_list(request):
    devices = Device.objects.all().order_by('id')
    context = {
        'devices': devices
    }
    return render(request, 'inventory/device_list.html', context)

def register_device(request):
    if request.method == 'POST':
        form = DeviceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_page')
    else:
        form = DeviceForm()
    return render(request, 'inventory/register_device.html', {'form': form})

def device_update(request, pk):
    device = get_object_or_404(Device, pk=pk)
    if request.method == 'POST':
        form = DeviceForm(request.POST, instance=device)
        if form.is_valid():
            form.save()
            return redirect('device_list')
    else:
        form = DeviceForm(instance=device)
    context = {
        'form': form
    }
    return render(request, 'inventory/register_device.html', context)

def device_delete(request, pk):
    device = get_object_or_404(Device, pk=pk)
    if request.method == 'POST':
        device.delete()
        return redirect('device_list')
    context = {
        'device': device
    }
    return render(request, 'inventory/device_confirm_delete.html', context)


# --- Views para Clientes (Clients) ---

def register_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('client_success_page')
    else:
        form = ClientForm()
    return render(request, 'inventory/register_client.html', {'form': form})

def client_success_view(request):
    return render(request, 'inventory/client_success.html')


# --- Views para Movimentações (Movements) ---

def device_history(request, pk):
    # 1. Busca o dispositivo específico pelo seu ID (pk)
    device = get_object_or_404(Device, pk=pk)
    
    # 2. Busca TODAS as movimentações relacionadas a este dispositivo.
    #    O Django faz isso de forma inteligente com `device.movimentacao_set.all()`
    movements = device.movimentacao_set.all().order_by('-movement_date')
    
    context = {
        'device': device,
        'movements': movements
    }
    
    return render(request, 'inventory/device_history.html', context)

def movement_list(request):
    movimentacoes = Movimentacao.objects.all().order_by('-movement_date')
    context = {
        'movimentacoes': movimentacoes
    }
    return render(request, 'inventory/movement_list.html', context)

def register_movement(request):
    if request.method == 'POST':
        form = MovimentacaoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('movement_list')
    else:
        form = MovimentacaoForm()
    return render(request, 'inventory/register_movement.html', {'form': form})

def movement_update(request, pk):
    movimentacao = get_object_or_404(Movimentacao, pk=pk)
    if request.method == 'POST':
        form = MovimentacaoForm(request.POST, instance=movimentacao)
        if form.is_valid():
            form.save()
            return redirect('movement_list')
    else:
        form = MovimentacaoForm(instance=movimentacao)
    context = {
        'form': form
    }
    return render(request, 'inventory/register_movement.html', context)

def movement_delete(request, pk):
    movimentacao = get_object_or_404(Movimentacao, pk=pk)
    if request.method == 'POST':
        movimentacao.delete()
        return redirect('movement_list')
    context = {
        'movimentacao': movimentacao
    }
    return render(request, 'inventory/movement_confirm_delete.html', context)


# --- Views Genéricas ---

def success_view(request):
    return render(request, 'inventory/success.html')

def create_inspection(request, pk):
    device = get_object_or_404(Device, pk=pk)
    if request.method == 'POST':
        form = InspectionForm(request.POST)
        if form.is_valid():
            inspection = form.save(commit=False)
            inspection.device = device
            inspection.save()
            return redirect('device_history', pk=device.pk) # Volta para o histórico do dispositivo
    else:
        form = InspectionForm()

    context = {
        'form': form,
        'device': device
    }
    return render(request, 'inventory/create_inspection.html', context)