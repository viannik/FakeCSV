import csv
import os
import random
import tempfile
import uuid

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from faker import Faker

from .forms import *
from .models import *


@login_required
def schema_list(request):
    schemas = Schema.objects.filter(owner=request.user).order_by('-modified_date')
    return render(request, 'data_schemas/schema_list.html', {'schemas': schemas, 'header': 'Data Schemas'})


@login_required
def schema_create(request):
    schema_form = SchemaForm()
    formset = ColumnFormSet()

    if request.method == 'POST':
        schema_form = SchemaForm(request.POST)
        formset = ColumnFormSet(request.POST)
        if schema_form.is_valid() and formset.is_valid():
            schema = schema_form.save(commit=False)
            schema.owner = request.user
            schema.save()
            for form in formset:
                column = form.save(commit=False)
                column.schema = schema
                column.save()
            messages.success(request, 'Schema created successfully!')
            return redirect('schema_list')

    context = {
        'schema_form': schema_form,
        'formset': formset,
        'header': 'Schema create'
    }
    return render(request, 'data_schemas/schema_update.html', context)


@login_required
def schema_update(request, pk):
    schema = get_object_or_404(Schema, pk=pk)
    ColumnFormSet = inlineformset_factory(Schema, Column, form=ColumnForm, extra=0, can_delete=True)
    if request.method == 'POST':
        schema_form = SchemaForm(request.POST, instance=schema)
        formset = ColumnFormSet(request.POST, instance=schema)
        if schema_form.is_valid() and formset.is_valid():
            schema_form.save()
            formset.save()
            return redirect('schema_list')
    else:
        schema_form = SchemaForm(instance=schema)
        formset = ColumnFormSet(instance=schema)
    context = {
        'schema_form': schema_form,
        'formset': formset,
        'header': 'Schema update'
    }
    return render(request, 'data_schemas/schema_update.html', context)


@login_required
def schema_delete(request, pk):
    Schema.objects.filter(pk=pk).delete()
    return redirect('schema_list')


def generate_data(data_type, from_int=None, to_int=None):
    fake = Faker()
    match data_type:
        case 'Full Name':
            return fake.name()
        case 'Job':
            return fake.job()
        case 'Email':
            return fake.email()
        case 'Domain Name':
            return fake.domain_name()
        case 'Phone Number':
            return fake.phone_number()
        case 'Company Name':
            return fake.company()
        case 'Text':
            num_sentences = random.randint(from_int, to_int)
            return ' '.join(fake.sentences(num_sentences))
        case 'Integer':
            return random.randint(from_int, to_int)
        case 'Address':
            return fake.address()
        case 'Date':
            return fake.date()
        case _:
            return ''


@login_required
def schema_datasets(request, pk):
    schema = get_object_or_404(Schema, pk=pk)
    columns = Column.objects.filter(schema=schema)
    datasets = CSVFile.objects.filter(schema=schema)
    header = 'Schema datasets'

    if request.method == 'POST':
        form = CSVFileForm(request.POST)
        if form.is_valid():
            separator = schema.column_separator
            character = schema.string_character
            num_rows = form.cleaned_data['rows']

            max_order = columns.aggregate(Max('column_order'))['column_order__max']
            headers = [''] * max_order
            for column in columns:
                headers[column.column_order - 1] = column.name

            with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
                file_name = temp_file.name
                writer = csv.writer(temp_file, delimiter=separator, quotechar=character, quoting=csv.QUOTE_ALL)
                writer.writerow(headers)

                for i in range(num_rows):
                    row = [''] * max_order
                    for column in columns:
                        row[column.column_order - 1] = str(generate_data(column.column_type, column.from_int, column.to_int))
                    writer.writerow(row)

            with open(file_name, 'r') as f:
                csv_file = CSVFile(user=request.user, schema=schema)
                csv_file.file.save(f'{schema.name}-{num_rows}.csv', f)

            os.unlink(file_name)
            return redirect('schema_datasets', pk=schema.pk)
    else:
        form = CSVFileForm()

    context = {
        'schema': schema,
        'columns': columns,
        'datasets': datasets,
        'header': header,
        'form': form,
    }
    return render(request, 'data_schemas/schema_datasets.html', context)


def schema_dataset_download(request, pk, dataset_pk):
    dataset = get_object_or_404(CSVFile, pk=dataset_pk)
    response = HttpResponse(dataset.file, content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={dataset.file.name}'
    return response


def schema_dataset_delete(request, pk, dataset_pk):
    CSVFile.objects.filter(pk=dataset_pk).delete()
    return redirect('schema_datasets', pk=pk)
