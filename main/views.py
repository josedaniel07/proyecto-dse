from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, FormView, TemplateView, View, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.db.models import F
from django.contrib import messages
from .models import *
from .forms import *
from random import randint
from datetime import date


class HomePageView(TemplateView):
  template_name = "main/home.html"
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['latest_products'] = Producto.objects.all()[:4]
    context['productos'] = Producto.objects.all()
    return context

class ProductListView(ListView):
  model = Producto
  template_name = 'main/producto_list.html'
  object_list = Producto.objects.all()
  def get_queryset(self):
    query = self.request.GET.get('q')
    query2 = self.request.GET.get('categoria')
    query3 = self.request.GET.get('filtro')
    if query is None and query2 is None and query3 is None:
      return Producto.objects.all().order_by('nombre')
    if query2 == "abc":
      object_list=Producto.objects.all().order_by('nombre')
      if query is not None:
        object_list=object_list.filter(nombre__icontains=query).order_by('nombre')
        if query3 == "1":
          object_list = object_list.filter(nombre__icontains=query).order_by('precio','nombre')
          return object_list
        elif query3 == "2":
          object_list = object_list.filter(nombre__icontains=query).order_by('-precio','nombre')
          return object_list
      else:
        if query3 == "1":
          object_list = Producto.objects.all().order_by('precio','nombre')
          return object_list
        elif query3 == "2":
          object_list = Producto.objects.all().order_by('-precio','nombre')
          return object_list
    else:
      object_list=Producto.objects.filter(categoria__pk=query2).order_by('nombre')
      if query is not None:
        object_list=object_list.filter(nombre__icontains=query).order_by('nombre')
        if query3 == "1":
          object_list = object_list.order_by('precio','nombre')
          return object_list
        elif query3 == "2":
          object_list = object_list.order_by('-precio', 'nombre')
          return object_list
      else:
        if query3 == "1":
          object_list = object_list.order_by('precio','nombre')
          return object_list
        elif query3 == "2":
          object_list = object_list.order_by('-precio', 'nombre')
          return object_list

class ProductDetailView(DetailView):
  model = Producto
class ProveedorListView(ListView):
  model = Proveedor
class ProveedorDetailView(DetailView):
  model = Proveedor
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['productos'] = context['object'].producto_set.all()
    return context


class CategoriaListView(ListView):
  model = Categoria
class CategoriaDetailView(DetailView):
  model = Categoria
class LocalizacionListView(ListView):
  model = Localizacion
class LocalizacionDetailView(DetailView):
  model = Localizacion

class PreRegister(TemplateView):
  template_name = 'registration/register.html'

class RegistrationViewCliente(FormView):
  template_name = 'registration/cliente.html'
  form_class = ClienteUserForm
  success_url = reverse_lazy('home')
  def form_valid(self, form):
    # This methos is called when valid from data has been POSTed
    # It should return an HttpResponse
    # Create User
    username = form.cleaned_data['username']
    first_name = form.cleaned_data['first_name']
    last_name = form.cleaned_data['last_name']
    email = form.cleaned_data['email']
    password = form.cleaned_data['password1']
    user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
    user.save()
    # Create Profile
    documento_identidad = form.cleaned_data['documento_identidad']
    fecha_nacimiento = form.cleaned_data['fecha_nacimiento']
    genero = form.cleaned_data['genero']
    numero = form.cleaned_data['numero']
    user_profile = Profile.objects.create(user=user, documento_identidad=documento_identidad, fecha_nacimiento=fecha_nacimiento, estado="", genero=genero,numero=numero)
    user_profile.save()
    # Create Cliente if needed
    ruc = form.cleaned_data['RUC']
    preferencias = form.cleaned_data['preferencias']
    cliente = Cliente.objects.create(user_profile=user_profile, RUC=ruc, preferencias=preferencias)
    # Login the user
    login(self.request, user)
    return super().form_valid(form)

