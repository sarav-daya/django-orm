# Generated by Django 3.2.7 on 2021-09-02 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_product_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='zip',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]