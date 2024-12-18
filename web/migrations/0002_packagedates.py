# Generated by Django 4.2.4 on 2024-11-14 05:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("web", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="PackageDates",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("available_date", models.DateField()),
                ("destination", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="web.destinationcity")),
            ],
            options={
                "verbose_name": "Package Date",
                "verbose_name_plural": "Package Date",
            },
        ),
    ]
