# blocks/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import (
    FirstPageBlock, SecondPageBlock, ThirdPageBlock,
    MediaItem, FormSubmission
)


class MediaItemInline(admin.TabularInline):
    model = MediaItem
    extra = 1
    fields = ('file', 'title', 'caption', 'order')
    ordering = ('order',)


class BaseBlockAdmin(admin.ModelAdmin):
    list_display = ('title', 'block_type', 'order', 'is_active', 'created_at', 'updated_at')
    list_filter = ('block_type', 'is_active')
    search_fields = ('title', 'subtitle', 'content')
    list_editable = ('order', 'is_active')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('block_type', 'title', 'subtitle', 'order', 'is_active')
        }),
        ('Содержимое', {
            'fields': ('content',),
            'classes': ('collapse',)
        }),
        ('Стилизация', {
            'fields': ('custom_styles', 'custom_classes'),
            'classes': ('collapse',)
        }),
        ('Информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(FirstPageBlock)
class FirstPageBlockAdmin(BaseBlockAdmin):
    inlines = [MediaItemInline]

    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px;"/>', obj.image.url)
        return "-"

    preview_image.short_description = 'Preview'

    list_display = BaseBlockAdmin.list_display + ('preview_image',)
    fieldsets = BaseBlockAdmin.fieldsets + (
        ('Медиа', {
            'fields': ('image', 'video'),
            'classes': ('collapse',)
        }),
    )


@admin.register(SecondPageBlock)
class SecondPageBlockAdmin(BaseBlockAdmin):
    inlines = [MediaItemInline]

    def preview_icon(self, obj):
        if obj.icon:
            return format_html('<img src="{}" style="max-height: 30px;"/>', obj.icon.url)
        return "-"

    preview_icon.short_description = 'Icon'

    list_display = BaseBlockAdmin.list_display + ('preview_icon',)
    fieldsets = BaseBlockAdmin.fieldsets + (
        ('Медиа', {
            'fields': ('icon',),
            'classes': ('collapse',)
        }),
    )


@admin.register(ThirdPageBlock)
class ThirdPageBlockAdmin(BaseBlockAdmin):
    inlines = [MediaItemInline]

    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px;"/>', obj.image.url)
        return "-"

    preview_image.short_description = 'Preview'

    list_display = BaseBlockAdmin.list_display + ('preview_image',)
    fieldsets = BaseBlockAdmin.fieldsets + (
        ('Медиа', {
            'fields': ('image',),
            'classes': ('collapse',)
        }),
    )


@admin.register(FormSubmission)
class FormSubmissionAdmin(admin.ModelAdmin):
    list_display = ('block', 'ip_address', 'created_at')
    list_filter = ('block', 'created_at')
    readonly_fields = ('block', 'form_data', 'ip_address', 'created_at')

    def has_add_permission(self, request):
        return False


@admin.register(MediaItem)
class MediaItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_block', 'order', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'caption')
    ordering = ('order',)

    def get_block(self, obj):
        if obj.first_page_block:
            return f"First Page - {obj.first_page_block.title}"
        elif obj.second_page_block:
            return f"Second Page - {obj.second_page_block.title}"
        elif obj.third_page_block:
            return f"Third Page - {obj.third_page_block.title}"
        return "No block"

    get_block.short_description = 'Block'