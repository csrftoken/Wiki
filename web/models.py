
import hashlib

from django.db import models
from django.utils.safestring import mark_safe
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, Group, PermissionsMixin,
)

# Create your models here.


class Book(models.Model):
    """
    书籍名称
    """
    name = models.CharField(max_length=32, verbose_name="书籍名称", unique=True)
    img = models.CharField(max_length=128, verbose_name="图片", )
    brief = models.CharField(max_length=255, verbose_name="概述", )
    status = models.BooleanField(verbose_name="上线状态")
    date = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class BookChapter(models.Model):
    """
    书籍章节
    """
    book = models.ForeignKey("Book", verbose_name="Wiki名称")
    chapter = models.IntegerField(verbose_name="章节数")
    name = models.CharField(max_length=32, verbose_name="章节名称")
    brief = models.CharField(max_length=128, verbose_name="章节介绍")
    order = models.IntegerField(verbose_name="排序序号")
    date = models.DateTimeField(auto_now_add=True)

    def __repr__(self):
        return "{}-{}".format(self.book, self.name)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["order", ]


class BookSection(models.Model):
    """
    书籍条目
    """
    chapter = models.ForeignKey("BookChapter", verbose_name="章节名称")
    name = models.CharField(max_length=64, verbose_name="名称")
    content = models.TextField(verbose_name="主体内容")
    uv = models.IntegerField(default=0, verbose_name="UV数")
    pv = models.IntegerField(default=0, verbose_name="PV数")
    order = models.IntegerField(verbose_name="排序")
    memo = models.CharField(max_length=128, verbose_name="摘要（说明）")
    status = models.BooleanField(verbose_name="是否保存为草稿(勾选后前台不展示该篇)",)
    date = models.DateTimeField(auto_now_add=True)

    def __repr__(self):
        return "{}-{}".format(self.chapter, self.name)

    class Meta:
        ordering = ["order", ]


class AccountManager(BaseUserManager):
    def create_user(self, username, mobile, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not username:
            raise ValueError('Username cannot be null')

        user = self.model(
            username=username,
            mobile=mobile,
            # name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, mobile):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(username,
                                password=password,
                                mobile=mobile,
                                # name=name,
                                )
        user.is_superuser = True
        user.is_active = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser, PermissionsMixin):
    username = models.CharField("用户名", max_length=64, unique=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        blank=True,
        null=True
    )
    mobile = models.BigIntegerField(verbose_name="手机", unique=True, help_text="用于手机验证码登录")
    uid = models.CharField(max_length=64, unique=True)  # 与第3方交互用户信息时，用这个uid,以避免泄露敏感用户信息
    password = models.CharField('password', max_length=128,
                                help_text=mark_safe('''<a class='btn-link' href='password'>重置密码</a>'''))
    is_active = models.BooleanField(default=True, verbose_name="账户状态")
    is_staff = models.BooleanField(verbose_name='staff status', default=False, help_text='决定着用户是否可登录管理后台')
    memo = models.TextField('备注', blank=True, null=True, default=None)
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="注册时间")

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['mobile']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    class Meta:
        verbose_name = '账户信息'
        verbose_name_plural = "账户信息"

    def save(self, *args, **kwargs):
        if not self.pk:
            # This code only happens if the objects is not in the database yet. Otherwise it would have pk
            m = hashlib.md5()
            m.update(self.username.encode(encoding="utf-8"))
            self.uid = m.hexdigest()
        super(Account, self).save(*args, **kwargs)

    objects = AccountManager()

    def __str__(self):
        return "%s(%s)" % (self.username, self.name)
