from rest_framework import serializers
from emails.services import email_campaign_service

class EmailCampaignSerializer(serializers.Serializer):
	receiver_email_id = serializers.CharField()
	link = serializers.URLField()

	def perform_tasks_and_get_data(self):
		data = email_campaign_service.EmailCampaign(self.validated_data).perform_tasks_and_get_data()
		return data
