# Generated by Django 4.0 on 2022-01-26 03:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('accounts', '0004_remove_saleorder_sales_person'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.user'),
        ),
    ]
