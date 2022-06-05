from django.contrib import admin

# Register your models here.
from .models import Account, Resource, UserGroup, Menu


@admin.register(Account)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username',)  # 展示
    list_filter = ('username',)
    list_per_age = 20  # 分页
    search_fields = ('username',)


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('resourcename', 'url', 'status', 'pid')  # 展示
    list_filter = ('resourcename',)
    list_per_age = 20  # 分页
    search_fields = ('resourcename',)


@admin.register(UserGroup)
class UserGroupAdmin(admin.ModelAdmin):
    list_display = ('name', )  # 展示
    list_filter = ('name',)
    list_per_age = 20  # 分页
    search_fields = ('name',)


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('name_menu',)  # 展示
    list_filter = ('name_menu',)
    list_per_age = 20  # 分页
    search_fields = ('name_menu',)


