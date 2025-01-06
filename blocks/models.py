from django.db import models

class BaseBlock(models.Model):
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['order']

class BasePageBlock(BaseBlock):
    title = models.CharField(max_length=200)
    subtitle = models.TextField(blank=True)
    content = models.JSONField(default=dict, help_text="Stores block-specific content and settings")
    custom_styles = models.JSONField(default=dict, blank=True)
    custom_classes = models.CharField(max_length=200, blank=True)

    class Meta:
        abstract = True

class FirstPageBlock(BasePageBlock):
    BLOCK_TYPES = (
        ('hero', 'Hero Section'),
        ('carousel', 'Image Carousel'),
        ('text', 'Text Block'),
        ('contact_form', 'Contact Form'),
        ('map', 'Google Map'),
        ('image', 'Single Image'),
        ('video', 'Video Block')
    )

    block_type = models.CharField(max_length=20, choices=BLOCK_TYPES)
    image = models.ImageField(upload_to='first_page/images/', null=True, blank=True)
    video = models.FileField(upload_to='first_page/videos/', null=True, blank=True)

    def __str__(self):
        return f"First Page - {self.get_block_type_display()} - {self.title}"

class SecondPageBlock(BasePageBlock):
    BLOCK_TYPES = (
        ('program', 'Program Block'),
        ('faq', 'FAQ Section'),
        ('pricing', 'Pricing Table'),
        ('features', 'Features List')
    )

    block_type = models.CharField(max_length=20, choices=BLOCK_TYPES)
    icon = models.FileField(upload_to='second_page/icons/', null=True, blank=True)

    def __str__(self):
        return f"Second Page - {self.get_block_type_display()} - {self.title}"

class ThirdPageBlock(BasePageBlock):
    BLOCK_TYPES = (
        ('partner', 'Partner Block'),
        ('testimonial', 'Testimonial'),
        ('gallery', 'Image Gallery'),
        ('info', 'Information Block')
    )

    block_type = models.CharField(max_length=20, choices=BLOCK_TYPES)
    image = models.ImageField(upload_to='third_page/images/', null=True, blank=True)

    def __str__(self):
        return f"Third Page - {self.get_block_type_display()} - {self.title}"

class MediaItem(models.Model):
    first_page_block = models.ForeignKey(FirstPageBlock, on_delete=models.CASCADE,
                                       related_name='media_items', null=True, blank=True)
    second_page_block = models.ForeignKey(SecondPageBlock, on_delete=models.CASCADE,
                                        related_name='media_items', null=True, blank=True)
    third_page_block = models.ForeignKey(ThirdPageBlock, on_delete=models.CASCADE,
                                       related_name='media_items', null=True, blank=True)
    file = models.FileField(upload_to='blocks/media/')
    title = models.CharField(max_length=200)
    caption = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class FormSubmission(models.Model):
    block = models.ForeignKey(FirstPageBlock, on_delete=models.CASCADE)
    form_data = models.JSONField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Form submission for {self.block.title} at {self.created_at}"