from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('productos',views.ProductListView.as_view(), name='product-list'),
    path('productos/<int:pk>',views.ProductDetailView.as_view(), name='product-detail'),
    path('proveedores', views.ProveedorListView.as_view(), name='proveedor-list'),
    path('proveedor/<str:pk>', views.ProveedorDetailView.as_view(), name='proveedor-detail'),
    path('categorias', views.CategoriaListView.as_view(), name='categoria-list'),
    path('categorias/<str:pk>', views.CategoriaDetailView.as_view(), name='categoria-detail'),
    path('localizacion', views.LocalizacionListView.as_view(), name='localizacion-list'),
    path('localizacion/<str:pk>', views.LocalizacionDetailView.as_view(), name='localizacion-detail'),
    path('registro/', views.PreRegister.as_view(), name='register'),
    path('registro/colaborador', views.RegistrationViewColaborador.as_view(), name='colaborador'),
    path('registro/cliente', views.RegistrationViewCliente.as_view(), name='cliente'),
    path('add_to_cart/<int:product_pk>',views.AddToCartView.as_view(), name='add-to-cart'),
    path('remove_from_cart/<int:product_pk>', views.RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('remove_all_from_cart/<int:product_pk>', views.RemoveAllFromCartView.as_view(), name='remove-all-from-cart'),
    path('carrito/', views.PedidoDetailView.as_view(), name='pedido-detail'),
    path('checkout/<int:pk>', views.PedidoUpdateView.as_view(), name='pedido-update'),
    path('payment/', views.PaymentView.as_view(), name='payment'),
    path('complete_payment/', views.CompletePaymentView.as_view(), name='complete-payment'),
    path('pedidos/', views.PedidosListView.as_view(), name='pedido-list'),
    path('pedidos/<int:pk>', views.PedidoCliente.as_view(), name='pedido-cliente'),
    path('cancela/<int:pedido_pk>', views.cancelarPedido.as_view(), name='pedido-cancelado'),
    path('aprueba/<int:pedido_pk>', views.confirmarPedido.as_view(), name='pedido-entregado'),
]