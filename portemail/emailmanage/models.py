﻿from django.db import models
from django.contrib.auth.models import User, UserManager
from django.conf import settings
from datetime import datetime

# Create your models here.


class TypeMeta(models.Model):
	cname = models.CharField(u'中文名',max_length=50)
	ename = models.CharField(u'英文名',max_length=50,blank=True)
	ename_abbr = models.CharField(u'英文简称',max_length=20,blank=True)
	class Meta:
		abstract = True



class ShipType(TypeMeta):
	pass



class TermType(TypeMeta):
	pass
	
		
class bagType(TypeMeta):
	pass

class CargoType(TypeMeta):
	pass


class FillChoices:
	@staticmethod
	def get_ship_type_choices():
		r = []
		all_entries = ShipType.objects.all()
		for obj in all_entries:
			r = r + [(obj.id, obj.cname)]
		return r
		
	@staticmethod
	def get_term_type_choices():
		r = []
		all_entries = TermType.objects.all()
		for obj in all_entries:
			r = r + [(obj.id, obj.cname)]
		return r
		
	@staticmethod
	def get_bag_type_choices():
		r = []
		all_entries = BagType.objects.all()
		for obj in all_entries:
			r = r + [(obj.id, obj.cname)]
		return r    
		
	@staticmethod
	def get_bag_type_choices():
		r = []
		all_entries = BagType.objects.all()
		for obj in all_entries:
			r = r + [(obj.id, obj.cname)]
		return r



SHIP_TYPE_CHOICES = (
    ('1', '杂货船'),
    ('2', '散装船'),
    ('3', '多用途船'),
    ('4', '重吊船'),
    ('5', '集装箱船'),
    ('6', '汽船'),
    ('7', '液化气船'),
    ('8', '滚装船'),
    ('9', '化学品船'),
)

TERM_TYPE_CHOICES = (
    ('FLT', 'FLT-班轮条款'),
    ('FIOST', 'FIOST-船东不负责装、卸、堆装、平舱'),
    ('FI', 'FI-船东不负责装'),
    ('FO', 'FO-船东不负责卸'),
    ('FIO', 'FIO-船东不负责装、卸'),
    ('FILO', 'FILO-船东不负责装但负责卸'),
    ('LIFO', 'LIFO-船东负责装不负责卸'),
)

TIME_ZONE_CHOICES = (
    ('0', 'UTC'),
    ('+1', 'UTC+1'),
    ('+2', 'UTC+2'),
    ('+3', 'UTC+3'),
    ('+4', 'UTC+4'),
    ('+5', 'UTC+5'),
    ('+6', 'UTC+6'),
    ('+7', 'UTC+7'),
    ('+8', 'UTC+8'),
    ('+9', 'UTC+9'),
    ('+10', 'UTC+10'),
    ('+11', 'UTC+11'),
    ('12', 'UTC12'),
    ('-11', 'UTC-11'),
    ('-10', 'UTC-10'),
    ('-9', 'UTC-9'),
    ('-8', 'UTC-8'),
    ('-7', 'UTC-7'),
    ('-6', 'UTC-6'),
    ('-5', 'UTC-5'),
    ('-4', 'UTC-4'),
    ('-3', 'UTC-3'),
    ('-2', 'UTC-2'),
    ('-1', 'UTC-1'),    
)

QUANTITY_UNIT_CHOICES = (
    ('1', '吨'),
    ('2', '立方米'),
)

CURRENCY_UNIT_CHOICES = (
    ('1', '美元'),
    ('2', '人民币'),
)


class Area(models.Model):
	cname = models.CharField(u'中文名称',max_length=20)
	ename = models.CharField(u'英文名称',max_length=20)
	def __str__(self):
		return self.cname+'_'+self.ename


