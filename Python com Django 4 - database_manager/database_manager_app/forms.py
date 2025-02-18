from django import forms
from .models import Database, Table, Column, DataItem

class DataEntryForm(forms.Form):
    def __init__(self, *args, **kwargs):
        columns = kwargs.pop('columns')
        super(DataEntryForm, self).__init__(*args, **kwargs)
        for column in columns:
            self.fields[column.name] = forms.CharField(label=column.name)

class EditDataForm(forms.ModelForm):
    class Meta:
        model = DataItem
        fields = ['value']

class EditDatabaseForm(forms.ModelForm):
    class Meta:
        model = Database
        fields = ['name']

class EditTableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ['name']

class EditColumnForm(forms.ModelForm):
    class Meta:
        model = Column
        fields = ['name', 'column_type']