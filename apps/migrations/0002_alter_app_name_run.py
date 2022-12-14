# Generated by Django 4.1.2 on 2022-10-29 23:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='app',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.CreateModel(
            name='Run',
            fields=[
                ('created', models.DateTimeField()),
                ('containerId', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('app_name', models.CharField(max_length=100)),
                ('image', models.CharField(max_length=200)),
                ('command', models.CharField(max_length=200)),
                ('envs', models.JSONField()),
                ('app', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.app')),
            ],
        ),
    ]
