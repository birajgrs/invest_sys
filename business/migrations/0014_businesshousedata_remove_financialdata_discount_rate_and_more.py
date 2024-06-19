# Generated by Django 5.0.6 on 2024-06-11 18:32

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "business",
            "0013_financialdata_business_house_selfbankinvestment_name_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="BusinessHouseData",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(default="Default Name", max_length=100)),
                ("description", models.TextField()),
                ("founded_date", models.DateField()),
                ("location", models.CharField(max_length=200)),
                ("website", models.URLField()),
                ("type_of_service_or_product", models.CharField(max_length=200)),
                ("total_investment", models.IntegerField()),
                ("initial_investment", models.IntegerField()),
                ("discount_rate", models.FloatField()),
                ("operational_days", models.IntegerField()),
                ("project_lifetime", models.IntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name="financialdata",
            name="discount_rate",
        ),
        migrations.RemoveField(
            model_name="financialdata",
            name="initial_investment",
        ),
        migrations.RemoveField(
            model_name="financialdata",
            name="operational_days",
        ),
        migrations.RemoveField(
            model_name="financialdata",
            name="project_lifetime",
        ),
        migrations.RemoveField(
            model_name="financialdata",
            name="total_investment",
        ),
        migrations.AlterField(
            model_name="financialdata",
            name="transaction_date",
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="financialdata",
            name="business_house",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="financial_data",
                to="business.businesshousedata",
            ),
        ),
        migrations.DeleteModel(
            name="BusinessHouse",
        ),
    ]
