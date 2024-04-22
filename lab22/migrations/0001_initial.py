# Generated by Django 5.0.4 on 2024-04-09 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cname', models.CharField(max_length=10)),
                ('ccode', models.CharField(max_length=30)),
                ('credits', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Students',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('usn', models.CharField(max_length=50)),
                ('sem', models.IntegerField()),
                ('branch', models.CharField(max_length=30)),
                ('sce', models.ManyToManyField(to='lab22.course')),
            ],
        ),
    ]