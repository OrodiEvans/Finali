# Generated by Django 4.2.8 on 2023-12-24 18:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('EcommerceApp', '0002_rename_psw_user_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/')),
                ('description', models.CharField(max_length=200)),
                ('price', models.CharField(max_length=50)),
            ],
        ),
    ]