class Country(models.Model):
	abbr_cname = models.CharField(u'中文简称',max_length=20)
	full_cname = models.CharField(u'中文全称',max_length=20)
	abbr_ename = models.CharField(u'英文简称',max_length=20)
	full_ename = models.CharField(u'英文全称',max_length=20)
	number_code = models.CharField(u'数字代码',max_length=3)
	english_code_3 = models.CharField(u'英文3码',max_length=3)
	english_code_2 = models.CharField(u'英文2码',max_length=2)
	area = models.ForeignKey(Area, verbose_name=u'区域',on_delete=models.CASCADE)
	def __str__(self):
		return self.abbr_cname


class Port(models.Model):
	port_code = models.CharField(u'港口代码',max_length=20,primary_key =True)
	port_cname = models.CharField(u'港口中文名称',max_length=30)
	port_ename = models.CharField(u'港口英文名称',max_length=50)
	currency = models.CharField(u'货币',max_length=10)
	time_zone= models.CharField(u'时区',max_length=3,choices=TIME_ZONE_CHOICES)
	berth = models.CharField(u'泊位',max_length=256,blank=True)
	max_loa = models.DecimalField(u'最大船长(米)',max_digits=8,decimal_places =2,blank=True, null=True)
	draft_limit = models.DecimalField(u'吃水限制(米)',max_digits=10,decimal_places =3,blank=True, null=True)
	lifts_tons = models.CharField(u'装卸能力',max_length=50,blank=True, null=True)
	ldRate = models.DecimalField(u'装卸率',max_digits=4,decimal_places =2,blank=True, null=True)
	cranes_mobile= models.BooleanField(u'岸吊',blank=True)
	cranes_floating= models.BooleanField(u'浮吊',blank=True)
	web_site = models.CharField(u'网站',max_length=50,blank=True)
	memo = models.TextField(u'备注',max_length=256,blank=True)
	area = models.ForeignKey(Area, verbose_name=u'区域',on_delete=models.CASCADE)
	country = models.ForeignKey(Country, verbose_name=u'国家',on_delete=models.CASCADE)
	def __str__(self):
		return self.port_cname


class Sender(models.Model):
	email = models.EmailField(u'邮箱',max_length=100)
	name = models.CharField(u'姓名',max_length=20)
	post = models.CharField(u'职位',max_length=20,blank=True)
	telephone = models.CharField(u'办公电话',max_length=15)
	mobile = models.CharField(u'手机',max_length=15,blank=True)
	fax = models.CharField(u'传真',max_length=15,blank=True)
	skype = models.CharField(u'skype',max_length=15,blank=True)
	qq = models.CharField(u'QQ',max_length=10,blank=True)
	company_name = models.CharField(u'公司名称',max_length=80,blank=True)
	def __str__(self):
		return self.name
	
class CustomUser(models.Model):
	user = models.OneToOneField(User)
	name = models.CharField(u'姓名',max_length=20,blank=True)
	post = models.CharField(u'职位',max_length=20,blank=True)
	telephone = models.CharField(u'办公电话',max_length=15)
	mobile = models.CharField(u'手机',max_length=15,blank=True)
	fax = models.CharField(u'传真',max_length=15,blank=True)
	skype = models.CharField(u'skype',max_length=15,blank=True)
	qq = models.CharField(u'QQ',max_length=10,blank=True)
	company_name = models.CharField(u'公司名称',max_length=80,blank=True)
	register_time = models.DateTimeField(u'注册时间',auto_now_add=True)
	def __str__(self):
		 return self.name
	

