# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import django.utils.timezone as timezone
from django.db import models



# Create your models here.

HTTP_CHOICE = (
    ('HTTP', 'HTTP'),
    ('HTTPS', 'HTTPS')
)

REQUEST_TYPE_CHOICE = (
    ('POST', 'POST'),
    ('GET', 'GET'),
    ('PUT', 'PUT'),
    ('DELETE', 'DELETE')
)


REQUEST_PARAMETER_TYPE_CHOICE = (
    ('form-data', '表单(form-data)'),
    ('raw', '源数据(raw)')
)

RESULT_CHOICE = (
    ('PASS', '成功'),
    ('FAIL', '失败'),
    ('ERROR', '异常'),
)

HTTP_CODE_CHOICE = (
    ('200', '200'),
    ('404', '404'),
    ('400', '400'),
    ('502', '502'),
    ('500', '500'),
    ('302', '302'),
)

PARAMTYPE=(
    ('int', 'int'),
    ('string', 'string'),
)

TASK_CHOICE = (
    ('circulation', '循环'),
    ('timing', '定时'),
)

#项目表
class Project(models.Model):
    ProjectType = (
        ('Web', 'Web'),
        ('App', 'App')
    )
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name='项目名称')
    version = models.CharField(max_length=50, verbose_name='版本')
    type = models.CharField(max_length=50, verbose_name='类型', choices=ProjectType)
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name='描述')
    status = models.BooleanField(default=True, verbose_name='状态0:删除，1：未删除')
    LastUpdateTime = models.DateTimeField(auto_now=True, verbose_name='最近修改时间')
    createTime = models.DateTimeField(auto_now=True, verbose_name='创建时间')
    user = models.CharField(max_length=32)

#环境表
class Env(models.Model):
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    env_name = models.CharField(max_length=32)
    env_url= models.CharField(max_length=100, verbose_name='访问地址')
    evn_port=models.CharField(max_length=10, verbose_name='端口')
    env_desc = models.CharField(max_length=1000, default='')
    env_createTime = models.DateTimeField('创建时间', default=timezone.now)
    user =  models.CharField(max_length=32)


#用例管理
class Case(models.Model):
    """
    用例管理
    """
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='所属项目')
    name = models.CharField(max_length=50, verbose_name='用例名称')
    user = models.CharField(max_length=32, verbose_name='创建人')
    desc = models.CharField(max_length=1024, blank=True, null=True, verbose_name='描述')
    status = models.CharField(max_length=32, default='4', verbose_name='状态：1成功，2失败 3未完成 4未开始')
    CreateTime = models.DateTimeField(auto_now=True, verbose_name='创建时间')
    LastUpdateTime = models.DateTimeField(auto_now=True, verbose_name='最近修改时间')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '用例'
        verbose_name_plural = '用例管理'


#接口管理
class ApiCase(models.Model):
    """
    接口管理
    """
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='所属项目')
    name = models.CharField(max_length=50, verbose_name='接口名称')
    httpType = models.CharField(max_length=50, default='HTTP', verbose_name='http/https', choices=HTTP_CHOICE)
    method = models.CharField(max_length=50, verbose_name='请求方式', choices=REQUEST_TYPE_CHOICE)
    apiAddress = models.CharField(max_length=1024, verbose_name='接口地址')
    requestParameterType = models.CharField(default='1', max_length=50, verbose_name='请求参数格式', choices=REQUEST_PARAMETER_TYPE_CHOICE)
    status = models.CharField(max_length=32, default='', verbose_name='状态1成功，0失败')
    user = models.CharField(max_length=32, verbose_name='创建人')
    desc = models.CharField(max_length=1024, blank=True, null=True, verbose_name='描述')
    CreateTime = models.DateTimeField(auto_now=True, null=True, verbose_name='创建时间')
    LastUpdateTime = models.DateTimeField(auto_now=True, verbose_name='最近修改时间')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '接口'
        verbose_name_plural = '接口管理'

#请求头
class ApiHead(models.Model):
    id = models.AutoField(primary_key=True)
    api = models.ForeignKey(ApiCase, on_delete=models.CASCADE, verbose_name="所属接口")
    name = models.CharField(max_length=1024, verbose_name="标签")
    value = models.CharField(max_length=1024, blank=True, null=True, verbose_name='内容')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '请求头'
        verbose_name_plural = '请求头管理'

#请求数据源
class ApiParameterRaw(models.Model):
    id = models.AutoField(primary_key=True)
    api = models.OneToOneField(ApiCase, on_delete=models.CASCADE, verbose_name="所属接口")
    data = models.TextField(blank=True, null=True, verbose_name='内容')

    class Meta:
        verbose_name = '请求参数Raw'

