import json
import base64
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from emails import models as email_models


class EmailCampaign(object):
    def __init__(self, data):
        self.data = data
        self.receiver_email_id = self._get_attribute('receiver_email_id')
        self.link = self._get_attribute('link')

    def _get_attribute(self, attribute_key):
        attribute_value = None
        if self.data.get(attribute_key):
            attribute_value = self.data[attribute_key]
        return attribute_value

    def _create_email_tracking_model_entry(self):
        model_creation_data = {
            'email_id': self.receiver_email_id,
            'destination_url': self.link
        }
        model_object = email_models.EmailTracking.objects.create(
            **model_creation_data)
        return model_object.id

    def _encode_model_row_id(self, row_id):
        return hex(row_id)

    def _encoded_data_string(self, row_id):
        click_url_data = {
            'encoded_url_id': hex(row_id),
            'destination_url': self.link
        }
        encoded_data_string = base64.urlsafe_b64encode(json.dumps(click_url_data).encode()).decode()
        return encoded_data_string

    def _email_template_data(self, encoded_row_id, encoded_data_string):
        email_template_data = {
            'image_url': settings.EMAIL_TRACKING_BASE_URL + 'open/event/?encoded_url_id={encoded_row_id}'.format(encoded_row_id=encoded_row_id),
            'click_url': settings.EMAIL_TRACKING_BASE_URL + 'click/event/?encoded_click_string={encoded_click_string}'.format(encoded_click_string=encoded_data_string)
        }
        return email_template_data

    def _html_part(self, template_data):
        template = None
        template = get_template('sample_template.html')
        html_part = template.render(template_data)
        return html_part

    def _send_email_to_customer(self, html_part):
        msg = EmailMultiAlternatives(
            'test_subject', None, 'omkar61909@gmail.com', [self.receiver_email_id])
        msg.attach_alternative(html_part, 'text/html')
        result = msg.send(True)
        return result

    def perform_tasks_and_get_data(self):
        data = dict()
        """
            create entry in the table, use the row_id,
            use the row_id to generate callback url

        """
        email_tracking_model_row_id = self._create_email_tracking_model_entry()
        encoded_row_id = self._encode_model_row_id(email_tracking_model_row_id)
        encoded_data_string = self._encoded_data_string(email_tracking_model_row_id)
        email_template_data = self._email_template_data(encoded_row_id, encoded_data_string)
        html_part = self._html_part(email_template_data)
        self._send_email_to_customer(html_part)
        return data
