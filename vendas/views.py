from django.shortcuts import render, redirect, get_object_or_404
from .models import Venda
from django.db.models import Sum


# 🔧 Função para tratar valores monetários corretamente
def converter_valor(valor_str):
    if not valor_str:
        return 0

    # remove espaços
    valor_str = valor_str.strip()

    # remove separador de milhar e ajusta decimal
    valor_str = valor_str.replace('.', '').replace(',', '.')

    try:
        return float(valor_str)
    except ValueError:
        return 0


def dashboard(request):

    if request.method == "POST":
        vendedor = request.POST.get("vendedor")
        valor_str = request.POST.get("valor")

        valor = converter_valor(valor_str)

        Venda.objects.create(vendedor=vendedor, valor=valor)
        return redirect("dashboard")

    vendas = Venda.objects.all()

    total = vendas.aggregate(Sum("valor"))["valor__sum"] or 0

    vendedores = {}

    for venda in vendas:
        vendedores[venda.vendedor] = vendedores.get(venda.vendedor, 0) + venda.valor

    labels = list(vendedores.keys())

    # 🔥 CONVERSÃO PARA PORCENTAGEM
    valores_brutos = [float(v) for v in vendedores.values()]
    soma_total = sum(valores_brutos)

    if soma_total > 0:
        valores = [(v / soma_total) * 100 for v in valores_brutos]
    else:
        valores = [0 for v in valores_brutos]

    context = {
        "labels": labels,
        "valores": valores,
        "total": total,
        "vendas": vendas
    }

    return render(request, "dashboard.html", context)


def deletar_venda(request, id):
    venda = get_object_or_404(Venda, id=id)
    venda.delete()
    return redirect("dashboard")


def editar_venda(request, id):
    venda = get_object_or_404(Venda, id=id)

    if request.method == "POST":
        venda.vendedor = request.POST.get("vendedor")

        valor_str = request.POST.get("valor")
        venda.valor = converter_valor(valor_str)

        venda.save()
        return redirect("dashboard")

    return render(request, "editar.html", {"venda": venda})