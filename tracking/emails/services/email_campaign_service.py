from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from emails import models as email_models
from django.conf import settings

class EmailCampaign(object):
    def __init__(self, data):
        self.data = data
        self.receiver_email_id = self._get_attribute('receiver_email_id')

    def _get_attribute(self, attribute_key):
        attribute_value = None
        if self.data.get(attribute_key):
            attribute_value = self.data[attribute_key]
        return attribute_value

    def _create_email_tracking_model_entry(self):
        model_creation_data = {
            'email_id': self.receiver_email_id,         
        }
        model_object = email_models.EmailTracking.objects.create(**model_creation_data)
        return model_object.id

    def _encode_model_row_id(self, row_id):
        return hex(row_id)

    def _email_template_data(self, encoded_row_id):
        email_template_data = {
            'image_url': settings.EMAIL_TRACKING_BASE_URL + 'open/event/?encoded_url_id={encoded_row_id}'.format(encoded_row_id=encoded_row_id)
        }
        return email_template_data

    def _html_part(self, template_data):
        template = None
        template = get_template('sample_template.html')
        html_part = template.render(template_data)
        return html_part

    def _send_email_to_customer(self, html_part):
        msg = EmailMultiAlternatives(
            'test_subject', None, 'omkar61909@gmail.com',[self.receiver_email_id])
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
        email_template_data = self._email_template_data(encoded_row_id)
        html_part = self._html_part(email_template_data)
        self._send_email_to_customer(html_part)
        return data