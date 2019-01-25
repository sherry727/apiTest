# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class ZtAction(models.Model):
    objecttype = models.CharField(db_column='objectType', max_length=30)  # Field name made lowercase.
    objectid = models.IntegerField(db_column='objectID')  # Field name made lowercase.
    product = models.CharField(max_length=255)
    project = models.IntegerField()
    actor = models.CharField(max_length=30)
    action = models.CharField(max_length=30)
    date = models.DateTimeField()
    comment = models.TextField()
    extra = models.CharField(max_length=255)
    read = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'zt_action'


class ZtBug(models.Model):
    product = models.IntegerField()
    module = models.IntegerField()
    project = models.IntegerField()
    plan = models.IntegerField()
    story = models.IntegerField()
    storyversion = models.SmallIntegerField(db_column='storyVersion')  # Field name made lowercase.
    task = models.IntegerField()
    totask = models.IntegerField(db_column='toTask')  # Field name made lowercase.
    tostory = models.IntegerField(db_column='toStory')  # Field name made lowercase.
    title = models.CharField(max_length=255)
    keywords = models.CharField(max_length=255)
    severity = models.IntegerField()
    pri = models.IntegerField()
    type = models.CharField(max_length=30)
    os = models.CharField(max_length=30)
    browser = models.CharField(max_length=30)
    hardware = models.CharField(max_length=30)
    found = models.CharField(max_length=30)
    steps = models.TextField()
    status = models.CharField(max_length=8)
    confirmed = models.IntegerField()
    activatedcount = models.SmallIntegerField(db_column='activatedCount')  # Field name made lowercase.
    mailto = models.CharField(max_length=255)
    openedby = models.CharField(db_column='openedBy', max_length=30)  # Field name made lowercase.
    openeddate = models.DateTimeField(db_column='openedDate')  # Field name made lowercase.
    openedbuild = models.CharField(db_column='openedBuild', max_length=255)  # Field name made lowercase.
    assignedto = models.CharField(db_column='assignedTo', max_length=30)  # Field name made lowercase.
    assigneddate = models.DateTimeField(db_column='assignedDate')  # Field name made lowercase.
    resolvedby = models.CharField(db_column='resolvedBy', max_length=30)  # Field name made lowercase.
    resolution = models.CharField(max_length=30)
    resolvedbuild = models.CharField(db_column='resolvedBuild', max_length=30)  # Field name made lowercase.
    resolveddate = models.DateTimeField(db_column='resolvedDate')  # Field name made lowercase.
    closedby = models.CharField(db_column='closedBy', max_length=30)  # Field name made lowercase.
    closeddate = models.DateTimeField(db_column='closedDate')  # Field name made lowercase.
    duplicatebug = models.IntegerField(db_column='duplicateBug')  # Field name made lowercase.
    linkbug = models.CharField(db_column='linkBug', max_length=255)  # Field name made lowercase.
    case = models.IntegerField()
    caseversion = models.SmallIntegerField(db_column='caseVersion')  # Field name made lowercase.
    result = models.IntegerField()
    testtask = models.IntegerField()
    lasteditedby = models.CharField(db_column='lastEditedBy', max_length=30)  # Field name made lowercase.
    lastediteddate = models.DateTimeField(db_column='lastEditedDate')  # Field name made lowercase.
    deleted = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'zt_bug'


class ZtBuild(models.Model):
    product = models.IntegerField()
    project = models.IntegerField()
    name = models.CharField(max_length=150)
    scmpath = models.CharField(db_column='scmPath', max_length=255)  # Field name made lowercase.
    filepath = models.CharField(db_column='filePath', max_length=255)  # Field name made lowercase.
    date = models.DateField()
    stories = models.TextField()
    bugs = models.TextField()
    builder = models.CharField(max_length=30)
    desc = models.TextField()
    deleted = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'zt_build'


class ZtBurn(models.Model):
    project = models.IntegerField(primary_key=True)
    date = models.DateField()
    left = models.FloatField()
    consumed = models.FloatField()

    class Meta:
        managed = False
        db_table = 'zt_burn'
        unique_together = (('project', 'date'),)


