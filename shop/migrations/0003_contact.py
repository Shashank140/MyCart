# Generated by Django 3.1.7 on 2021-04-25 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20210416_0114'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('msg_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('email', models.CharField(default='', max_length=100)),
                ('phone', models.CharField(default='', max_length=100)),
                ('desc', models.CharField(default='', max_length=5000)),
            ],
        ),
    ]
