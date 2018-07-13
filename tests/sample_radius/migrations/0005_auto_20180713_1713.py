# Generated by Django 2.0.5 on 2018-07-13 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sample_radius', '0004_auto_20180708_1237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='radiuscheck',
            name='attribute',
            field=models.CharField(choices=[('Max-Daily-Session', 'Max-Daily-Session'), ('Max-All-Session', 'Max-All-Session'), ('Max-Daily-Session-Traffic', 'Max-Daily-Session-Traffic'), ('Cleartext-Password', 'Cleartext-Password'), ('NT-Password', 'NT-Password'), ('LM-Password', 'LM-Password'), ('MD5-Password', 'MD5-Password'), ('SMD5-Password', 'SMD5-Password'), ('SHA-Password', 'SHA-Password'), ('SSHA-Password', 'SSHA-Password'), ('Crypt-Password', 'Crypt-Password')], default='NT-Password', max_length=64, verbose_name='attribute'),
        ),
    ]
