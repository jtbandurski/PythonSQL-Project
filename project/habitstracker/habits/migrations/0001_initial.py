# Generated by Django 4.1.5 on 2023-01-15 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('comment_id', models.AutoField(primary_key=True, serialize=False)),
                ('publish_date', models.TextField()),
                ('content', models.TextField()),
            ],
            options={
                'db_table': 'comments',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Habbits',
            fields=[
                ('habbit_id', models.AutoField(primary_key=True, serialize=False)),
                ('habbit_type', models.BinaryField()),
                ('habbit_desc', models.TextField(blank=True, null=True)),
                ('habbit_name', models.TextField()),
                ('habbit_days_target', models.TextField()),
                ('success_activity', models.TextField()),
                ('success_range', models.TextField()),
                ('success_amount', models.TextField()),
                ('success_unit', models.TextField()),
            ],
            options={
                'db_table': 'habbits',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='HabbitsTracker',
            fields=[
                ('habbit_tracker_id', models.AutoField(primary_key=True, serialize=False)),
                ('habbit_type', models.BinaryField()),
                ('date', models.TextField()),
                ('yes_no_value', models.BinaryField(blank=True, null=True)),
                ('success_amount_value', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'habbits_tracker',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('like_id', models.AutoField(primary_key=True, serialize=False)),
                ('publish_date', models.TextField()),
                ('like_value', models.BinaryField()),
            ],
            options={
                'db_table': 'likes',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('post_id', models.AutoField(primary_key=True, serialize=False)),
                ('publish_date', models.TextField()),
                ('content', models.TextField()),
            ],
            options={
                'db_table': 'posts',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UsersList',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_name', models.TextField(unique=True)),
                ('first_name', models.TextField()),
                ('last_name', models.TextField()),
                ('occupation', models.TextField()),
                ('email', models.TextField()),
                ('password', models.TextField()),
            ],
            options={
                'db_table': 'users_list',
                'managed': False,
            },
        ),
    ]
