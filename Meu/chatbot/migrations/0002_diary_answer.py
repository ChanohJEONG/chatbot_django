# Generated by Django 3.0.5 on 2020-06-10 07:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='diary_answer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('day', models.DateField(blank=True, null=True)),
                ('question', models.CharField(max_length=200)),
                ('useranswer', models.CharField(max_length=200)),
                ('m', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='chatbot.Member')),
            ],
            options={
                'db_table': 'diary_answer',
            },
        ),
    ]