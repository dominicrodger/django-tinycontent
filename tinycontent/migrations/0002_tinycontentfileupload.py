from django.db import models, migrations
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tinycontent', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TinyContentFileUpload',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'The name of the file.', max_length=60)),
                ('slug', autoslug.fields.AutoSlugField(unique=True, editable=False)),
                ('file', models.FileField(upload_to=b'tinycontent/uploads')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('-created',),
                'verbose_name': 'File upload',
            },
        ),
    ]
