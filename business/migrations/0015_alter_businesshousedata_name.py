# Generated by Django 5.0.6 on 2024-06-11 18:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "business",
            "0014_businesshousedata_remove_financialdata_discount_rate_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="businesshousedata",
            name="name",
            field=models.CharField(max_length=100),
        ),
    ]