class ZtCase(models.Model):
    product = models.IntegerField()
    module = models.IntegerField()
    path = models.IntegerField()
    story = models.IntegerField()
    storyversion = models.SmallIntegerField(db_column='storyVersion')  # Field name made lowercase.
    title = models.CharField(max_length=255)
    precondition = models.TextField()
    keywords = models.CharField(max_length=255)
    pri = models.IntegerField()
    type = models.CharField(max_length=30)
    stage = models.CharField(max_length=255)
    howrun = models.CharField(db_column='howRun', max_length=30)  # Field name made lowercase.
    scriptedby = models.CharField(db_column='scriptedBy', max_length=30)  # Field name made lowercase.
    scripteddate = models.DateField(db_column='scriptedDate')  # Field name made lowercase.
    scriptstatus = models.CharField(db_column='scriptStatus', max_length=30)  # Field name made lowercase.
    scriptlocation = models.CharField(db_column='scriptLocation', max_length=255)  # Field name made lowercase.
    status = models.CharField(max_length=30)
    frequency = models.CharField(max_length=1)
    order = models.IntegerField()
    openedby = models.CharField(db_column='openedBy', max_length=30)  # Field name made lowercase.
    openeddate = models.DateTimeField(db_column='openedDate')  # Field name made lowercase.
    lasteditedby = models.CharField(db_column='lastEditedBy', max_length=30)  # Field name made lowercase.
    lastediteddate = models.DateTimeField(db_column='lastEditedDate')  # Field name made lowercase.
    version = models.IntegerField()
    linkcase = models.CharField(db_column='linkCase', max_length=255)  # Field name made lowercase.
    frombug = models.IntegerField(db_column='fromBug')  # Field name made lowercase.
    deleted = models.CharField(max_length=1)
    lastrunner = models.CharField(db_column='lastRunner', max_length=30)  # Field name made lowercase.
    lastrundate = models.DateTimeField(db_column='lastRunDate')  # Field name made lowercase.
    lastrunresult = models.CharField(db_column='lastRunResult', max_length=30)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'zt_case'


class ZtCasestep(models.Model):
    case = models.IntegerField()
    version = models.SmallIntegerField()
    desc = models.TextField()
    expect = models.TextField()

    class Meta:
        managed = False
        db_table = 'zt_casestep'


class ZtCompany(models.Model):
    name = models.CharField(max_length=120, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    fax = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=120, blank=True, null=True)
    zipcode = models.CharField(max_length=10, blank=True, null=True)
    website = models.CharField(max_length=120, blank=True, null=True)
    backyard = models.CharField(max_length=120, blank=True, null=True)
    guest = models.CharField(max_length=1)
    admins = models.CharField(max_length=255, blank=True, null=True)
    deleted = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'zt_company'


class ZtConfig(models.Model):
    owner = models.CharField(max_length=30)
    module = models.CharField(max_length=30)
    section = models.CharField(max_length=30)
    key = models.CharField(max_length=30)
    value = models.TextField()

    class Meta:
        managed = False
        db_table = 'zt_config'
        unique_together = (('owner', 'module', 'section', 'key'),)


class ZtDept(models.Model):
    name = models.CharField(max_length=60)
    parent = models.IntegerField()
    path = models.CharField(max_length=255)
    grade = models.IntegerField()
    order = models.IntegerField()
    position = models.CharField(max_length=30)
    function = models.CharField(max_length=255)
    manager = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'zt_dept'


