# Generated by Django 4.0.5 on 2022-07-20 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mine_mgt', '0008_claim_balance_alter_payment_proof_alter_payment_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='claim',
            name='monthly_labour_returns',
            field=models.IntegerField(default=0),
        ),
    ]
