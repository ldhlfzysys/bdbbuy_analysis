# Generated by Django 2.1.2 on 2018-11-06 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('car_id', models.AutoField(primary_key=True, serialize=False)),
                ('customer_id', models.IntegerField(blank=True, null=True)),
                ('coupon_id', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'car',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CarProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car_id', models.IntegerField(blank=True, null=True)),
                ('product_id', models.IntegerField(blank=True, null=True)),
                ('product_count', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'car_product',
                'managed': False,
            },
        ),
    ]
