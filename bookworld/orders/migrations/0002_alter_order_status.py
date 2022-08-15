# Generated by Django 4.0.6 on 2022-08-08 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Processing', 'Processing'), ('Shipped', 'Shipped'), ('Deliverd', 'Deliverd'), ('Cancelled', 'Cancelled')], default='Processing', max_length=10),
        ),
    ]
