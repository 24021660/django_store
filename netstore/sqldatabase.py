# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AddressList(models.Model):
    address_id = models.CharField(primary_key=True, max_length=50)
    address_name = models.CharField(max_length=50, blank=True, null=True)
    address_level = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'address_list'


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
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
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


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


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


class NetstoreGoods(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    picture = models.CharField(max_length=100)
    desc = models.TextField()

    class Meta:
        managed = False
        db_table = 'netstore_goods'


class NetstoreUser(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.CharField(max_length=254)

    class Meta:
        managed = False
        db_table = 'netstore_user'


class Sysdiagrams(models.Model):
    name = models.CharField(max_length=128)
    principal_id = models.IntegerField()
    diagram_id = models.AutoField(primary_key=True)
    version = models.IntegerField(blank=True, null=True)
    definition = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sysdiagrams'
        unique_together = (('principal_id', 'name'),)


class TbBookinfo(models.Model):
    bookid = models.IntegerField(db_column='BookID', primary_key=True)  # Field name made lowercase.
    classid = models.ForeignKey('TbClass', models.DO_NOTHING, db_column='ClassID')  # Field name made lowercase.
    bookname = models.CharField(db_column='BookName', max_length=50)  # Field name made lowercase.
    bookintroduce = models.TextField(db_column='BookIntroduce')  # Field name made lowercase.
    author = models.CharField(db_column='Author', max_length=50)  # Field name made lowercase.
    company = models.CharField(db_column='Company', max_length=50)  # Field name made lowercase.
    bookurl = models.CharField(db_column='BookUrl', max_length=200)  # Field name made lowercase.
    marketprice = models.FloatField(db_column='MarketPrice')  # Field name made lowercase.
    hotprice = models.FloatField(db_column='HotPrice')  # Field name made lowercase.
    isrefinment = models.BooleanField(db_column='Isrefinment')  # Field name made lowercase.
    ishot = models.BooleanField(db_column='IsHot')  # Field name made lowercase.
    isdiscount = models.BooleanField(db_column='IsDiscount')  # Field name made lowercase.
    loaddate = models.DateTimeField(db_column='LoadDate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tb_BookInfo'


class TbClass(models.Model):
    classid = models.IntegerField(db_column='ClassID', primary_key=True)  # Field name made lowercase.
    classname = models.CharField(db_column='ClassName', max_length=50)  # Field name made lowercase.
    categoryurl = models.CharField(db_column='CategoryUrl', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tb_Class'


class TbMember(models.Model):
    memberid = models.IntegerField(db_column='MemberID', primary_key=True)  # Field name made lowercase.
    username = models.CharField(db_column='UserName', max_length=50)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=50)  # Field name made lowercase.
    realname = models.CharField(db_column='RealName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    sex = models.BooleanField(db_column='Sex', blank=True, null=True)  # Field name made lowercase.
    phonecode = models.CharField(db_column='Phonecode', max_length=20, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=50)  # Field name made lowercase.
    memberlevel = models.IntegerField()
    address_sheng = models.CharField(db_column='Address_sheng', max_length=200, blank=True, null=True)  # Field name made lowercase.
    address_shi = models.CharField(db_column='Address_shi', max_length=50, blank=True, null=True)  # Field name made lowercase.
    address_quxian = models.CharField(db_column='Address_quxian', max_length=50, blank=True, null=True)  # Field name made lowercase.
    address_detail = models.CharField(db_column='Address_detail', max_length=200, blank=True,null=True)  # Field name made lowercase.
    postcode = models.CharField(db_column='PostCode', max_length=10, blank=True, null=True)  # Field name made lowercase.
    loaddate = models.DateTimeField(db_column='LoadDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tb_Member'


class TbOrderinfo(models.Model):
    orderid = models.IntegerField(db_column='OrderID', primary_key=True)  # Field name made lowercase.
    orderdate = models.DateTimeField(db_column='OrderDate')  # Field name made lowercase.
    booksfee = models.FloatField(db_column='BooksFee')  # Field name made lowercase.
    shipfee = models.FloatField(db_column='ShipFee')  # Field name made lowercase.
    totalprice = models.FloatField(db_column='TotalPrice')  # Field name made lowercase.
    shiptype = models.CharField(db_column='ShipType', max_length=50)  # Field name made lowercase.
    receivername = models.CharField(db_column='ReceiverName', max_length=50)  # Field name made lowercase.
    receiverphone = models.CharField(db_column='ReceiverPhone', max_length=20)  # Field name made lowercase.
    receiveraddress = models.CharField(db_column='ReceiverAddress', max_length=200)  # Field name made lowercase.
    receiveremail = models.CharField(db_column='ReceiverEmail', max_length=50)  # Field name made lowercase.
    isconfirm = models.BooleanField(db_column='IsConfirm')  # Field name made lowercase.
    issend = models.BooleanField(db_column='IsSend')  # Field name made lowercase.
    isend = models.BooleanField(db_column='IsEnd')  # Field name made lowercase.
    adminid = models.BooleanField(db_column='AdminID', blank=True, null=True)  # Field name made lowercase.
    confirmtime = models.DateTimeField(db_column='ConfirmTime', blank=True, null=True)  # Field name made lowercase.
    receiverpostcode = models.CharField(db_column='ReceiverPostCode', max_length=10)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tb_OrderInfo'


class TbAdmin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    admin_name = models.CharField(max_length=50)
    admin_password = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_admin'


class TbDetail(models.Model):
    detailid = models.IntegerField(db_column='DetailID', primary_key=True)  # Field name made lowercase.
    bookid = models.ForeignKey(TbBookinfo, models.DO_NOTHING, db_column='BookID')  # Field name made lowercase.
    num = models.IntegerField(db_column='Num')  # Field name made lowercase.
    orderid = models.ForeignKey(TbOrderinfo, models.DO_NOTHING, db_column='OrderID')  # Field name made lowercase.
    totalprice = models.FloatField(db_column='TotalPrice')  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=200)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tb_detail'


class TbImage(models.Model):
    imageid = models.IntegerField(db_column='ImageID')  # Field name made lowercase.
    imagename = models.CharField(db_column='ImageName', max_length=50)  # Field name made lowercase.
    imageurl = models.CharField(db_column='ImageUrl', max_length=200)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tb_image'