class ZtDoc(models.Model):
    product = models.IntegerField()
    project = models.IntegerField()
    lib = models.CharField(max_length=30)
    module = models.CharField(max_length=30)
    title = models.CharField(max_length=255)
    digest = models.CharField(max_length=255)
    keywords = models.CharField(max_length=255)
    type = models.CharField(max_length=30)
    content = models.TextField()
    url = models.CharField(max_length=255)
    views = models.SmallIntegerField()
    addedby = models.CharField(db_column='addedBy', max_length=30)  # Field name made lowercase.
    addeddate = models.DateTimeField(db_column='addedDate')  # Field name made lowercase.
    editedby = models.CharField(db_column='editedBy', max_length=30)  # Field name made lowercase.
    editeddate = models.DateTimeField(db_column='editedDate')  # Field name made lowercase.
    deleted = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'zt_doc'


class ZtDoclib(models.Model):
    id = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=60)
    deleted = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'zt_doclib'


class ZtEffort(models.Model):
    user = models.CharField(max_length=30)
    todo = models.CharField(max_length=1)
    date = models.DateField()
    begin = models.DateTimeField()
    end = models.DateTimeField()
    type = models.CharField(max_length=1)
    idvalue = models.IntegerField()
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=255)
    status = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'zt_effort'


class ZtExtension(models.Model):
    name = models.CharField(max_length=150)
    code = models.CharField(unique=True, max_length=30)
    version = models.CharField(max_length=50)
    author = models.CharField(max_length=100)
    desc = models.TextField()
    license = models.TextField()
    type = models.CharField(max_length=20)
    site = models.CharField(max_length=150)
    zentaocompatible = models.CharField(db_column='zentaoCompatible', max_length=100)  # Field name made lowercase.
    installedtime = models.DateTimeField(db_column='installedTime')  # Field name made lowercase.
    depends = models.CharField(max_length=100)
    dirs = models.TextField()
    files = models.TextField()
    status = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'zt_extension'


class ZtFile(models.Model):
    pathname = models.CharField(max_length=50)
    title = models.CharField(max_length=90)
    extension = models.CharField(max_length=30)
    size = models.IntegerField()
    objecttype = models.CharField(db_column='objectType', max_length=30)  # Field name made lowercase.
    objectid = models.IntegerField(db_column='objectID')  # Field name made lowercase.
    addedby = models.CharField(db_column='addedBy', max_length=30)  # Field name made lowercase.
    addeddate = models.DateTimeField(db_column='addedDate')  # Field name made lowercase.
    downloads = models.IntegerField()
    extra = models.CharField(max_length=255)
    deleted = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'zt_file'


class ZtGroup(models.Model):
    name = models.CharField(max_length=30)
    role = models.CharField(max_length=30)
    desc = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'zt_group'


class ZtGrouppriv(models.Model):
    group = models.IntegerField()
    module = models.CharField(max_length=30)
    method = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'zt_grouppriv'
        unique_together = (('group', 'module', 'method'),)


class ZtHistory(models.Model):
    action = models.IntegerField()
    field = models.CharField(max_length=30)
    old = models.TextField()
    new = models.TextField()
    diff = models.TextField()

    class Meta:
        managed = False
        db_table = 'zt_history'


class ZtLang(models.Model):
    lang = models.CharField(max_length=30)
    module = models.CharField(max_length=30)
    section = models.CharField(max_length=30)
    key = models.CharField(max_length=60)
    value = models.TextField()
    system = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'zt_lang'
        unique_together = (('lang', 'module', 'section', 'key'),)


class ZtModule(models.Model):
    root = models.IntegerField()
    name = models.CharField(max_length=60)
    parent = models.IntegerField()
    path = models.CharField(max_length=255)
    grade = models.IntegerField()
    order = models.SmallIntegerField()
    type = models.CharField(max_length=30)
    owner = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'zt_module'


class ZtProduct(models.Model):
    name = models.CharField(max_length=90)
    code = models.CharField(max_length=45)
    status = models.CharField(max_length=30)
    desc = models.TextField()
    po = models.CharField(db_column='PO', max_length=30)  # Field name made lowercase.
    qd = models.CharField(db_column='QD', max_length=30)  # Field name made lowercase.
    rd = models.CharField(db_column='RD', max_length=30)  # Field name made lowercase.
    acl = models.CharField(max_length=7)
    whitelist = models.CharField(max_length=255)
    createdby = models.CharField(db_column='createdBy', max_length=30)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='createdDate')  # Field name made lowercase.
    createdversion = models.CharField(db_column='createdVersion', max_length=20)  # Field name made lowercase.
    deleted = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'zt_product'


