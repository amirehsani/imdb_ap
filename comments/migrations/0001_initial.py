# Generated by Django 4.1.3 on 2022-11-22 08:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('movies', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MovieComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('status', models.PositiveSmallIntegerField(choices=[(10, 'Created'), (20, 'Approved'), (30, 'Rejected'), (40, 'Deleted')], default=10)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.movie')),
                ('parent_comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comments.moviecomment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s', to=settings.AUTH_USER_MODEL)),
                ('validated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='validated_%(class)s', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CrewComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('status', models.PositiveSmallIntegerField(choices=[(10, 'Created'), (20, 'Approved'), (30, 'Rejected'), (40, 'Deleted')], default=10)),
                ('crew', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.crew')),
                ('parent_comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comments.crewcomment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s', to=settings.AUTH_USER_MODEL)),
                ('validated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='validated_%(class)s', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
