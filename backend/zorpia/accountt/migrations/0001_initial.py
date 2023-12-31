# Generated by Django 4.2.7 on 2023-11-15 03:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('username', models.CharField(max_length=255, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('name', models.CharField(max_length=50)),
                ('dob', models.DateField()),
                ('userid', models.IntegerField(unique=True)),
                ('password', models.CharField(max_length=30)),
                ('is_verified', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_blocked', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Userdetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('phone', models.PositiveIntegerField()),
                ('gender', models.CharField(max_length=10, null=True)),
                ('last_seen', models.DateTimeField()),
                ('commenting', models.BooleanField(default=True)),
                ('posting', models.BooleanField(default=True)),
                ('red_flags', models.PositiveIntegerField()),
                ('userr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accountt.customuser')),
            ],
        ),
    ]
