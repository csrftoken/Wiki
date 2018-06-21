# LuffyWiki

## 环境

```

python 3.6.2

django 1.11.3

```

## 配置

### 创建虚拟环境

1、安装 （如果安装请忽略）

```
pip3 install virtualenv
```

2、创建

```
mkdir -p /app/project_name

cd    /app/project_name

virtualenv --no-site-packages project_name

```

3、使用及退出

```

source project_name/bin/activate

deactivate

```

### Clone 代码

1、配置

```
git config --global user.name "luffy"            # 配置git使用用户
git config --global user.email luffy@qq.com      # 邮箱
git config --global color.ui true                # 语法高亮
git config --list                                # 查看
```

2、创建并clone代码

```
mkdir /usr/local/luffy_dev

cd /usr/local/luffy_dev

git init

git clone https://github.com/triaquae/luffy.git

git fetch origin dev  # 指定代码分支 `master`

git checkout -b dev

git pull origin dev

```

## 启动

1、准备

```
cd `project_name`

pip3 install -r requirements.txt

mkdir `app`/migrations

touch `app`/migrations/__init__.py

python3 manage.py makemigrations

python3 manage.py migrate

```

2、开始

```

1、初始化数据
python manage.py loaddata init.json

2、启动
python3 manage.py runserver 0.0.0.0:80

3、访问

默认账户名及密码

root

root123456

```
