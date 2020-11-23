from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Localizacion, Categoria

from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _
from django.core.validators import BaseValidator
from datetime import date

def calculate_age(born):
    today = date.today()
    return today.year - born.year - \
           ((today.month, today.day) < (born.month, born.day))

@deconstructible
class MinAgeValidator(BaseValidator):
    message = _("Debes ser mayor de 18 para poder registrarte %(limit_value)d.")
    code = 'min_age'

    def compare(self, a, b):
        return calculate_age(a) < b

class ClienteUserForm(UserCreationForm):
    # django.contrib.auth.User attributes
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    email = forms.EmailField(max_length=150)
    # Profile attributes
    documento_identidad = forms.CharField(max_length=8)
    fecha_nacimiento = forms.DateField(validators=[MinAgeValidator(18)])
    ## Opciones de genero
    MASCULINO = 'MA'
    FEMENINO = 'FE'
    NO_BINARIO = 'NB'
    GENERO_CHOICES = [
        (MASCULINO, 'Masculino'),
        (FEMENINO, 'Femenino'),
        (NO_BINARIO, 'No Binario')
    ]
    genero = forms.ChoiceField(choices=GENERO_CHOICES)
    # Cliente attributes
    RUC = forms.CharField(max_length=11, required=False)
    preferencias = forms.ModelChoiceField(queryset=Categoria.objects.all(), required=False)
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'documento_identidad',
            'fecha_nacimiento',
            'genero',
            'RUC',
            'preferencias',
        ]
class ColaboradorUserForm(UserCreationForm):
    # django.contrib.auth.User attributes
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    email = forms.EmailField(max_length=150)
    # Profile attributes
    documento_identidad = forms.CharField(max_length=8)
    fecha_nacimiento = forms.DateField()
    estado = forms.CharField(max_length=3)
    ## Opciones de genero
    MASCULINO = 'MA'
    FEMENINO = 'FE'
    NO_BINARIO = 'NB'
    GENERO_CHOICES = [
        (MASCULINO, 'Masculino'),
        (FEMENINO, 'Femenino'),
        (NO_BINARIO, 'No Binario')
    ]
    genero = forms.ChoiceField(choices=GENERO_CHOICES)
    # Colaborador attributes
    reputacion = forms.FloatField(required=False)
    cobertura_entrega = forms.ModelChoiceField(queryset=Localizacion.objects.all(), required=False)
    numero = forms.CharField(max_length=9)
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'numero',
            'documento_identidad',
            'fecha_nacimiento',
            'estado',
            'genero',
            'reputacion',
            'cobertura_entrega',
        ]