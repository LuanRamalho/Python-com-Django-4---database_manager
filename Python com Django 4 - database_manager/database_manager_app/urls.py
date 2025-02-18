from django.urls import path
from .views import home, register, create_database, edit_database, delete_database, database_detail, create_table, edit_table, delete_table, table_detail, create_column, edit_column, delete_column, add_data, edit_data, delete_data, search_data

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('create_database/', create_database, name='create_database'),
    path('database/edit/<int:db_id>/', edit_database, name='edit_database'),
    path('database/delete/<int:db_id>/', delete_database, name='delete_database'),
    path('database/<int:db_id>/', database_detail, name='database_detail'),
    path('database/<int:db_id>/create_table/', create_table, name='create_table'),
    path('table/edit/<int:table_id>/', edit_table, name='edit_table'),
    path('table/delete/<int:table_id>/', delete_table, name='delete_table'),
    path('table/<int:table_id>/', table_detail, name='table_detail'),
    path('table/<int:table_id>/create_column/', create_column, name='create_column'),
    path('column/edit/<int:column_id>/', edit_column, name='edit_column'),
    path('column/delete/<int:column_id>/', delete_column, name='delete_column'),
    path('table/<int:table_id>/add_data/', add_data, name='add_data'),
    path('table/edit_data/<int:item_id>/', edit_data, name='edit_data'),
    path('table/delete_data/<int:item_id>/', delete_data, name='delete_data'),
    path('table/<int:table_id>/search/', search_data, name='search_data'),
]