class ZtProductplan(models.Model):
    product = models.IntegerField()
    title = models.CharField(max_length=90)
    desc = models.TextField()
    begin = models.DateField()
    end = models.DateField()
    deleted = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'zt_productplan'


class ZtProject(models.Model):
    iscat = models.CharField(db_column='isCat', max_length=1)  # Field name made lowercase.
    catid = models.IntegerField(db_column='catID')  # Field name made lowercase.
    type = models.CharField(max_length=20)
    parent = models.IntegerField()
    name = models.CharField(max_length=90)
    code = models.CharField(max_length=45)
    begin = models.DateField()
    end = models.DateField()
    days = models.SmallIntegerField()
    status = models.CharField(max_length=10)
    statge = models.CharField(max_length=1)
    pri = models.CharField(max_length=1)
    desc = models.TextField()
    openedby = models.CharField(db_column='openedBy', max_length=30)  # Field name made lowercase.
    openeddate = models.IntegerField(db_column='openedDate')  # Field name made lowercase.
    openedversion = models.CharField(db_column='openedVersion', max_length=20)  # Field name made lowercase.
    closedby = models.CharField(db_column='closedBy', max_length=30)  # Field name made lowercase.
    closeddate = models.IntegerField(db_column='closedDate')  # Field name made lowercase.
    canceledby = models.CharField(db_column='canceledBy', max_length=30)  # Field name made lowercase.
    canceleddate = models.IntegerField(db_column='canceledDate')  # Field name made lowercase.
    po = models.CharField(db_column='PO', max_length=30)  # Field name made lowercase.
    pm = models.CharField(db_column='PM', max_length=30)  # Field name made lowercase.
    qd = models.CharField(db_column='QD', max_length=30)  # Field name made lowercase.
    rd = models.CharField(db_column='RD', max_length=30)  # Field name made lowercase.
    team = models.CharField(max_length=30)
    acl = models.CharField(max_length=7)
    whitelist = models.CharField(max_length=255)
    deleted = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'zt_project'


class ZtProjectproduct(models.Model):
    project = models.IntegerField(primary_key=True)
    product = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'zt_projectproduct'
        unique_together = (('project', 'product'),)


class ZtProjectstory(models.Model):
    project = models.IntegerField()
    product = models.IntegerField()
    story = models.IntegerField()
    version = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'zt_projectstory'
        unique_together = (('project', 'story'),)


class ZtRelease(models.Model):
    product = models.IntegerField()
    build = models.IntegerField()
    name = models.CharField(unique=True, max_length=30)
    date = models.DateField()
    stories = models.TextField()
    bugs = models.TextField()
    desc = models.TextField()
    deleted = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'zt_release'


