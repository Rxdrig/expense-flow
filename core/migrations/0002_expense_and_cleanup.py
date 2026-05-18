from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Expense",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=120)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=12)),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("food", "Food"),
                            ("transport", "Transport"),
                            ("entertainment", "Entertainment"),
                            ("games", "Games"),
                            ("subscriptions", "Subscriptions"),
                            ("education", "Education"),
                            ("other", "Other"),
                        ],
                        default="other",
                        max_length=20,
                    ),
                ),
                ("date", models.DateField()),
                ("description", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="expenses", to=settings.AUTH_USER_MODEL),
                ),
            ],
            options={"ordering": ["-date", "-created_at"]},
        ),
        migrations.DeleteModel(name="Heroe"),
        migrations.DeleteModel(name="TipoHeroe"),
    ]
