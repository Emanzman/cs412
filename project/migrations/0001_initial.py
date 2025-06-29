# Generated by Django 5.2.3 on 2025-06-17 20:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.TextField()),
                ('category', models.CharField(choices=[('music', 'Music'), ('history', 'History'), ('geography', 'Geography')])),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='TriviaAttempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField()),
                ('score', models.IntegerField()),
                ('attempt_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(unique=True)),
                ('first_name', models.CharField()),
                ('last_name', models.CharField()),
                ('email', models.EmailField(blank=True, max_length=254, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('admin_user', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionChoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_text', models.CharField()),
                ('correct_choice', models.BooleanField(default=False)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.question')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.question')),
                ('user_choice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.questionchoice')),
                ('trivia_attempt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.triviaattempt')),
            ],
        ),
        migrations.AddField(
            model_name='triviaattempt',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.user'),
        ),
        migrations.AddField(
            model_name='question',
            name='question_creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.user'),
        ),
    ]
