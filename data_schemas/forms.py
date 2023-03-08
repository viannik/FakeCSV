from django import forms
from django.forms import inlineformset_factory

from .models import *


class SchemaForm(forms.ModelForm):
	class Meta:
		model = Schema
		fields = ['name', 'column_separator', 'string_character']
		widgets = {
			'name': forms.TextInput(attrs={'class': 'form-control'}),
			'column_separator': forms.Select(choices=COLUMN_SEPARATORS),
			'string_character': forms.Select(choices=STRING_CHARACTERS),
		}


class ColumnForm(forms.ModelForm):
	class Meta:
		model = Column
		fields = ['name', 'column_type', 'from_int', 'to_int', 'column_order']
		widgets = {
			'name': forms.TextInput(attrs={'class': 'form-control'}),
			'column_type': forms.Select(choices=COLUMN_TYPES, attrs={'onchange': "type_changed(this);"}),
			'from_int': forms.NumberInput(attrs={'class': 'form-control'}),
			'to_int': forms.NumberInput(attrs={'class': 'form-control'}),
			'column_order': forms.NumberInput(attrs={'class': 'form-control'}),
			'DELETE': forms.HiddenInput(),
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['column_order'].initial = 1


ColumnFormSet = inlineformset_factory(Schema, Column, form=ColumnForm, extra=1)


class CSVFileForm(forms.Form):
	rows = forms.IntegerField(min_value=1, widget=forms.NumberInput(
		attrs={
			'class': "form-control",
		}
	))
