# Generated by Django 2.2 on 2019-06-02 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_auto_20190529_0120'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='creator',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