class RegistrationViewColaborador(FormView):
  template_name = 'registration/colaborador.html'
  form_class = ColaboradorUserForm
  success_url = reverse_lazy('home')
  def form_valid(self, form):
    # This methos is called when valid from data has been POSTed
    # It should return an HttpResponse
    # Create User
    username = form.cleaned_data['username']
    first_name = form.cleaned_data['first_name']
    last_name = form.cleaned_data['last_name']
    email = form.cleaned_data['email']
    password = form.cleaned_data['password1']
    user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
    user.save()
    # Create Profile
    documento_identidad = form.cleaned_data['documento_identidad']
    fecha_nacimiento = form.cleaned_data['fecha_nacimiento']
    estado = form.cleaned_data['estado']
    genero = form.cleaned_data['genero']
    numero = form.cleaned_data['numero']
    user_profile = Profile.objects.create(user=user, documento_identidad=documento_identidad, fecha_nacimiento=fecha_nacimiento, estado=estado, genero=genero, numero=numero)
    user_profile.save()
    # Create Colaborador if needed
    reputacion = form.cleaned_data['reputacion']
    colaborador = Colaborador.objects.create(user_profile=user_profile, reputacion=reputacion)
    # Handle special attribute
    cobertura_entrega = form.cleaned_data['cobertura_entrega']
    cobertura_entrega_set = Localizacion.objects.filter(pk=cobertura_entrega.pk)
    colaborador.cobertura_entrega.set(cobertura_entrega_set)
    colaborador.save()
    # Login the user
    login(self.request, user)
    return super().form_valid(form)


class AddToCartView(View):
  def get(self, request, product_pk):
    # Obten el cliente
    user_profile = Profile.objects.get(user=request.user)
    cliente = Cliente.objects.get(user_profile=user_profile)
    # Obtén el producto que queremos añadir al carrito
    producto = Producto.objects.get(pk=product_pk)
    # Obtén/Crea un/el pedido en proceso (EP) del usuario
    pedido, _ = Pedido.objects.get_or_create(cliente=cliente, estado='En Proceso', tarifa=0)
    pedido.fecha_creacion = datetime.datetime.now()
    # Obtén/Crea un/el detalle de pedido
    detalle_pedido, created = DetallePedido.objects.get_or_create(
      producto=producto,
      pedido=pedido,
    )

    # Si el detalle de pedido es creado la cantidad es 1
    # Si no sumamos 1 a la cantidad actual
    if created:
      detalle_pedido.cantidad = 1
    else:
      detalle_pedido.cantidad = F('cantidad') + 1
    # Guardamos los cambios
    detalle_pedido.save()
    # Recarga la página
    return redirect(request.META['HTTP_REFERER'])


class RemoveFromCartView(View):
  def get(self, request, product_pk):
    # Obten el cliente
    user_profile = Profile.objects.get(user=request.user)
    cliente = Cliente.objects.get(user_profile=user_profile)
    # Obtén el producto que queremos añadir al carrito
    producto = Producto.objects.get(pk=product_pk)
    # Obtén/Crea un/el pedido en proceso (EP) del usuario
    pedido, _ = Pedido.objects.get_or_create(cliente=cliente, estado='En Proceso')
    # Obtén/Crea un/el detalle de pedido
    detalle_pedido = DetallePedido.objects.get(
      producto=producto,
      pedido=pedido,
    )
    # Si la cantidad actual menos 1 es 0 elmina el producto del carrito
    # Si no restamos 1 a la cantidad actual
    if detalle_pedido.cantidad - 1 == 0:
      detalle_pedido.delete()
    else:
      detalle_pedido.cantidad = F('cantidad') - 1
      # Guardamos los cambios
      detalle_pedido.save()
    # Recarga la página
    return redirect(request.META['HTTP_REFERER'])

class RemoveAllFromCartView(View):
  def get(self, request, product_pk):
    # Obten el cliente
    user_profile = Profile.objects.get(user=request.user)
    cliente = Cliente.objects.get(user_profile=user_profile)
    # Obtén el producto que queremos añadir al carrito
    producto = Producto.objects.get(pk=product_pk)
    # Obtén/Crea un/el pedido en proceso (EP) del usuario
    pedido, _ = Pedido.objects.get_or_create(cliente=cliente, estado='En Proceso')
    # Obtén/Crea un/el detalle de pedido
    detalle_pedido = DetallePedido.objects.get(
      producto=producto,
      pedido=pedido,
    )
    detalle_pedido.delete()
    return redirect(request.META['HTTP_REFERER'])

