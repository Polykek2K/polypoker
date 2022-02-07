import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_customuser_money'),
    ]

    operations = [
        migrations.AlterField(
            model_name='CustomUser',
            name='username',
            field=models.CharField(max_length=25, unique=True, validators=[django.core.validators.RegexValidator(message='Only alphanumeric characters and _ allowed.', regex='^[0-9a-zA-Z_]*$')]),
        ),
    ]
