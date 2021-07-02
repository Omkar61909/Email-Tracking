from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from emails import views as email_views


urlpatterns = [
	path(r'email/send/', email_views.EmailCampaignDetail.as_view(), name='EmailCampaignDetail'),
	path(r'open/event/', email_views.EmailOpenEventDetail.as_view(), name='EmailOpenEventDetail')
]

