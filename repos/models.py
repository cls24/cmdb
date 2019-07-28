from django.db import models
from django.db.models import Model


# Create your models here.


class Department(Model):
    name = models.CharField(max_length=64)

    class Meta:
        verbose_name_plural = '部门表'


class User(Model):
    name = models.CharField(max_length=32)
    email = models.EmailField()
    mobile_phone = models.CharField(max_length=32)
    department = models.ForeignKey('Department', on_delete=models.CASCADE, verbose_name='所属部门')

    class Meta:
        verbose_name_plural = '用户表'


class UserGroup(Model):
    name = models.CharField(max_length=32)
    class Meta:
        verbose_name_plural = '员工组表'

class AdminGroup(Model):
    name = models.CharField(max_length=32)
    class Meta:
        verbose_name_plural = '管理员组表'

class UG(Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    businessgroup = models.ForeignKey('UserGroup', on_delete=models.CASCADE)

class AG(Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    admingroup = models.ForeignKey('AdminGroup', on_delete=models.CASCADE)


class BusinessUnit(Model):
    name = models.CharField('业务线名', max_length=32)
    businessgroup = models.ForeignKey('UserGroup', on_delete=models.CASCADE, verbose_name='业务负责人')
    admingroup = models.ForeignKey('AdminGroup', on_delete=models.CASCADE, verbose_name='管理员')

    class Meta:
        verbose_name_plural = '业务线表'


class Tag(Model):
    name = models.CharField(max_length=32)

    class Meta:
        verbose_name_plural = '资产标签表'


class AssetTag(Model):
    t = models.ForeignKey('Tag', on_delete=models.CASCADE)
    a = models.ForeignKey('Asset', on_delete=models.CASCADE)


class Asset(Model):
    device_type_choices = (
        (1, '服务器'),
        (2, '交换机'),
        (3, '防火墙'),
        (4, '防火墙'),
    )
    device_status_choices = (
        (1, '在线'),
        (2, '离线'),
        (3, '上架'),
        (4, '下架'),
    )
    device_type_id = models.IntegerField(choices=device_type_choices, default=1)
    device_status_id = models.IntegerField(choices=device_status_choices, default=1)

    Cabinet_num = models.CharField('机架号', max_length=30, null=True)
    Cabinet_order = models.CharField('机架中序号', max_length=30, null=True)

    idc = models.ForeignKey('IDC', null=True, on_delete=models.CASCADE, verbose_name='IDC机房')
    business_unit = models.ForeignKey('BusinessUnit', null=True, on_delete=models.CASCADE, verbose_name='业务线')
    department = models.ForeignKey('Department', on_delete=models.CASCADE, verbose_name='部门')
    latest_date = models.DateField(null=True)
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = '资产表'


class IDC(Model):
    name = models.CharField(max_length=32)
    city = models.CharField(max_length=32)

    class Meta:
        verbose_name_plural = 'IDC表'


class NetworkDevice(Model):
    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)
    name = models.CharField('设备名称', max_length=128)
    sn = models.CharField('sn号', max_length=64, db_index=True)
    vendor = models.CharField('制造商', max_length=32, null=True, blank=True)
    model = models.CharField('型号', max_length=64)
    manage_ip = models.GenericIPAddressField('管理ip', null=True, blank=True)
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = '网络设备表'


class Server(Model):
    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)
    hostname = models.CharField('主机名', max_length=128, unique=True)
    sn = models.CharField('sn号', max_length=64, db_index=True)
    vendor = models.CharField('制造商', max_length=32, null=True, blank=True)
    model = models.CharField('型号', max_length=64,null=True, blank=True)
    manage_ip = models.GenericIPAddressField('管理ip', null=True, blank=True)
    os_platform = models.CharField('系统平台', max_length=16, null=True, blank=True)
    os_version = models.CharField('系统版本', max_length=16, null=True, blank=True)
    cpu_model = models.CharField('型号', max_length=64)
    cpu_cores = models.IntegerField('核数')
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = '服务器表'


class Disk(Model):
    slot = models.CharField('槽位', max_length=32)
    model = models.CharField('型号', max_length=64)
    capacity = models.FloatField('容量')
    type = models.CharField('磁盘类型', max_length=32)
    server = models.ForeignKey('Server', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = '硬盘表'

class Nic(Model):
    name = models.CharField('网卡名称', max_length=128)
    hwaddr = models.CharField('网卡mac', max_length=64)
    ipv4 = models.CharField('ipv4地址', max_length=128)
    up = models.BooleanField(default=True)
    server = models.ForeignKey('Server', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = '网卡表'


class Memory(Model):
    slot = models.CharField('槽位', max_length=32)
    # model = models.CharField('型号', max_length=64)
    vendor = models.CharField('制造商', max_length=32, null=True, blank=True)
    capacity = models.FloatField('容量')
    sn = models.CharField('内存sn号',max_length=64)
    server = models.ForeignKey('Server', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = '内存表'


class AssetLog(Model):
    log_type_choices = (
        (1, 'ERROR'),
        (2, 'WARN'),
        (3, 'INFO'),
    )
    title = models.CharField(max_length=16)
    content = models.TextField()
    add_time = models.DateTimeField(auto_now_add=True),
    asset = models.ForeignKey('Asset', on_delete=models.CASCADE)
    type = models.IntegerField(choices=log_type_choices)
    user = models.ForeignKey('User', on_delete=models.CASCADE, null=True)


class AssetRecord(Model):
    content = models.TextField()
    add_time = models.DateTimeField(auto_now_add=True)
    asset = models.ForeignKey('Asset', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE, null=True)
