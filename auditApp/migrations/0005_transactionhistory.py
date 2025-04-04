# Generated by Django 5.1.7 on 2025-03-13 16:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auditApp', '0004_alter_transaction_approved_by_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TransactionHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('changed_at', models.DateTimeField(auto_now_add=True)),
                ('field_name', models.CharField(max_length=100)),
                ('old_value', models.CharField(max_length=255, null=True)),
                ('new_value', models.CharField(max_length=255, null=True)),
                ('changed_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to='auditApp.transaction')),
            ],
            options={
                'ordering': ['-changed_at'],
            },
        ),
    ]