#api参数
class APIParameter(models.Model):
    """
    请求的参数
    """
    id = models.AutoField(primary_key=True)
    api = models.ForeignKey(ApiCase, related_name='parameterList', on_delete=models.CASCADE, verbose_name='接口')
    requestParameterType = models.CharField(max_length=50, verbose_name='请求参数格式', choices=REQUEST_PARAMETER_TYPE_CHOICE)
    name = models.CharField(max_length=1024, verbose_name='参数名')
    value = models.CharField(max_length=1024, verbose_name='内容', blank=True, null=True)
    paramType = models.CharField(default='string', max_length=1024, verbose_name='类型',choices=PARAMTYPE)


    def __unicode__(self):
        return self.value

    class Meta:
        verbose_name = '接口参数'
        verbose_name_plural = '接口参数管理'


class task(models.Model):
    """
        执行任务
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name='任务名')
    desc = models.CharField(max_length=1024, verbose_name='任务描述')
    type = models.CharField(max_length=50, default='timing', verbose_name='类型', choices=TASK_CHOICE)
    time = models.CharField(max_length=1024, verbose_name='定时')
    status = models.IntegerField(default=0, verbose_name='1:执行中，2：结束，0：待执行,3:暂停')
    startTime = models.DateTimeField(auto_now=False, verbose_name='开始时间',null=True)
    endTime = models.DateTimeField(auto_now=False, verbose_name='结束时间',null=True)
    user = models.CharField(max_length=32, verbose_name='创建人', default= '')
    env_id = models.CharField(max_length=32, verbose_name='环境', default='')
    CreateTime = models.DateTimeField(auto_now=True, verbose_name='创建时间')
    min = models.CharField(max_length=32, default='*', verbose_name='分钟',null=True)
    hour = models.CharField(max_length=32, default='*', verbose_name='小时',null=True)
    day = models.CharField(max_length=32, default='*', verbose_name='天',null=True)
    month = models.CharField(max_length=32, default='*', verbose_name='月',null=True)
    week = models.CharField(max_length=32, default='*', verbose_name='周',null=True)



class taskCase(models.Model):
    """
    任务和表关联
    """
    id = models.AutoField(primary_key=True)
    task_id=models.IntegerField(default=0, verbose_name='任务')
    case_id=models.IntegerField(default=0, verbose_name='用例')




#用例接口管理
class AutoApiCase(models.Model):
    """
    用例接口管理
    """
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='所属项目')
    case = models.ForeignKey(Case, on_delete=models.CASCADE, verbose_name='所属用例')
    name = models.CharField(max_length=50, verbose_name='接口名称')
    httpType = models.CharField(max_length=50, default='HTTPS', verbose_name='http/https', choices=HTTP_CHOICE)
    method = models.CharField(max_length=50, verbose_name='请求方式', choices=REQUEST_TYPE_CHOICE)
    apiAddress = models.CharField(max_length=1024, verbose_name='接口地址')
    requestParameterType = models.CharField(max_length=50, verbose_name='请求参数格式', choices=REQUEST_PARAMETER_TYPE_CHOICE)
    status = models.CharField(max_length=32, default='', verbose_name='返回结果')
    sort = models.IntegerField(default=0,verbose_name='排序')
    user = models.CharField(max_length=32, verbose_name='创建人')
    desc = models.CharField(max_length=1024, blank=True, null=True, verbose_name='描述')
    CreateTime = models.DateTimeField(auto_now=True, verbose_name='创建时间')
    LastUpdateTime = models.DateTimeField(auto_now=True, verbose_name='最近修改时间')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '所属接口'
        verbose_name_plural = '所属接口管理'

#请求头
class autoApiHead(models.Model):
    id = models.AutoField(primary_key=True)
    autoApi = models.ForeignKey(AutoApiCase, on_delete=models.CASCADE, verbose_name="所属接口")
    name = models.CharField(max_length=1024, verbose_name="标签")
    value = models.CharField(max_length=1024, blank=True, null=True, verbose_name='内容')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '用例请求头'
        verbose_name_plural = '用例请求头管理'

#请求数据源
class autoApiParameterRaw(models.Model):
    id = models.AutoField(primary_key=True)
    autoApi = models.ForeignKey(AutoApiCase, on_delete=models.CASCADE, verbose_name="所属接口")
    data = models.TextField(blank=True, null=True, verbose_name='内容')

    class Meta:
        verbose_name = '请求参数Raw'

#用例参数
class autoAPIParameter(models.Model):
    """
    请求的参数
    """
    id = models.AutoField(primary_key=True)
    autoApi = models.ForeignKey(AutoApiCase, related_name='parameterList', on_delete=models.CASCADE, verbose_name='接口')
    requestParameterType = models.CharField(max_length=50, verbose_name='请求参数格式', choices=REQUEST_PARAMETER_TYPE_CHOICE)
    name = models.CharField(max_length=1024, verbose_name='参数名')
    value = models.CharField(max_length=1024, verbose_name='内容', blank=True, null=True)
    paramType = models.CharField(default='string', max_length=1024, verbose_name='类型',choices=PARAMTYPE)


    def __unicode__(self):
        return self.value

    class Meta:
        verbose_name = '用例接口参数'
        verbose_name_plural = '用例接口参数管理'

class step(models.Model):
    """
    步骤管理
    """
    id = models.AutoField(primary_key=True)
    autoCase_id = models.IntegerField(null=True, verbose_name='所属项目')
    name = models.CharField(max_length=50, verbose_name='步骤名称')
    type = models.CharField(max_length=20, verbose_name='步骤类型')
    sort = models.PositiveIntegerField(default=0, verbose_name='步骤排序')
    content = models.CharField(max_length=200, verbose_name='步骤类型')


class TestResult(models.Model):
    """
    执行结果
    """
    id = models.AutoField(primary_key=True)
    autoApi = models.ForeignKey(AutoApiCase, on_delete=models.CASCADE, verbose_name='接口')
    statusCode = models.CharField(blank=True, null=True, max_length=1024, verbose_name='期望HTTP状态', choices=HTTP_CODE_CHOICE)
    examineType = models.CharField(max_length=1024, verbose_name='匹配规则')
    data = models.TextField(blank=True, null=True, verbose_name='规则内容')
    result = models.CharField(max_length=50, verbose_name='测试结果', choices=RESULT_CHOICE)
    httpStatus = models.CharField(max_length=50, blank=True, null=True, verbose_name='http状态', choices=HTTP_CODE_CHOICE)
    responseData = models.TextField(blank=True, null=True, verbose_name='实际返回内容')
    user = models.CharField(max_length=32, verbose_name='创建人')

    def __unicode__(self):
        return self.httpStatus

    class Meta:
        verbose_name = '测试结果'
        verbose_name_plural = '测试结果管理'

class taskResult(models.Model):
    """
    任务执行结果
    """
    id = models.AutoField(primary_key=True)
    task = models.ForeignKey(task, on_delete=models.CASCADE, verbose_name='任务关联')
    autoRunTime_id = models.IntegerField(null=True, verbose_name='时间关联')
    case_id=models.IntegerField(default=0, verbose_name='用例')
    autoApi_id=models.IntegerField(default=0, verbose_name='用例')
    result = models.CharField(max_length=50, verbose_name='测试结果', choices=RESULT_CHOICE)
    httpStatus = models.CharField(max_length=50, blank=True, null=True, verbose_name='http状态', choices=HTTP_CODE_CHOICE)
    responseData = models.TextField(blank=True, null=True, verbose_name='实际返回内容')
    user = models.CharField(max_length=32, verbose_name='创建人')
    testTime = models.CharField(max_length=50, verbose_name='测试时间',default='')


    def __unicode__(self):
        return self.httpStatus

    class Meta:
        verbose_name = '测试结果'
        verbose_name_plural = '测试结果管理'

class AutoTaskRunTime(models.Model):
    """
    用例执行开始和结束时间
    """
    id = models.AutoField(primary_key=True)
    task = models.ForeignKey(task, on_delete=models.CASCADE, verbose_name='任务', default='')
    startTime = models.DateTimeField(verbose_name='开始时间', null=True)
    endTime = models.DateTimeField(verbose_name='结束时间', null=True)
    testTime = models.DateTimeField(verbose_name='测试时间',null=True)

    class Meta:
        verbose_name = '用例任务执行时间'
        verbose_name_plural = '用例任务执行时间'

class globalVariable(models.Model):
    """
    全局变量
    """
    id = models.AutoField(primary_key=True)
    autoApi_id=models.IntegerField(null=True, verbose_name='用例')
    name = models.CharField(max_length=50, verbose_name='变量名')
    path = models.CharField(max_length=200, verbose_name='返回参数路径', null=True)
    value = models.CharField(max_length=50, verbose_name='变量值', null=True)
    user = models.CharField(max_length=50, verbose_name='创建人')


class sqlManager(models.Model):
    """
    数据库管理
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name='数据库取名')
    sqltype=models.IntegerField(null=True, verbose_name='数据库类型1：mysql，2：redis，3：mango')
    host=models.CharField(null=True, verbose_name='数据库地址', max_length=50)
    username=models.CharField(null=True, verbose_name='登录名', max_length=50)
    password=models.CharField(null=True, verbose_name='密码', max_length=50)
    db=models.CharField(null=True, verbose_name='数据库名', max_length=50)
    port=models.CharField(null=True, verbose_name='端口', max_length=10)
    user = models.CharField(null=True, verbose_name='创建人', max_length=50)
    desc = models.CharField(null=True, verbose_name='描述', max_length=200)
    CreateTime = models.DateTimeField(auto_now=True, verbose_name='创建时间')

class sql_api(models.Model):
    """
    数据库和api关联
    """
    id = models.AutoField(primary_key=True)
    sql_id= models.IntegerField(null=True, verbose_name='数据库环境')
    autoApi_id=models.IntegerField(null=True, verbose_name='接口')





