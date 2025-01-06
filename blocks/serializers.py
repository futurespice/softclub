# blocks/serializers.py
from rest_framework import serializers
from .models import (
    FirstPageBlock, SecondPageBlock, ThirdPageBlock,
    MediaItem, FormSubmission
)

class MediaItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaItem
        fields = ['id', 'file', 'title', 'caption', 'order', 'created_at']

class FormSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormSubmission
        fields = ['id', 'form_data', 'created_at', 'ip_address']

class BaseBlockSerializer(serializers.ModelSerializer):
    content_preview = serializers.SerializerMethodField()

    def get_content_preview(self, obj):
        """Возвращает предварительный просмотр контента в зависимости от типа блока"""
        if obj.block_type == 'text':
            return obj.content.get('text', '')[:100] + '...'
        return str(obj.content)

class FirstPageBlockSerializer(BaseBlockSerializer):
    media_items = MediaItemSerializer(many=True, read_only=True)
    form_submissions_count = serializers.SerializerMethodField()

    class Meta:
        model = FirstPageBlock
        fields = [
            'id', 'block_type', 'title', 'subtitle', 'content',
            'custom_styles', 'custom_classes', 'order', 'is_active',
            'image', 'video', 'media_items', 'form_submissions_count',
            'content_preview', 'created_at', 'updated_at'
        ]

    def get_form_submissions_count(self, obj):
        if obj.block_type == 'contact_form':
            return obj.formsubmission_set.count()
        return None

class SecondPageBlockSerializer(BaseBlockSerializer):
    media_items = MediaItemSerializer(many=True, read_only=True)

    class Meta:
        model = SecondPageBlock
        fields = [
            'id', 'block_type', 'title', 'subtitle', 'content',
            'custom_styles', 'custom_classes', 'order', 'is_active',
            'icon', 'media_items', 'content_preview', 'created_at', 'updated_at'
        ]

class ThirdPageBlockSerializer(BaseBlockSerializer):
    media_items = MediaItemSerializer(many=True, read_only=True)

    class Meta:
        model = ThirdPageBlock
        fields = [
            'id', 'block_type', 'title', 'subtitle', 'content',
            'custom_styles', 'custom_classes', 'order', 'is_active',
            'image', 'media_items', 'content_preview', 'created_at', 'updated_at'
        ]