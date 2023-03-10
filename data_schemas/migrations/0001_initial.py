# Generated by Django 4.1.7 on 2023-03-09 10:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Schema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=203)),
                ('column_separator', models.CharField(choices=[(',', 'Comma(,)'), (';', 'Semicolon(;)'), ('|', 'Pipe(|)'), (' ', 'Space( )'), ('\\t', 'Tab(   )')], max_length=10)),
                ('string_character', models.CharField(choices=[('"', 'Double Quote(")'), ("'", "Single Quote(')")], max_length=1)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CSVFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='csv_files/')),
                ('created_date', models.DateField(auto_now_add=True)),
                ('schema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_schemas.schema')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Column',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=202)),
                ('column_type', models.CharField(choices=[('Full Name', 'Full Name'), ('Job', 'Job'), ('Email', 'Email'), ('Domain Name', 'Domain Name'), ('Phone Number', 'Phone Number'), ('Company Name', 'Company Name'), ('Text', 'Text'), ('Integer', 'Integer'), ('Address', 'Address'), ('Date', 'Date')], max_length=20)),
                ('from_int', models.IntegerField(blank=True, null=True)),
                ('to_int', models.IntegerField(blank=True, null=True)),
                ('column_order', models.PositiveIntegerField()),
                ('schema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_schemas.schema')),
            ],
        ),
    ]
