from django.db import models, migrations
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tinycontent', '0002_tinycontentfileupload'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tinycontentfileupload',
            name='slug',
            field=autoslug.fields.AutoSlugField(populate_from=b'name', unique=True, editable=False),
        ),
    ]
