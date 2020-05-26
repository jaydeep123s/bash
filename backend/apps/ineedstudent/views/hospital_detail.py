from datetime import datetime
import logging

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import TemplateView

from apps.iamstudent.models import EmailToHospital, Student
from apps.ineedstudent.forms import EmailToHospitalForm
from apps.ineedstudent.models import Hospital
from apps.mapview.src.map import haversine, plzs

logger = logging.getLogger(__name__)


@method_decorator([login_required], name="dispatch")
class HospitalDetailView(TemplateView):
    def post(self, request, uuid):

        h = get_object_or_404(Hospital, uuid=uuid)
        initial = {
            "subject": _("Neues Hilfsangebot"),
            "message": _(
                "Hallo, ich habe ihr Gesuche auf der Plattform match4healthcare gesehen und bin für die Stelle qualifiziert.\nIch bin...\nIch möchte helfen in dem..."
            ),
        }

        if request.POST and request.user.is_student and request.user.validated_email:
            s = request.user.student

            email_form = EmailToHospitalForm(request.POST, initial=initial)

            if email_form.is_valid():
                start_text = _(
                    "Hallo %s,\n\nSie haben über unsere Plattform match4healthcare von %s (%s) eine Antwort auf Ihre Anzeige bekommen.\n"
                    "Falls Sie keine Anfragen mehr bekommen möchten, deaktivieren Sie Ihre "
                    "Anzeige im Profil online.\n\n"
                    % (h.ansprechpartner, s.name_first, request.user.email)
                )
                message = (
                    start_text
                    + "===============================================\n\n"
                    + email_form.cleaned_data["message"]
                    + "\n\n===============================================\n\n"
                    + "Mit freundlichen Grüßen,\nIhr match4healthcare Team"
                )
                emailtohospital = EmailToHospital.objects.create(
                    student=s,
                    hospital=h,
                    message=email_form.cleaned_data["message"],
                    subject=email_form.cleaned_data["subject"],
                )

                email = EmailMessage(
                    subject="[match4healthcare] " + email_form.cleaned_data["subject"],
                    body=message,
                    from_email=settings.NOREPLY_MAIL,
                    to=[h.user.email],
                )
                email.send()
                emailtohospital.send_date = datetime.now()
                emailtohospital.save()

                return render(request, "hospital_contacted.html")

        return self.get(request, uuid)

    def get(self, request, uuid):
        h = get_object_or_404(Hospital, uuid=uuid)
        initial = {
            "subject": _("Neues Hilfsangebot"),
            "message": _(
                "Hallo, ich habe ihr Gesuche auf der Plattform match4healthcare gesehen und bin für die Stelle qualifiziert.\nIch bin...\nIch möchte helfen in dem..."
            ),
        }

        email_form = EmailToHospitalForm(initial=initial)

        lat1, lon1, ort1 = plzs[h.countrycode][h.plz]

        context = {
            "hospital": h,
            "uuid": h.uuid,
            "ort": ort1,
            "mail": h.user.username,
        }

        if request.user.is_student:
            s = Student.objects.get(user=request.user)
            lat2, lon2, context["student_ort"] = plzs[s.countrycode][s.plz]
            context["distance"] = int(haversine(lon1, lat1, lon2, lat2))
            context["plz_student"] = s.plz

        context["email_form"] = email_form

        return render(request, "hospital_view.html", context)
