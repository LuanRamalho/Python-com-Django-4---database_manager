from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Database, Table, Column, DataItem
from .forms import DataEntryForm, EditDataForm, EditDatabaseForm, EditTableForm, EditColumnForm

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def create_database(request):
    if request.method == 'POST':
        db_name = request.POST['db_name']
        db = Database(name=db_name, owner=request.user)
        db.save()
        return redirect('database_detail', db_id=db.id)
    return render(request, 'create_database.html')

@login_required
def edit_database(request, db_id):
    db = get_object_or_404(Database, id=db_id)
    if request.method == 'POST':
        form = EditDatabaseForm(request.POST, instance=db)
        if form.is_valid():
            form.save()
            return redirect('database_detail', db_id=db.id)
    else:
        form = EditDatabaseForm(instance=db)
    return render(request, 'edit_database.html', {'form': form, 'database': db})

@login_required
def delete_database(request, db_id):
    db = get_object_or_404(Database, id=db_id)
    if request.method == 'POST':
        db.delete()
        return redirect('home')
    return render(request, 'delete_database.html', {'database': db})

@login_required
def database_detail(request, db_id):
    db = get_object_or_404(Database, id=db_id)
    tables = Table.objects.filter(database=db)
    return render(request, 'database_detail.html', {'database': db, 'tables': tables})

@login_required
def create_table(request, db_id):
    if request.method == 'POST':
        table_name = request.POST['table_name']
        db = get_object_or_404(Database, id=db_id)
        table = Table(name=table_name, database=db)
        table.save()
        return redirect('table_detail', table_id=table.id)
    return render(request, 'create_table.html', {'db_id': db_id})

@login_required
def edit_table(request, table_id):
    table = get_object_or_404(Table, id=table_id)
    if request.method == 'POST':
        form = EditTableForm(request.POST, instance=table)
        if form.is_valid():
            form.save()
            return redirect('table_detail', table_id=table.id)
    else:
        form = EditTableForm(instance=table)
    return render(request, 'edit_table.html', {'form': form, 'table': table})

@login_required
def delete_table(request, table_id):
    table = get_object_or_404(Table, id=table_id)
    if request.method == 'POST':
        table.delete()
        return redirect('database_detail', db_id=table.database.id)
    return render(request, 'delete_table.html', {'table': table})

@login_required
def table_detail(request, table_id):
    table = get_object_or_404(Table, id=table_id)
    columns = Column.objects.filter(table=table)
    data_items = DataItem.objects.filter(table=table)
    data = {column.name: [] for column in columns}
    for item in data_items:
        data[item.column.name].append(item)
    return render(request, 'table_detail.html', {'table': table, 'columns': columns, 'data': data})

@login_required
def create_column(request, table_id):
    if request.method == 'POST':
        column_name = request.POST['column_name']
        column_type = request.POST['column_type']
        table = get_object_or_404(Table, id=table_id)
        column = Column(name=column_name, column_type=column_type, table=table)
        column.save()
        return redirect('table_detail', table_id=table.id)
    return render(request, 'create_column.html', {'table_id': table_id})

@login_required
def edit_column(request, column_id):
    column = get_object_or_404(Column, id=column_id)
    if request.method == 'POST':
        form = EditColumnForm(request.POST, instance=column)
        if form.is_valid():
            form.save()
            return redirect('table_detail', table_id=column.table.id)
    else:
        form = EditColumnForm(instance=column)
    return render(request, 'edit_column.html', {'form': form, 'column': column})

@login_required
def delete_column(request, column_id):
    column = get_object_or_404(Column, id=column_id)
    if request.method == 'POST':
        column.delete()
        return redirect('table_detail', table_id=column.table.id)
    return render(request, 'delete_column.html', {'column': column})

@login_required
def add_data(request, table_id):
    table = get_object_or_404(Table, id=table_id)
    columns = Column.objects.filter(table=table)
    if request.method == 'POST':
        form = DataEntryForm(request.POST, columns=columns)
        if form.is_valid():
            for column in columns:
                value = form.cleaned_data[column.name]
                data_item = DataItem(table=table, column=column, value=value)
                data_item.save()
            return redirect('table_detail', table_id=table.id)
    else:
        form = DataEntryForm(columns=columns)
    return render(request, 'add_data.html', {'table': table, 'form': form})

@login_required
def edit_data(request, item_id):
    data_item = get_object_or_404(DataItem, id=item_id)
    if request.method == 'POST':
        form = EditDataForm(request.POST, instance=data_item)
        if form.is_valid():
            form.save()
            return redirect('table_detail', table_id=data_item.table.id)
    else:
        form = EditDataForm(instance=data_item)
    return render(request, 'edit_data.html', {'form': form, 'data_item': data_item})

@login_required
def delete_data(request, item_id):
    data_item = get_object_or_404(DataItem, id=item_id)
    table_id = data_item.table.id
    data_item.delete()
    return redirect('table_detail', table_id=table_id)

@login_required
def search_data(request, table_id):
    query = request.GET.get('q', '')
    table = get_object_or_404(Table, id=table_id)
    columns = Column.objects.filter(table=table)
    data_items = DataItem.objects.filter(table=table, value__icontains=query)
    data = {column.name: [] for column in columns}
    for item in data_items:
        data[item.column.name].append(item)
    return render(request, 'table_detail.html', {'table': table, 'columns': columns, 'data': data, 'query': query})