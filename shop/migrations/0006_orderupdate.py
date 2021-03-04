# Generated by Django 3.1.6 on 2021-02-17 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20210216_0547'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderUpdate',
            fields=[
                ('update_id', models.AutoField(primary_key=True, serialize=False)),
                ('order_id', models.IntegerField(default='')),
                ('update_desc', models.CharField(default='', max_length=33330)),
                ('timestamp', models.DateField(auto_now_add=True)),
            ],
        ),
    ]