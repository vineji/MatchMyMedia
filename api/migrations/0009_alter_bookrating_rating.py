# Generated by Django 5.1.6 on 2025-03-18 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0008_remove_bookrating_user_bookrating_user_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bookrating",
            name="rating",
            field=models.FloatField(),
        ),
    ]