class ZtStory(models.Model):
    product = models.IntegerField()
    module = models.IntegerField()
    plan = models.IntegerField()
    source = models.CharField(max_length=20)
    frombug = models.IntegerField(db_column='fromBug')  # Field name made lowercase.
    title = models.CharField(max_length=255)
    keywords = models.CharField(max_length=255)
    type = models.CharField(max_length=30)
    pri = models.IntegerField()
    estimate = models.FloatField()
    status = models.CharField(max_length=7)
    stage = models.CharField(max_length=10)
    mailto = models.CharField(max_length=255)
    openedby = models.CharField(db_column='openedBy', max_length=30)  # Field name made lowercase.
    openeddate = models.DateTimeField(db_column='openedDate')  # Field name made lowercase.
    assignedto = models.CharField(db_column='assignedTo', max_length=30)  # Field name made lowercase.
    assigneddate = models.DateTimeField(db_column='assignedDate')  # Field name made lowercase.
    lasteditedby = models.CharField(db_column='lastEditedBy', max_length=30)  # Field name made lowercase.
    lastediteddate = models.DateTimeField(db_column='lastEditedDate')  # Field name made lowercase.
    reviewedby = models.CharField(db_column='reviewedBy', max_length=255)  # Field name made lowercase.
    revieweddate = models.DateField(db_column='reviewedDate')  # Field name made lowercase.
    closedby = models.CharField(db_column='closedBy', max_length=30)  # Field name made lowercase.
    closeddate = models.DateTimeField(db_column='closedDate')  # Field name made lowercase.
    closedreason = models.CharField(db_column='closedReason', max_length=30)  # Field name made lowercase.
    tobug = models.IntegerField(db_column='toBug')  # Field name made lowercase.
    childstories = models.CharField(db_column='childStories', max_length=255)  # Field name made lowercase.
    linkstories = models.CharField(db_column='linkStories', max_length=255)  # Field name made lowercase.
    duplicatestory = models.IntegerField(db_column='duplicateStory')  # Field name made lowercase.
    version = models.SmallIntegerField()
    deleted = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'zt_story'


class ZtStoryspec(models.Model):
    story = models.IntegerField()
    version = models.SmallIntegerField()
    title = models.CharField(max_length=90)
    spec = models.TextField()
    verify = models.TextField()

    class Meta:
        managed = False
        db_table = 'zt_storyspec'
        unique_together = (('story', 'version'),)


class ZtTask(models.Model):
    project = models.IntegerField()
    module = models.IntegerField()
    story = models.IntegerField()
    storyversion = models.SmallIntegerField(db_column='storyVersion')  # Field name made lowercase.
    frombug = models.IntegerField(db_column='fromBug')  # Field name made lowercase.
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=20)
    pri = models.IntegerField()
    estimate = models.FloatField()
    consumed = models.FloatField()
    left = models.FloatField()
    deadline = models.DateField()
    status = models.CharField(max_length=6)
    mailto = models.CharField(max_length=255)
    desc = models.TextField()
    openedby = models.CharField(db_column='openedBy', max_length=30)  # Field name made lowercase.
    openeddate = models.DateTimeField(db_column='openedDate')  # Field name made lowercase.
    assignedto = models.CharField(db_column='assignedTo', max_length=30)  # Field name made lowercase.
    assigneddate = models.DateTimeField(db_column='assignedDate')  # Field name made lowercase.
    eststarted = models.DateField(db_column='estStarted')  # Field name made lowercase.
    realstarted = models.DateField(db_column='realStarted')  # Field name made lowercase.
    finishedby = models.CharField(db_column='finishedBy', max_length=30)  # Field name made lowercase.
    finisheddate = models.DateTimeField(db_column='finishedDate')  # Field name made lowercase.
    canceledby = models.CharField(db_column='canceledBy', max_length=30)  # Field name made lowercase.
    canceleddate = models.DateTimeField(db_column='canceledDate')  # Field name made lowercase.
    closedby = models.CharField(db_column='closedBy', max_length=30)  # Field name made lowercase.
    closeddate = models.DateTimeField(db_column='closedDate')  # Field name made lowercase.
    closedreason = models.CharField(db_column='closedReason', max_length=30)  # Field name made lowercase.
    lasteditedby = models.CharField(db_column='lastEditedBy', max_length=30)  # Field name made lowercase.
    lastediteddate = models.DateTimeField(db_column='lastEditedDate')  # Field name made lowercase.
    deleted = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'zt_task'


class ZtTaskestimate(models.Model):
    task = models.IntegerField()
    date = models.DateField()
    left = models.FloatField()
    consumed = models.FloatField()
    account = models.CharField(max_length=30)
    work = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'zt_taskestimate'


class ZtTeam(models.Model):
    project = models.IntegerField(primary_key=True)
    account = models.CharField(max_length=30)
    role = models.CharField(max_length=30)
    join = models.DateField()
    days = models.SmallIntegerField()
    hours = models.FloatField()

    class Meta:
        managed = False
        db_table = 'zt_team'
        unique_together = (('project', 'account'),)


