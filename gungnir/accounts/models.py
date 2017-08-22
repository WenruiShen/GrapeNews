from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_comma_separated_integer_list

# customized user model
# extends from default model
class User(AbstractUser):

    collection_topic_id_array = models.CharField(max_length=20, validators=[validate_comma_separated_integer_list],
                                                 null=True, blank=True)
    REQUIRED_FIELDS = ['email']

    class Meta(AbstractUser.Meta):
        pass
