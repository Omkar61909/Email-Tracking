import datetime
from emails import models as email_models

class EmailOpenEvent(object):
    def __init__(self, data):
        self.data = data
        self.encoded_url_id = self._get_attribute('encoded_url_id')
        self.decoded_url_id = self._decoded_url_id()

    def _get_attribute(self, attribute_key):
        attribute_value = None
        if self.data.get(attribute_key):
            attribute_value = self.data[attribute_key]
        return attribute_value

    def _decoded_url_id(self):
        decoded_url_id = None
        if self.encoded_url_id:
            decoded_url_id = int(self.encoded_url_id, base=16)
        return decoded_url_id

    def _email_campaign_model_data(self):
        email_campaign_model_data = dict()
        model_value = email_models.EmailTracking.objects.filter(
            id=self.decoded_url_id).values('open_count', 'first_open_datetime', 'latest_open_datetime').first()
        if model_value:
            email_campaign_model_data = dict(model_value)
        return email_campaign_model_data

    def _update_email_campaign_model_data(self, email_campaign_model_data):
        current_datetime = datetime.datetime.now()
        updation_data = {
            'latest_open_datetime': current_datetime,
            'open_count': email_campaign_model_data.get('open_count', 0) + 1, 
        } 
        if email_campaign_model_data.get('first_open_datetime') in [None, '']:
            updation_data['first_open_datetime'] = current_datetime
        email_models.EmailTracking.objects.filter(id=self.decoded_url_id).update(**updation_data)


    def perform_tasks(self):
        email_campaign_model_data = self._email_campaign_model_data()
        if email_campaign_model_data:
            self._update_email_campaign_model_data(email_campaign_model_data)
