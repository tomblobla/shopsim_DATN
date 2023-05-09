from django import forms
from .models import Network, Tag

class SIMFilterForm(forms.Form):
    min_price = forms.DecimalField(label='Giá tối thiểu', required=False)
    max_price = forms.DecimalField(label='Giá tối đa', required=False)
    networks = forms.ModelMultipleChoiceField(queryset=Network.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)