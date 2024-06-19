# Generated by Django 4.2.11 on 2024-06-19 10:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        (
            "business",
            "0016_rename_daily_expenses_financialdata_daily_expenses_extra_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="financialdata",
            name="business_house_relation",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="financial_data",
                to="business.businesshouserelationship",
            ),
        ),
    ]