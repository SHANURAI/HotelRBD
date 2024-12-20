# Generated by Django 4.2.17 on 2024-12-09 23:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Client",
            fields=[
                ("client_id", models.AutoField(primary_key=True, serialize=False)),
                ("fullname", models.CharField(max_length=100)),
                ("year_of_birth", models.IntegerField()),
                ("gender", models.CharField(max_length=1)),
                ("username", models.CharField(max_length=100)),
            ],
            options={
                "db_table": "Clients",
            },
        ),
        migrations.CreateModel(
            name="Post",
            fields=[
                ("post_id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.TextField()),
                ("salary", models.FloatField()),
                ("description", models.TextField(blank=True, null=True)),
            ],
            options={
                "db_table": "Posts",
            },
        ),
        migrations.CreateModel(
            name="Room",
            fields=[
                ("room_id", models.AutoField(primary_key=True, serialize=False)),
                ("type", models.TextField()),
                ("cost_per_night", models.IntegerField()),
            ],
            options={
                "db_table": "Rooms",
            },
        ),
        migrations.CreateModel(
            name="Service",
            fields=[
                ("service_id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.TextField()),
                ("cost", models.FloatField()),
                ("description", models.TextField(blank=True, null=True)),
            ],
            options={
                "db_table": "Services",
            },
        ),
        migrations.CreateModel(
            name="Staff",
            fields=[
                ("staff_id", models.AutoField(primary_key=True, serialize=False)),
                ("fullname", models.CharField(max_length=100)),
                ("year_of_birth", models.IntegerField()),
                ("gender", models.CharField(max_length=1)),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="main.post"
                    ),
                ),
            ],
            options={
                "db_table": "Staff",
            },
        ),
        migrations.CreateModel(
            name="Booking",
            fields=[
                ("booking_id", models.AutoField(primary_key=True, serialize=False)),
                ("check_in_date", models.DateField()),
                ("count_of_nights", models.IntegerField()),
                ("total_booking_cost", models.FloatField()),
                (
                    "client",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="main.client"
                    ),
                ),
                (
                    "room",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="main.room"
                    ),
                ),
            ],
            options={
                "db_table": "Bookings",
            },
        ),
        migrations.CreateModel(
            name="ProvidedService",
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
                ("count_of_services", models.IntegerField()),
                ("total_service_cost", models.FloatField()),
                (
                    "booking",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="main.booking"
                    ),
                ),
                (
                    "service",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="main.service"
                    ),
                ),
                (
                    "staff",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="main.staff"
                    ),
                ),
            ],
            options={
                "db_table": "Provided_Services",
                "unique_together": {("booking", "staff", "service")},
            },
        ),
    ]
