from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, unique=True, null=False, blank=False, editable=False)
    user_id = models.CharField(max_length=255, editable=False)
    role_id = models.CharField(max_length=255, editable=False, default="4")
    is_verified = models.BooleanField(default=False)

    class Meta:
        '''
        to set table name in database
        '''
        db_table = "user"