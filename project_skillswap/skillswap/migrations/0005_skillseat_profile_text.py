# Generated by Django 3.2.7 on 2022-11-17 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skillswap', '0004_alter_skillseat_age'),
    ]

    operations = [
        migrations.AddField(
            model_name='skillseat',
            name='profile_text',
            field=models.CharField(default='よろしくお願いします', max_length=10000, verbose_name='プロフィール文章'),
        ),
    ]
