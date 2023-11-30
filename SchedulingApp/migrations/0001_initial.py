# Generated by Django 4.2.7 on 2023-11-29 00:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='defaultcoursename', max_length=50)),
                ('department', models.CharField(default='defaultdept', max_length=20)),
                ('courseNumber', models.IntegerField(default=1234)),
                ('semester', models.CharField(choices=[('spring', 'Spring'), ('summer', 'Summer'), ('fall', 'Fall'), ('winter', 'Winter')], default='fa', max_length=6)),
                ('year', models.IntegerField(default=2023)),
            ],
        ),
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(default='default@uwm.edu', max_length=20)),
                ('password', models.CharField(default='defaultpassword', max_length=20)),
                ('firstName', models.CharField(default='defaultfirstname', max_length=20)),
                ('lastName', models.CharField(default='defaultlastname', max_length=20)),
                ('phoneNumber', models.CharField(default='defaultphonenumber', max_length=20)),
                ('streetAddress', models.CharField(default='1234 Main st', max_length=50)),
                ('city', models.CharField(default='Milwaukee', max_length=20)),
                ('state', models.CharField(default='WI', max_length=2)),
                ('zipcode', models.IntegerField(default=53206)),
                ('role', models.CharField(choices=[('admin', 'Admin'), ('instructor', 'Instructor'), ('ta', 'TA')], default='ad', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sectionNumber', models.IntegerField(default=400)),
                ('type', models.CharField(choices=[('lecture', 'Lecture'), ('grader', 'Grader'), ('lab', 'Lab')], default='le', max_length=7)),
                ('location', models.CharField(default='defaultlocation', max_length=50)),
                ('daysMeeting', models.CharField(default='MTWHF', max_length=7)),
                ('startTime', models.CharField(default='defaultstarttime', max_length=50)),
                ('endTime', models.CharField(default='defaultendtime', max_length=50)),
                ('assignedUser', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='SchedulingApp.myuser')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SchedulingApp.course')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='assignedUser',
            field=models.ManyToManyField(blank=True, to='SchedulingApp.myuser'),
        ),
    ]
