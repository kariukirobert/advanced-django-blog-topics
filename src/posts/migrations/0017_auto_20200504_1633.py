# Generated by Django 2.1 on 2020-05-04 13:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0016_auto_20200504_1630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='posts',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='posts.PostTopic'),
        ),
    ]
