接口测试平台从开始到放弃<br>
使用方法：<br>
1.安装Python3环境<br>
2.下载代码到本地并解压<br>
3.cmd到根目录下安装相关依赖包<br>
pip install -r requirements.txt<br>
4.安装mysql数据库，配置数据库连接，进入apiTest/settings.py<br>
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 数据库引擎
        'NAME': 'autoapi',
        'USER': 'root',
        'PASSWORD': '12345678',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            "init_command": "SET default_storage_engine='INNODB'"
        }
   }
}
5.cmd到根目录下，让 Django 知道我们在我们的模型有一些变更<br>
python manage.py makemigrations<br>
6.创造或修改表结构<br>
python manage.py migrate <br>
7.创建超级用户，用于登录后台管理<br>
python manage.py createsuperuser<br>
8.运行启动django服务<br>
python manage.py runserver 0.0.0.0:8000<br>
9.现在就可以访问 http://127.0.0.1:8000/login 进行登录<br>
