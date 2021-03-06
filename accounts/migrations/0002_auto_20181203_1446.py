# Generated by Django 2.1.3 on 2018-12-03 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_customer',
            field=models.BooleanField(default=False, help_text='Customers can have accounts with the bank.', verbose_name='customer'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_teller',
            field=models.BooleanField(default=False, help_text='Tellers have permissions for creating customers', verbose_name='teller'),
        ),
    ]
