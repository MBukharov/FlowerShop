# Generated by Django 4.2.18 on 2025-01-30 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_alter_order_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('СБОРКА', 'На сборке'), ('В ПУТИ', 'В доставке'), ('ВЫПОЛННЕН', 'Выполнен'), ('ОТМЕНЕН', 'Отменен')], default='СБОРКА', max_length=10),
        ),
    ]
