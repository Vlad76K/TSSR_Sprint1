# Generated by Django 4.2.7 on 2023-11-08 16:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pereval_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='perevaladded',
            name='obj_status',
        ),
        migrations.DeleteModel(
            name='StatusObjects',
        ),
        migrations.AddField(
            model_name='perevaladded',
            name='obj_status',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='pereval_app.statuslist'),
        ),
    ]
