# Generated by Django 5.0.6 on 2024-06-07 07:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("business", "0004_rename_future_date_selfbankinvestment_roi_date_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="selfbankinvestment",
            name="created_date",
            field=models.DateField(auto_now_add=True),
        ),
    ]