class ZtTestresult(models.Model):
    run = models.IntegerField()
    case = models.IntegerField()
    version = models.SmallIntegerField()
    caseresult = models.CharField(db_column='caseResult', max_length=30)  # Field name made lowercase.
    stepresults = models.TextField(db_column='stepResults')  # Field name made lowercase.
    lastrunner = models.CharField(db_column='lastRunner', max_length=30)  # Field name made lowercase.
    date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'zt_testresult'


class ZtTestrun(models.Model):
    task = models.IntegerField()
    case = models.IntegerField()
    version = models.IntegerField()
    assignedto = models.CharField(db_column='assignedTo', max_length=30)  # Field name made lowercase.
    lastrunner = models.CharField(db_column='lastRunner', max_length=30)  # Field name made lowercase.
    lastrundate = models.DateTimeField(db_column='lastRunDate')  # Field name made lowercase.
    lastrunresult = models.CharField(db_column='lastRunResult', max_length=30)  # Field name made lowercase.
    status = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'zt_testrun'
        unique_together = (('task', 'case'),)


class ZtTesttask(models.Model):
    name = models.CharField(max_length=90)
    product = models.IntegerField()
    project = models.IntegerField()
    build = models.CharField(max_length=30)
    owner = models.CharField(max_length=30)
    pri = models.IntegerField()
    begin = models.DateField()
    end = models.DateField()
    desc = models.TextField()
    report = models.TextField()
    status = models.CharField(max_length=7)
    deleted = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'zt_testtask'


class ZtTodo(models.Model):
    account = models.CharField(max_length=30)
    date = models.DateField()
    begin = models.SmallIntegerField()
    end = models.SmallIntegerField()
    type = models.CharField(max_length=10)
    idvalue = models.IntegerField()
    pri = models.IntegerField()
    name = models.CharField(max_length=150)
    desc = models.TextField()
    status = models.CharField(max_length=5)
    private = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'zt_todo'


class ZtUser(models.Model):
    dept = models.IntegerField()
    account = models.CharField(unique=True, max_length=30)
    password = models.CharField(max_length=32)
    role = models.CharField(max_length=10)
    realname = models.CharField(max_length=30)
    nickname = models.CharField(max_length=60)
    commiter = models.CharField(max_length=100)
    avatar = models.CharField(max_length=30)
    birthday = models.DateField()
    gender = models.CharField(max_length=1)
    email = models.CharField(max_length=90)
    skype = models.CharField(max_length=90)
    qq = models.CharField(max_length=20)
    yahoo = models.CharField(max_length=90)
    gtalk = models.CharField(max_length=90)
    wangwang = models.CharField(max_length=90)
    mobile = models.CharField(max_length=11)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=120)
    zipcode = models.CharField(max_length=10)
    join = models.DateField()
    visits = models.IntegerField()
    ip = models.CharField(max_length=15)
    last = models.IntegerField()
    fails = models.IntegerField()
    locked = models.DateTimeField()
    deleted = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'zt_user'


class ZtUsercontact(models.Model):
    account = models.CharField(max_length=30)
    listname = models.CharField(db_column='listName', max_length=60)  # Field name made lowercase.
    userlist = models.TextField(db_column='userList')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'zt_usercontact'


class ZtUsergroup(models.Model):
    account = models.CharField(max_length=30)
    group = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'zt_usergroup'
        unique_together = (('account', 'group'),)


class ZtUserquery(models.Model):
    account = models.CharField(max_length=30)
    module = models.CharField(max_length=30)
    title = models.CharField(max_length=90)
    form = models.TextField()
    sql = models.TextField()

    class Meta:
        managed = False
        db_table = 'zt_userquery'


class ZtUsertpl(models.Model):
    account = models.CharField(max_length=30)
    type = models.CharField(max_length=30)
    title = models.CharField(max_length=150)
    content = models.TextField()

    class Meta:
        managed = False
        db_table = 'zt_usertpl'
