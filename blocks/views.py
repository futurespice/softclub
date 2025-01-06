# blocks/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import (
    FirstPageBlock, SecondPageBlock, ThirdPageBlock,
    MediaItem, FormSubmission
)
from .serializers import (
    FirstPageBlockSerializer, SecondPageBlockSerializer,
    ThirdPageBlockSerializer, MediaItemSerializer,
    FormSubmissionSerializer
)


class BasePageViewSet(viewsets.ModelViewSet):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    @swagger_auto_schema(
        method='post',
        request_body=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'order': openapi.Schema(type=openapi.TYPE_INTEGER),
                }
            )
        )
    )
    @action(detail=False, methods=['post'])
    def reorder(self, request):
        for item in request.data:
            self.queryset.model.objects.filter(id=item['id']).update(order=item['order'])
        return Response({'status': 'success'})

    @action(detail=True, methods=['post'])
    def duplicate(self, request, pk=None):
        block = self.get_object()
        block.pk = None
        block.title = f"Copy of {block.title}"
        block.save()
        return Response(self.get_serializer(block).data)


class FirstPageViewSet(BasePageViewSet):
    queryset = FirstPageBlock.objects.all()
    serializer_class = FirstPageBlockSerializer

    @swagger_auto_schema(
        method='post',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'files[]': openapi.Schema(type=openapi.TYPE_FILE),
                'titles[]': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)),
                'captions[]': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)),
            }
        )
    )
    @action(detail=True, methods=['post'])
    def upload_media(self, request, pk=None):
        block = self.get_object()
        files = request.FILES.getlist('files[]')
        titles = request.POST.getlist('titles[]')
        captions = request.POST.getlist('captions[]')

        media_items = []
        for i, file in enumerate(files):
            title = titles[i] if i < len(titles) else f"Media {i + 1}"
            caption = captions[i] if i < len(captions) else ""

            media_item = MediaItem.objects.create(
                first_page_block=block,
                file=file,
                title=title,
                caption=caption,
                order=i
            )
            media_items.append(media_item)

        return Response(MediaItemSerializer(media_items, many=True).data)

    @swagger_auto_schema(
        method='post',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'form_data': openapi.Schema(type=openapi.TYPE_OBJECT)
            }
        )
    )
    @action(detail=True, methods=['post'])
    def submit_form(self, request, pk=None):
        block = self.get_object()
        submission = FormSubmission.objects.create(
            block=block,
            form_data=request.data.get('form_data', {}),
            ip_address=request.META.get('REMOTE_ADDR')
        )
        return Response(FormSubmissionSerializer(submission).data)


class SecondPageViewSet(BasePageViewSet):
    queryset = SecondPageBlock.objects.all()
    serializer_class = SecondPageBlockSerializer

    @action(detail=True, methods=['post'])
    def upload_icon(self, request, pk=None):
        block = self.get_object()
        if 'icon' in request.FILES:
            block.icon = request.FILES['icon']
            block.save()
        return Response(self.get_serializer(block).data)


class ThirdPageViewSet(BasePageViewSet):
    queryset = ThirdPageBlock.objects.all()
    serializer_class = ThirdPageBlockSerializer

    @action(detail=True, methods=['post'])
    def upload_image(self, request, pk=None):
        block = self.get_object()
        if 'image' in request.FILES:
            block.image = request.FILES['image']
            block.save()
        return Response(self.get_serializer(block).data)