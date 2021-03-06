# Generated by Django 4.0.1 on 2022-01-13 11:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=35)),
            ],
        ),
        migrations.CreateModel(
            name='Order_item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('visible', models.BooleanField(default=False)),
                ('storage', models.IntegerField()),
                ('image', models.URLField(blank=True, max_length=255)),
                ('name', models.CharField(max_length=55)),
                ('ean', models.CharField(blank=True, db_index=True, max_length=13)),
                ('description', models.TextField(blank=True, max_length=10000, null=True)),
                ('time_create', models.DateTimeField(auto_now_add=True)),
                ('category_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.category')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.unit')),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('completed', 'Wys??ano'), ('in_progress ', 'W realizacji'), ('order_accept ', 'Przyj??to zam??wienie')], max_length=18)),
                ('email', models.EmailField(max_length=128)),
                ('phone_number', models.CharField(blank=True, max_length=12, null=True)),
                ('first_name', models.CharField(max_length=64)),
                ('last_name', models.CharField(max_length=64)),
                ('post_code', models.CharField(max_length=6)),
                ('city', models.CharField(max_length=64)),
                ('adress', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=32)),
                ('description', models.TextField(blank=True, max_length=2000, null=True)),
                ('time_create', models.DateTimeField(auto_now_add=True)),
                ('product_id', models.ManyToManyField(through='home.Order_item', to='home.Product')),
            ],
        ),
        migrations.AddField(
            model_name='order_item',
            name='orders',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.orders'),
        ),
        migrations.AddField(
            model_name='order_item',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.product'),
        ),
    ]
