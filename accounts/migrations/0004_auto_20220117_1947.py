import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20220113_1839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='CustomUser',
            name='username',
            field=models.CharField(max_length=25, unique=True, validators=[django.core.validators.RegexValidator(message='Username must consist only of alphanumeric characters and underscores.', regex='^[0-9a-zA-Z_]*$')]),
        ),
    ]
