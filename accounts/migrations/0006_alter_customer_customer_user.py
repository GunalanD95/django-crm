# Generated by Django 4.0 on 2022-01-27 02:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('accounts', '0005_alter_customer_customer_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.user'),
        ),
    ]
