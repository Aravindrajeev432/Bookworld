

from .models import Category
from django import forms

class category_form(forms.ModelForm):
    
    class Meta:
        model = Category
        category_name_field= forms.RegexField(regx = "/^\S*$/")
        fields = ['category_name',]