class Ship(models.Model):
	vessel_name = models.CharField(u'船名',max_length=20)
	dwt = models.DecimalField(u'载重吨',max_digits=10,decimal_places =2)
	built = models.DateField(u'建造日期')
	type = models.CharField(u'船型',max_length=2,choices=SHIP_TYPE_CHOICES)
	flag = models.CharField(u'船旗',max_length=20,blank=True)
	loa = models.DecimalField(u'船长(米)',max_digits=6,decimal_places =2)
	beam = models.DecimalField(u'船宽(米)',max_digits=5,decimal_places =2)
	depth = models.DecimalField(u'船深(米)',max_digits=5,decimal_places =2)
	draft = models.DecimalField(u'吃水(米)',max_digits=5,decimal_places =2)
	grain = models.DecimalField(u'舱容(立方米)',max_digits=10,decimal_places =2)
	hatch = models.IntegerField(u'舱数')
	tpc = models.DecimalField(u'每厘米吃水',max_digits=5,decimal_places =2,blank=True, null=True)
	imo = models.CharField(u'IMO No.',max_length=20,blank=True)
	call_sign = models.CharField(u'呼号',max_length=20,blank=True)
	pi_club = models.CharField(u'船东保赔协会',max_length=10,blank=True)	
	ship_class = models.CharField(u'船级',max_length=10,blank=True)
	gear = models.CharField(u'船吊',max_length=20,blank=True)
	memo = models.TextField(u'备注',max_length=256,blank=True)
	order = models.PositiveIntegerField()
	def __str__(self):
		return self.vessel_name


class Tonnage(models.Model):
	ship = models.ForeignKey(Ship, verbose_name=u'船舶', on_delete=models.CASCADE)
	sender = models.ForeignKey(Sender,verbose_name=u'发件人', on_delete=models.CASCADE)
	recorder = models.ForeignKey(User, verbose_name=u'记录人',on_delete=models.CASCADE)
	open_start_date = models.DateField(u'空船开始日期')
	open_end_date = models.DateField(u'空船结束日期')
	open_area = models.CharField(u'空船区域',max_length=50)
	memo = models.TextField(u'备注',max_length=256,blank=True)
	send_time = models.DateTimeField(u'发送时间')
	record_time = models.DateTimeField(u'录入时间',auto_now_add=True)
	def __str__(self):
		return self.open_area


class Cargo(models.Model):
	loading_port= models.ForeignKey(Port, verbose_name=u'装货港',on_delete=models.CASCADE, related_name='loading')
	discharge_port= models.ForeignKey(Port,verbose_name= u'卸货港',on_delete=models.CASCADE,related_name='discharge')
	sender = models.ForeignKey(Sender, verbose_name=u'发件人',on_delete=models.CASCADE)
	recorder = models.ForeignKey(User,verbose_name= u'记录人',on_delete=models.CASCADE)
	cargo_name = models.CharField(u'货物名称',max_length=100)
	cargo_type = models.CharField(u'货物类型',max_length=20)
	quantity = models.DecimalField(u'货量',max_digits=10,decimal_places =2)
	quantity_unit = models.CharField(u'货量单位',max_length=1,choices=QUANTITY_UNIT_CHOICES)
	laycan_start = models.DateField(u'受载期开始')
	laycan_end = models.DateField(u'受载期结束')
	package = models.CharField(u'包装类型',max_length=2,blank=True)
	sf = models.DecimalField(u'积载因素',max_digits=4,decimal_places =2,blank=True, null=True)
	ldRate = models.DecimalField(u'装卸率',max_digits=4,decimal_places =2,blank=True, null=True)
	frt = models.DecimalField(u'运费',max_digits=10,decimal_places =2,blank=True, null=True)
	currency_unit = models.CharField(u'货币单位',max_length=1,choices=CURRENCY_UNIT_CHOICES)
	crane = models.CharField(u'吊具',max_length=100,blank=True)
	comm = models.DecimalField(u'佣金(%)',max_digits=4,decimal_places =2,blank=True, null=True)
	term = models.CharField(u'条款',max_length=5,blank=True,choices=TERM_TYPE_CHOICES)
	memo = models.TextField(u'备注',max_length=256,blank=True)
	send_time = models.DateTimeField(u'发送时间')
	record_time = models.DateTimeField(u'录入时间',auto_now_add=True)
	def __str__(self):
		return self.cargo_name


