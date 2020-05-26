import logging

from django.db import models
import numpy as np

from .newsletter import Newsletter
from .user import User

logger = logging.getLogger(__name__)


def random_number():
    return np.random.randint(0, 100000)


class LetterApprovedBy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    newsletter = models.ForeignKey(Newsletter, on_delete=models.CASCADE)
    approval_code = models.IntegerField(default=random_number)
    did_see_email = models.BooleanField(default=False)

    class Meta:
        unique_together = (
            "user",
            "newsletter",
        )

    def verify_url(self, host):
        return "%s/matching/did_see_newsletter/%s/%s" % (
            host,
            self.newsletter.uuid,
            self.approval_code,
        )
