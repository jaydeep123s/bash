from datetime import datetime
import logging
import uuid

from django.conf import settings
from django.core.mail import EmailMessage
from django.db import models
from django.utils.translation import gettext_lazy as _

from match4healthcare.utils.email import send_mass_mail_sendgrid

from .user import User

logger = logging.getLogger(__name__)

ONLY_VALIDATED = 0
ONLY_NOT_VALIDATED = 1
ALL = 2
VALIDATED_AND_APPROVED = 3

VALIDATION_CHOICES = (
    (ONLY_VALIDATED, _("validierte")),
    (ONLY_NOT_VALIDATED, _("nicht validierte")),
    (ALL, _("validierte und nicht validierte")),
    (VALIDATED_AND_APPROVED, _("validiert und von uns approved")),
)


class NewsletterState:
    BEING_EDITED = 1
    UNDER_APPROVAL = 2
    READY_TO_SEND = 3
    SENT = 4


class Newsletter(models.Model):
    uuid = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)

    registration_date = models.DateTimeField(default=datetime.now, blank=True, null=True)
    last_edited_date = models.DateTimeField(default=None, blank=True, null=True)
    frozen_date = models.DateTimeField(default=None, blank=True, null=True)
    send_date = models.DateTimeField(default=None, blank=True, null=True)

    letter_authored_by = models.ManyToManyField(to=User, related_name="letter_authored_by")
    letter_approved_by = models.ManyToManyField(
        to="User", related_name="letter_approved_by", through="LetterApprovedBy"
    )
    sent_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="sent_by")
    frozen_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="frozen_by"
    )

    subject = models.CharField(max_length=200, default="")
    message = models.TextField(default="", max_length=1000000)

    was_sent = models.BooleanField(default=False)

    send_to_hospitals = models.BooleanField(default=False)
    send_to_students = models.BooleanField(default=False)

    user_validation_required = models.IntegerField(
        choices=VALIDATION_CHOICES, default=ONLY_VALIDATED, blank=False
    )

    def sending_state(self):
        if self.was_sent:
            return NewsletterState.SENT
        else:
            if self.frozen_by is None:
                return NewsletterState.BEING_EDITED
            elif self.required_approvals() > 0:
                return NewsletterState.UNDER_APPROVAL
            else:
                return NewsletterState.READY_TO_SEND

    def unfreeze(self):
        self.frozen_by = None
        self.frozen_date = None
        self.letter_approved_by.clear()

    def approve_from(self, user):
        self.letter_approved_by.add(user)

    def send(self, user):
        self.send_newsletter_out()
        self.send_date = datetime.now()
        self.was_sent = True
        self.sent_by = user

    def freeze(self, user):
        self.frozen_by = user
        self.frozen_date = datetime.now()

    def edit_meta_data(self, user):
        self.letter_authored_by.add(user)
        self.last_edited_date = datetime.now()

    def send_testmail_to(self, email_receipient):
        email = EmailMessage(
            subject=self._subject(),
            body=self.message,
            from_email=settings.NOREPLY_MAIL,
            to=[email_receipient],
        )
        email.content_subtype = "html"
        email.send()

    def has_been_approved_by(self, user):
        return (
            self.letter_approved_by.filter(
                letterapprovedby__user=user, letterapprovedby__did_see_email=True
            ).count()
            == 1
        )

    def required_approvals(self):
        return (
            settings.NEWSLETTER_REQUIRED_APPROVERS
            - self.letter_approved_by.filter(letterapprovedby__did_see_email=True).count()
        )

    def send_approval_mail(self, approval, host):
        body = "<h3>Link zum Approven ganz unten</h3><hr>"
        body += self.message
        body += (
            '<hr><a href="https://%s/matching_old/view_newsletter/%s"> Ich habe Probleme gefunden und will den '
            "Newsletter bearbeiten.</a><br>" % (host, self.uuid)
        )
        body += (
            '<a href="https://%s">Ich bestätige, dass diese E-Mail als Newsletter'
            " abgeschickt werden darf.</a>" % approval.verify_url(host)
        )
        email = EmailMessage(
            subject=self._subject(),
            body=body,
            from_email=settings.NOREPLY_MAIL,
            to=[approval.user.email],
        )
        email.content_subtype = "html"
        email.send()

    def _subject(self):
        return "[match4healthcare] " + str(self.subject)

    def send_newsletter_out(self):
        if self.sending_state() != NewsletterState.READY_TO_SEND:
            raise ValueError(
                "The newsletter is not ready to send, so you cannot send out an email."
            )

        hospital_filter = {"is_hospital": True}
        student_filter = {"is_student": True}

        if self.user_validation_required == ONLY_VALIDATED:
            hospital_filter["validated_email"] = True
            student_filter["validated_email"] = True
        elif self.user_validation_required == VALIDATED_AND_APPROVED:
            hospital_filter["validated_email"] = True
            hospital_filter["hospital__is_approved"] = True
            student_filter["validated_email"] = True
        elif self.user_validation_required == ONLY_NOT_VALIDATED:
            hospital_filter["validated_email"] = False
            student_filter["validated_email"] = False
        elif ALL:
            pass

        if self.send_to_hospitals:
            recipient_hospitals_qs = User.objects.filter(**hospital_filter).values_list(
                "email", flat=True
            )
            n_hospital = recipient_hospitals_qs.count()
            logger.info("Starting to send out newsletter to %s hospitals...", n_hospital)
            self._send_mail(recipient_hospitals_qs, n_hospital)

        if self.send_to_students:
            recipient_student_qs = User.objects.filter(**student_filter).values_list(
                "email", flat=True
            )
            n_students = recipient_student_qs.count()
            logger.info("Starting to send out newsletter to %s students...", n_students)
            self._send_mail(recipient_student_qs, n_students)

    def _send_mail(self, recipients, n):

        chunksize = 950
        # max allowed by sendgrid: 1k (but they have weird extra limitations, so be sure)
        # https://sendgrid.com/docs/API_Reference/Web_API_v3/Mail/index.html#-Limitations

        for i in range((n // chunksize) + 1):
            pos = i * chunksize
            send_mass_mail_sendgrid(
                recipient_list=recipients[pos : min(pos + chunksize, n)],
                subject=self._subject(),
                html_body=self.message,
                from_mail=settings.NOREPLY_MAIL,
            )
