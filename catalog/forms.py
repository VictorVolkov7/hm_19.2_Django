from django import forms
from django.forms import BaseInlineFormSet

from catalog.models import Product, Version


class StyleFormMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, forms.ModelForm):
    BANWORD = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

    class Meta:
        model = Product
        fields = '__all__'

    def clean_name(self):
        cleaned_data = self.cleaned_data.get('name')
        if cleaned_data in ProductForm.BANWORD:
            raise forms.ValidationError('Присутствуют запрещенные слова в названии')
        return cleaned_data

    def clean_title(self):
        cleaned_data = self.cleaned_data.get('title')
        if cleaned_data in ProductForm.BANWORD:
            raise forms.ValidationError('Присутствуют запрещенные слова в описании')
        return cleaned_data


class VersionForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Version
        fields = '__all__'
