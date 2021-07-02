from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from django.http import HttpResponse
from emails import serializers as email_serializers
from emails.services import email_tracking_service

# Create your views here.
class EmailCampaignDetail(APIView):
    def post(self, request, *args, **kwargs):
        serializer = email_serializers.EmailCampaignSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.perform_tasks_and_get_data(), status=status.HTTP_200_OK)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class EmailOpenEventDetail(APIView):
    def _request_data(self, request):
        request_data = {
            'encoded_url_id': request.GET.get('encoded_url_id'),
        }
        return request_data

    def get(self, request, *args, **kwargs):
        request_data = self._request_data(request=request)
        email_open_event_object = email_tracking_service.EmailOpenEvent(data=request_data).perform_tasks()
        return HttpResponse('', content_type="image/jpeg")
