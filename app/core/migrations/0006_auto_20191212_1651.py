# Generated by Django 3.0 on 2019-12-12 16:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_recipe_image_field'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='image_field',
            new_name='image',
        ),
    ]