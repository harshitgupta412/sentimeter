# Generated by Django 2.2 on 2020-08-15 11:11

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('sent', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Keys',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.CharField(max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='data',
            name='keyword',
        ),
        migrations.AddField(
            model_name='data',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='data',
            name='keys',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='sent.Keys'),
            preserve_default=False,
        ),
    ]
