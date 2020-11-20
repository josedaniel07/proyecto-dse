from .models import Categoria
def categories_processor(request):
    categories = Categoria.objects.all()
    return {'categorías': categories}
