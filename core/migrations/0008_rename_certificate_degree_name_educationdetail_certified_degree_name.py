# Generated by Django 4.0.4 on 2022-04-26 09:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_remove_educationdetail_course_type_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='educationdetail',
            old_name='certificate_degree_name',
            new_name='certified_degree_name',
        ),
    ]