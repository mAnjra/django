# Generated by Django 4.1.6 on 2023-02-21 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("todo", "0002_todo_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="todo",
            name="my_boolean_field",
            field=models.BooleanField(default=False),
        ),
    ]