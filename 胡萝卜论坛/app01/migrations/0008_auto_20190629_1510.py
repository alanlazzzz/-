# Generated by Django 2.2.2 on 2019-06-29 07:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0007_auto_20190629_1457'),
    ]

    operations = [
        migrations.AddField(
            model_name='info',
            name='user',
            field=models.ForeignKey(default='0', on_delete=django.db.models.deletion.CASCADE, to='app01.User'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('commentid', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.CharField(max_length=100)),
                ('date', models.CharField(max_length=100)),
                ('commenter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.User')),
                ('info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.Info')),
            ],
        ),
    ]
