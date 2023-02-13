# Generated by Django 4.1.5 on 2023-02-07 12:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0003_rename_auther_profile_account_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=50, validators=[django.core.validators.MinLengthValidator(2, 'Category name have to be more than one charecter.')])),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='preview',
            field=models.CharField(default='No preview', max_length=500),
        ),
        migrations.AddField(
            model_name='book',
            name='categories',
            field=models.ManyToManyField(related_name='categories', to='book.category'),
        ),
    ]
