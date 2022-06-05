from django.contrib import admin

# Register your models here.


from .models import Area, House


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('name',)  # 展示
    list_filter = ('name',)
    list_per_age = 20  # 分页
    search_fields = ('name',)


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = ('square',)  # 展示
    list_filter = ('square',)
    list_per_age = 20  # 分页
    search_fields = ('square',)


