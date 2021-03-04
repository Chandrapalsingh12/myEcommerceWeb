# Generated by Django 3.1.6 on 2021-02-14 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20210210_0518'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('msg_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('email', models.CharField(default='', max_length=30)),
                ('phone', models.IntegerField(default='', max_length=20)),
                ('message', models.CharField(default='', max_length=550)),
            ],
        ),
    ]
