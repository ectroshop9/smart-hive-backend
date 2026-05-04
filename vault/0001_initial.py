# Generated manually for vault.Block
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mac', models.CharField(max_length=17)),
                ('previous_hash', models.CharField(max_length=64)),
                ('block_hash', models.CharField(max_length=64, unique=True)),
                ('data_json', models.TextField()),
                ('signature_b64', models.TextField(blank=True, null=True)),
                ('nonce', models.BigIntegerField(blank=True, null=True)),
                ('timestamp', models.BigIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]
