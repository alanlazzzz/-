# Generated by Django 2.2.1 on 2019-06-28 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0003_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Info',
            fields=[
                ('infoid', models.AutoField(primary_key=True, serialize=False)),
                ('picid', models.CharField(max_length=1000)),
                ('textid', models.CharField(max_length=100)),
                ('date', models.CharField(max_length=100)),
                ('praisecounr', models.CharField(max_length=100)),
                ('kinds', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=70)),
            ],
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