class PedidoDetailView(DetailView):
  model = Pedido
  template_name = 'main/pedido_detail.html'
  def get_object(self):
    # Obten el cliente
    user_profile = Profile.objects.get(user=self.request.user)
    cliente = Cliente.objects.get(user_profile=user_profile)
    # Obtén/Crea un/el pedido en proceso (EP) del usuario
    pedido, existe = Pedido.objects.get_or_create(cliente=cliente, estado='En Proceso')
    pedido.fecha_creacion = datetime.datetime.now()
    pedido.save()
    return pedido
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['detalles'] = context['object'].detallepedido_set.all()
    return context

class PedidoUpdateView(UpdateView):
  model = Pedido
  fields = ['localizacion', 'direccion_entrega','tipo_comprobante']
  success_url = reverse_lazy('payment')

  def form_valid(self, form):
    # This method is called when valid form data has been POSTed.
    # It should return an HttpResponse.
    self.object = form.save(commit=False)
    # Calculo de tarifa
    self.object.tarifa = randint(5, 20)
    return super().form_valid(form)

class PaymentView(TemplateView):
  template_name = "main/payment.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    # Obten el cliente
    user_profile = Profile.objects.get(user=self.request.user)
    cliente = Cliente.objects.get(user_profile=user_profile)
    context['pedido'] = Pedido.objects.get(cliente=cliente, estado='En Proceso')

    return context

class CompletePaymentView(View):
  def get(self, request):
    # Obten el cliente
    user_profile = Profile.objects.get(user=request.user)
    cliente = Cliente.objects.get(user_profile=user_profile)
    # Obtén/Crea un/el pedido en proceso (EP) del usuario
    pedido = Pedido.objects.get(cliente=cliente, estado='En Proceso')
    # Cambia el estado del pedido
    pedido.estado = 'Pagado'
    # Asignacion de repartidor
    pedido.repartidor = Colaborador.objects.order_by('?').first()
    # Guardamos los cambios
    pedido.save()
    messages.success(request, 'Gracias por tu compra! Un repartidor ha sido asignado a tu pedido.')
    return redirect('home')

class PedidosListView(ListView):
  model = Pedido

  def get_queryset(self):
    user_profile = Profile.objects.get(user=self.request.user)
    cliente = Cliente.objects.get(user_profile=user_profile)
    if cliente is not None:
      object_list = Pedido.objects.filter(cliente_id=cliente.pk)
      return object_list
    else:
      return Pedido.objects.all()

class PedidoCliente(DetailView):
  model = Pedido
  template_name = 'main/pedido_cliente.html'
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['detallespedido'] = context['object'].detallepedido_set.all()
    return context

class cancelarPedido(View):
  def get(self, request, pedido_pk):
    # Obten el cliente
    user_profile = Profile.objects.get(user=request.user)
    cliente = Cliente.objects.get(user_profile=user_profile)
    pedidocod = Pedido.objects.get(pk=pedido_pk)
    # Obtén el pedido que se quiere cancelar
    pedido = Pedido.objects.get(cliente=cliente, pk=pedidocod.pk)
    # Cambia el estado del pedido
    pedido.estado = 'Cancelado'
    # Guardamos los cambios
    pedido.save()
    return redirect(request.META['HTTP_REFERER'])

class confirmarPedido(View):
  def get(self, request, pedido_pk):
    # Obten el cliente
    user_profile = Profile.objects.get(user=request.user)
    cliente = Cliente.objects.get(user_profile=user_profile)
    pedidocod = Pedido.objects.get(pk=pedido_pk)
    # Obtén el pedido que se quiere cancelar
    pedido = Pedido.objects.get(cliente=cliente, pk=pedidocod.pk)
    # Cambia el estado del pedido
    pedido.estado = 'Entregado'
    pedido.fecha_entrega = datetime.datetime.now()
    # Guardamos los cambios
    pedido.save()
    return redirect(request.META['HTTP_REFERER'])