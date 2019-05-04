# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from mongoengine import *


class django_session(Document):
    session_key=StringField()
    session_data=StringField()
    expire_date=DateTimeField()



class TbBookinfo(Document):
    itemname=StringField()
    itemstar=StringField()
    author = StringField()
    publisher_time = DateTimeField()
    publisher=StringField()
    price_n=FloatField()
    price_r=FloatField()
    price_s=FloatField()
    price_e=FloatField()
    pic_path=StringField()
    detail=StringField()
    supplier=StringField()
    itemid=StringField()
    store=StringField()

    class Meta:
        managed = False
        db_table = 'tb_BookInfo'


class TbClass(Document):
    classid = models.IntegerField(db_column='ClassID', primary_key=True)  # Field name made lowercase.
    classname = models.CharField(db_column='ClassName', max_length=50)  # Field name made lowercase.
    categoryurl = models.CharField(db_column='CategoryUrl', max_length=50)  # Field name made lowercase.



class TbMember(Document):
    username = StringField( max_length=50)  # Field name made lowercase.
    password = StringField(max_length=50)  # Field name made lowercase.
    realname = StringField(max_length=50, blank=True, null=True)  # Field name made lowercase.
    is_used = StringField(db_column='Sex', blank=True, null=True)  # Field name made lowercase.
    phonecode = StringField(blank=True, null=True)  # Field name made lowercase.
    email = StringField( max_length=50)  # Field name made lowercase.
    level = StringField()
    address_sheng = StringField(db_column='Address_sheng', max_length=200, blank=True, null=True)  # Field name made lowercase.
    address_shi = StringField(db_column='Address_shi', max_length=50, blank=True, null=True)  # Field name made lowercase.
    duty_people = StringField(db_column='Address_quxian', max_length=50, blank=True, null=True)  # Field name made lowercase.
    detail = StringField(db_column='Address_detail', max_length=200, blank=True,null=True)  # Field name made lowercase.
    register_pic = StringField()  # Field name made lowercase.
    loaddate = DateTimeField(db_column='LoadDate', blank=True, null=True)  #
    userid=StringField()
    logo=StringField()

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
    num = models.IntegerField(db_column='Num')  # Field name made lowercase.
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


class Tbcart(Document):
    cartid=StringField()
    itemid=StringField()
    cartname=StringField()
    cartqty=StringField()
    memberid=StringField()
    membername=StringField()
    cartstatus=StringField()
    approval=StringField()
    price=StringField()
    userid=StringField()
    username=StringField()
    orderdetail=StringField()
    ordertime=StringField()
    class Meta:
        managed = False
        db_table = 'tb_cart'

class Tbcartid(Document):
    cartmemberid=StringField()
    class Meta:
        managed = False
        db_table = 'tb_cartid'

class Tbitempic(Document):
    picid=StringField()
    picclass=StringField()
    picpath=StringField()
    itemid=StringField()

    class Meta:
        managed = False
        db_table = 'tb_itempic'

