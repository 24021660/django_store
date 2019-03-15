# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from mongoengine import *



















class NetstoreGoods(Document):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    picture = models.CharField(max_length=100)
    desc = models.TextField()

    class Meta:
        managed = False
        db_table = 'netstore_goods'


class NetstoreUser(Document):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.CharField(max_length=254)

    class Meta:
        managed = False
        db_table = 'netstore_user'


class Sysdiagrams(Document):
    name = models.CharField(max_length=128)
    principal_id = models.IntegerField()
    diagram_id = models.AutoField(primary_key=True)
    version = models.IntegerField(blank=True, null=True)
    definition = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sysdiagrams'
        unique_together = (('principal_id', 'name'),)


class TbBookinfo(Document):
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


class TbClass(Document):
    classid = models.IntegerField(db_column='ClassID', primary_key=True)  # Field name made lowercase.
    classname = models.CharField(db_column='ClassName', max_length=50)  # Field name made lowercase.
    categoryurl = models.CharField(db_column='CategoryUrl', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tb_Class'


class TbMember(Document):
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


class TbOrderinfo(Document):
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


class TbAdmin(Document):
    admin_id = models.AutoField(primary_key=True)
    admin_name = models.CharField(max_length=50)
    admin_password = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_admin'


class TbDetail(Document):
    detailid = models.IntegerField(db_column='DetailID', primary_key=True)  # Field name made lowercase.
    bookid = models.ForeignKey(TbBookinfo, models.DO_NOTHING, db_column='BookID')  # Field name made lowercase.
    num = models.IntegerField(db_column='Num')  # Field name made lowercase.
    orderid = models.ForeignKey(TbOrderinfo, models.DO_NOTHING, db_column='OrderID')  # Field name made lowercase.
    totalprice = models.FloatField(db_column='TotalPrice')  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=200)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tb_detail'


class TbImage(Document):
    imageid = models.IntegerField(db_column='ImageID')  # Field name made lowercase.
    imagename = models.CharField(db_column='ImageName', max_length=50)  # Field name made lowercase.
    imageurl = models.CharField(db_column='ImageUrl', max_length=200)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tb_image'
