# Generated by Django 4.2.7 on 2024-01-24 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tehreer', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activitylog',
            options={'ordering': ['-timestamp']},
        ),
        migrations.AddIndex(
            model_name='activitylog',
            index=models.Index(fields=['performer'], name='tehreer_act_perform_02e24a_idx'),
        ),
        migrations.AddIndex(
            model_name='activitylog',
            index=models.Index(fields=['target_user'], name='tehreer_act_target__f83342_idx'),
        ),
    ]
