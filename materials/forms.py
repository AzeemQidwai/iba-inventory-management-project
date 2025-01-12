from django import forms

class MaterialSearchForm(forms.Form):
    material_code = forms.CharField(label='Material Code', max_length=100)

