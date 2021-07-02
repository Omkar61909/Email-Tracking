from django.db import models

# Create your models here.
class EmailTracking(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    email_id = models.EmailField(blank=False, null=False)
    open_count = models.IntegerField(null=True, blank=True, default = 0)
    first_open_datetime = models.DateTimeField(null=True, blank=True)
    latest_open_datetime = models.DateTimeField(null=True, blank=True)
    click_count = models.IntegerField(null=True, blank=True, default = 0)
    first_click_datetime = models.DateTimeField(null=True, blank=True)
    latest_click_datetime = models.DateTimeField(null=True, blank=True)
    destination_url = models.URLField(max_length=200, null=True, blank=True)
    data = models.TextField(null=True, blank=True)

    class Meta(object):
        db_table = 'email_tracking_data' 	    