class Tct(models.Model):
	sender = models.ForeignKey(Sender, verbose_name=u'发件人',on_delete=models.CASCADE)
	recorder = models.ForeignKey(User, verbose_name=u'记录人',on_delete=models.CASCADE)
	account = models.CharField(u'租家',max_length=50,blank=True)
	dwt = models.DecimalField(u'载重吨',max_digits=10,decimal_places =2)
	delivery = models.CharField(u'交付地点',max_length=50)
	redelivery = models.CharField(u'交还地点',max_length=50)
	laycan_start = models.DateField(u'受载期开始')
	laycan_end = models.DateField(u'受载期结束')
	duration = models.CharField(u'租期',max_length=20)
	type = models.CharField(u'船型',max_length=2,choices=SHIP_TYPE_CHOICES)
	max_age= models.IntegerField(u'船龄限制(年)',blank=True, null=True)
	crane = models.CharField(u'装卸能力',max_length=50,blank=True)
	grain = models.DecimalField(u'舱容(立方米)',max_digits=10,decimal_places =2,blank=True, null=True)
	hatch = models.IntegerField(u'舱数',blank=True, null=True)
	memo = models.TextField(u'备注',max_length=256,blank=True)
	sendTime = models.DateTimeField(u'发送时间')
	recordTime = models.DateTimeField(u'录入时间',auto_now_add=True)
	def __str__(self):
		return self.account






class Agent(models.Model):
	email = models.EmailField(u'邮箱',max_length=100)
	name = models.CharField(u'联系人',max_length=20)
	telephone = models.CharField(u'办公电话',max_length=15)
	mobile = models.CharField(u'手机',max_length=11,blank=True)
	fax = models.CharField(u'传真',max_length=15,blank=True)
	skype = models.CharField(u'skype',max_length=15,blank=True)
	QQ = models.CharField(u'QQ',max_length=10,blank=True)
	company_name = models.CharField(u'公司名称',max_length=80)
	company_abbr = models.CharField(u'公司简称',max_length=20)
	company_address = models.CharField(u'公司地址',max_length=100,blank=True)
	web_site = models.CharField(u'公司网址',max_length=50,blank=True)
	company_about = models.TextField(u'公司简介',max_length=256,blank=True)
	port_code = models.CharField(u'港口代码',max_length=200)
	port_cname = models.CharField(u'港口名称',max_length=200)
	country = models.CharField(u'国家',max_length=30)
	def __str__(self):
		return self.name


class Star(models.Model):
	user_name = models.CharField(u'用户名',max_length=100)
	record_id = models.IntegerField(u'记录编号')
	flag_Time = models.DateTimeField(u'标记时间',auto_now_add=True)
	memo = models.TextField(u'备注',max_length=256,blank=True)
	class Meta:
		abstract = True
		unique_together = (("user_name", "record_id"),)



class StarTonnage(Star):
	star_table=models.CharField(u'星标记录类型',max_length=10,default="Tonnage",editable=False)
	
	
class StarCargo(Star):
	star_table=models.CharField(u'星标记录类型',max_length=10,default="Cargo",editable=False)
	
		
class StarTct(Star):
	star_table=models.CharField(u'星标记录类型',max_length=10,default="Tct",editable=False)
	
	

SELECTED_STATUS_CHOICES = ( )

class Selected(models.Model):
	user_name = models.CharField(u'用户名',max_length=100)
	record_id = models.IntegerField(u'记录编号')
	selected_Time = models.DateTimeField(u'筛选时间',auto_now_add=True)
	status = models.CharField(u'记录状态',max_length=1,choices=SELECTED_STATUS_CHOICES)
	memo = models.TextField(max_length=256,blank=True)
	class Meta:
		abstract = True
		unique_together = (("user_name", "record_id"),)



class SelectedTonnage(Selected):
	selected_table=models.CharField(u'筛选记录类型',max_length=10,default="Tonnage",editable=False)



class SelectedCargo(Selected):
	selected_table=models.CharField(u'筛选记录类型',max_length=10,default="Cargo",editable=False)


class SelectedTct(Selected):
	selected_table=models.CharField(u'筛选记录类型',max_length=10,default="Tct",editable=False)

