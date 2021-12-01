# Generated by Django 3.1.7 on 2021-03-02 04:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_picture', models.ImageField(upload_to='')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Scholarship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('overview', models.TextField()),
                ('content', tinymce.models.HTMLField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('financial_coverage', models.CharField(max_length=100)),
                ('No_of_scholarships', models.IntegerField()),
                ('thumbnail', models.ImageField(upload_to='')),
                ('category', models.CharField(choices=[('Internships', 'Internships'), ('Exchange Programs', 'Exchange Programs'), ('Scholarships', 'Scholarships')], max_length=200, null=True)),
                ('featured', models.BooleanField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Scholarship.author')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField()),
                ('scholarship', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='Scholarship.scholarship')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
