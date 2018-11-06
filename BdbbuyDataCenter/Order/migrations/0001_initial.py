# Generated by Django 2.1.2 on 2018-11-06 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MgOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('increment_id', models.CharField(blank=True, max_length=30, null=True)),
                ('state', models.CharField(blank=True, max_length=30, null=True)),
                ('status', models.CharField(blank=True, max_length=30, null=True)),
                ('coupon_code', models.CharField(blank=True, max_length=30, null=True)),
                ('shipping_description', models.CharField(blank=True, max_length=30, null=True)),
                ('customer_id', models.CharField(blank=True, max_length=30, null=True)),
                ('base_grand_total', models.CharField(blank=True, max_length=30, null=True)),
                ('quote_id', models.CharField(blank=True, max_length=30, null=True)),
                ('shipping_address', models.CharField(blank=True, max_length=200, null=True)),
                ('detail_address', models.CharField(blank=True, max_length=200, null=True)),
                ('customer_email', models.CharField(blank=True, max_length=30, null=True)),
                ('firstname', models.CharField(blank=True, max_length=30, null=True)),
                ('lastname', models.CharField(blank=True, max_length=30, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('telephone', models.CharField(blank=True, max_length=30, null=True)),
                ('postcode', models.CharField(blank=True, max_length=30, null=True)),
                ('driver_name', models.CharField(blank=True, max_length=30, null=True)),
            ],
            options={
                'db_table': 'mg_order',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='OrderComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.IntegerField()),
                ('customer_id', models.IntegerField(blank=True, null=True)),
                ('comment_content', models.TextField()),
                ('add_time', models.CharField(blank=True, max_length=32, null=True)),
                ('customer_name', models.CharField(blank=True, max_length=31, null=True)),
            ],
            options={
                'db_table': 'order_comment',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='OrderPay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(blank=True, null=True)),
                ('pay_type', models.IntegerField(blank=True, null=True)),
                ('snap_order_id', models.CharField(blank=True, max_length=50, null=True)),
                ('order_id', models.CharField(blank=True, max_length=50, null=True)),
                ('qr_code', models.CharField(blank=True, max_length=50, null=True)),
                ('pay_status', models.IntegerField(blank=True, null=True)),
                ('amount', models.IntegerField(blank=True, null=True)),
                ('refund', models.IntegerField(blank=True, null=True)),
                ('refund_msg', models.CharField(blank=True, max_length=200, null=True)),
                ('out_trade_no', models.CharField(blank=True, max_length=50, null=True)),
                ('new_order_id', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'order_pay',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('area_id', models.IntegerField(blank=True, null=True)),
                ('create_at', models.DateTimeField(blank=True, null=True)),
                ('customer_id', models.IntegerField(blank=True, null=True)),
                ('status', models.CharField(blank=True, max_length=11, null=True)),
                ('product_total', models.CharField(blank=True, max_length=20, null=True)),
                ('tax_total', models.CharField(blank=True, max_length=20, null=True)),
                ('coupon_total', models.CharField(blank=True, max_length=20, null=True)),
                ('sales_total', models.CharField(blank=True, max_length=20, null=True)),
                ('shipping_total', models.CharField(blank=True, max_length=20, null=True)),
                ('total', models.CharField(blank=True, max_length=20, null=True)),
                ('customer_coupon_id', models.IntegerField(blank=True, null=True)),
                ('shipping_address', models.TextField(blank=True, null=True)),
                ('customer_name', models.CharField(blank=True, max_length=30, null=True)),
                ('customer_mobile', models.CharField(blank=True, max_length=30, null=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('product_desc', models.TextField(blank=True, null=True)),
                ('driver_id', models.IntegerField(blank=True, null=True)),
                ('total_pay', models.TextField(blank=True, null=True)),
                ('order_remark', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'orders',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='OrderSpecify',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.IntegerField(blank=True, null=True)),
                ('driver_id', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'order_specify',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='OrdersTest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(blank=True, max_length=20, null=True)),
                ('area_id', models.IntegerField(blank=True, null=True)),
                ('create_at', models.DateTimeField(blank=True, null=True)),
                ('customer_id', models.IntegerField(blank=True, null=True)),
                ('status', models.CharField(blank=True, max_length=11, null=True)),
                ('product_total', models.CharField(blank=True, max_length=20, null=True)),
                ('tax_total', models.CharField(blank=True, max_length=20, null=True)),
                ('coupon_total', models.CharField(blank=True, max_length=20, null=True)),
                ('sales_total', models.CharField(blank=True, max_length=20, null=True)),
                ('shipping_total', models.CharField(blank=True, max_length=20, null=True)),
                ('total', models.CharField(blank=True, max_length=20, null=True)),
                ('customer_coupon_id', models.IntegerField(blank=True, null=True)),
                ('shipping_address', models.TextField(blank=True, null=True)),
                ('customer_name', models.CharField(blank=True, max_length=30, null=True)),
                ('customer_mobile', models.CharField(blank=True, max_length=30, null=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('product_desc', models.TextField(blank=True, null=True)),
                ('driver_id', models.IntegerField(blank=True, null=True)),
                ('total_pay', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'orders_test',
                'managed': False,
            },
        ),
    ]