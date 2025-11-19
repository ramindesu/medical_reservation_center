# Accounts/migrations/0003_add_monthly_appointment_limit.py

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='monthly_appointment_limit',
            field=models.IntegerField(default=30),
        ),
    ]
