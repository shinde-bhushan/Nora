from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    user_id = models.CharField(max_length=255)
    user_group = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)

    class Meta:
        '''
        to set table name in database
        '''
        db_table = "user"