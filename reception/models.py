# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class HostsConfigwarning(models.Model):
    ip = models.CharField(max_length=50)
    diskwarning = models.SmallIntegerField()
    networkwarning = models.IntegerField()
    networkwarningtime = models.CharField(max_length=50)
    cpuwarning = models.SmallIntegerField()
    cpuwarningtime = models.CharField(max_length=50)
    memorywarning = models.IntegerField()
    memorywarningtime = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'hosts_configwarning'


class HostsInformation(models.Model):
    ip = models.CharField(max_length=50, blank=True, null=True)
    system = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    key = models.CharField(max_length=50, blank=True, null=True)
    group = models.CharField(max_length=50, blank=True, null=True)
    disk = models.CharField(max_length=50, blank=True, null=True)
    cpu = models.CharField(max_length=50, blank=True, null=True)
    memmory = models.CharField(max_length=50, blank=True, null=True)
    bandwidth = models.IntegerField(blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hosts_information'


class HostsNormal(models.Model):
    ip = models.CharField(primary_key=True, max_length=50)
    disk = models.CharField(max_length=50, blank=True, null=True)
    bandwidth = models.CharField(max_length=50, blank=True, null=True)
    memmory = models.CharField(max_length=50, blank=True, null=True)
    cpu = models.CharField(max_length=50, blank=True, null=True)
    newtime = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hosts_normal'


class HostsNormalAll(models.Model):
    ip = models.CharField(max_length=50)
    disk = models.CharField(max_length=50, blank=True, null=True)
    bandwidth = models.CharField(max_length=50, blank=True, null=True)
    memmory = models.CharField(max_length=50, blank=True, null=True)
    cpu = models.CharField(max_length=50, blank=True, null=True)
    newtime = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hosts_normal_all'


class HostsUser(models.Model):
    username = models.CharField(primary_key=True, max_length=50)
    userpass = models.CharField(max_length=50)
    changepassword = models.DateTimeField(blank=True, null=True)
    level = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hosts_user'


class HostsUserlog(models.Model):
    username = models.CharField(max_length=50, blank=True, null=True)
    trypass = models.CharField(db_column='Trypass', max_length=50, blank=True, null=True)  # Field name made lowercase.
    time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hosts_userlog'


class HostsWhoerror(models.Model):
    ip = models.CharField(primary_key=True, max_length=50)
    disk = models.CharField(max_length=50, blank=True, null=True)
    bandwidth = models.CharField(max_length=50, blank=True, null=True)
    memmory = models.CharField(max_length=50, blank=True, null=True)
    cpu = models.CharField(max_length=50, blank=True, null=True)
    newtime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hosts_whoerror'


class HostsWhoerrorAll(models.Model):
    ip = models.CharField(max_length=50)
    disk = models.CharField(max_length=50, blank=True, null=True)
    bandwidth = models.CharField(max_length=50, blank=True, null=True)
    memmory = models.CharField(max_length=50, blank=True, null=True)
    cpu = models.CharField(max_length=50, blank=True, null=True)
    newtime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hosts_whoerror_all'


class HostsWholesale(models.Model):
    ip = models.CharField(max_length=50, blank=True, null=True)
    network = models.CharField(max_length=50, blank=True, null=True)
    cpu = models.CharField(max_length=50, blank=True, null=True)
    mem = models.CharField(max_length=50, blank=True, null=True)
    disk = models.CharField(max_length=100, blank=True, null=True)
    newtime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hosts_wholesale'


class HostsWhowarning(models.Model):
    ip = models.CharField(primary_key=True, max_length=50)
    disk = models.CharField(max_length=50, blank=True, null=True)
    bandwidth = models.CharField(max_length=50, blank=True, null=True)
    memmory = models.CharField(max_length=50, blank=True, null=True)
    cpu = models.CharField(max_length=50, blank=True, null=True)
    newtime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hosts_whowarning'


class HostsWhowarningAll(models.Model):
    ip = models.CharField(max_length=50)
    disk = models.CharField(max_length=50, blank=True, null=True)
    bandwidth = models.CharField(max_length=50, blank=True, null=True)
    memmory = models.CharField(max_length=50, blank=True, null=True)
    cpu = models.CharField(max_length=50, blank=True, null=True)
    newtime = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hosts_whowarning_all'
