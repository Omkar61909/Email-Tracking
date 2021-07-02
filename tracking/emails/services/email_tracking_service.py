import datetime
import json
import base64
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


class EmailClickEvent(object):
    def __init__(self, data):
        self.data = data
        self.encoded_click_url_string = self._get_attribute('encoded_click_string')
        self.decoded_click_url_data = self._decoded_click_url_data()
        self.decoded_url_id = self._decoded_url_id()

    def _get_attribute(self, attribute_key):
        attribute_value = None
        if self.data.get(attribute_key):
            attribute_value = self.data[attribute_key]
        return attribute_value

    def _decoded_click_url_data(self):
        decoded_click_url_data = json.loads(base64.urlsafe_b64decode(self.encoded_click_url_string.encode()).decode())
        return decoded_click_url_data

    def _decoded_url_id(self):
        decoded_url_id = None
        if self.decoded_click_url_data.get('encoded_url_id'):
            decoded_url_id = int(self.decoded_click_url_data['encoded_url_id'], base=16)
        return decoded_url_id

    def _email_campaign_model_data(self):
        email_campaign_model_data = dict()
        model_value = email_models.EmailTracking.objects.filter(
            id=self.decoded_url_id).values('click_count', 'first_click_datetime', 'latest_click_datetime').first()
        if model_value:
            email_campaign_model_data = dict(model_value)
        return email_campaign_model_data

    def _update_email_campaign_model_data(self, email_campaign_model_data):
        current_datetime = datetime.datetime.now()
        updation_data = {
            'click_count': email_campaign_model_data.get('click_count') + 1,
            'latest_click_datetime': current_datetime
        }
        if email_campaign_model_data.get('first_click_datetime') in [None, '']:
            updation_data['first_click_datetime'] = current_datetime        
        email_models.EmailTracking.objects.filter(id=self.decoded_url_id).update(**updation_data)

    def perform_tasks_and_get_data(self):
        data = {
            'destination_url': self.decoded_click_url_data.get('destination_url')
        }
        email_campaign_model_data = self._email_campaign_model_data()
        if email_campaign_model_data:
            self._update_email_campaign_model_data(email_campaign_model_data)
        return data