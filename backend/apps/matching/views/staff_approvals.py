import logging

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.utils.text import format_lazy
from django.utils.translation import gettext as _
from django.views import View
from django_tables2.config import RequestConfig

from apps.matching.models import Participant
from apps.matching.tables import ApproveParticipantTable

logger = logging.getLogger(__name__)


@method_decorator([login_required, staff_member_required(login_url="404")], name="dispatch")
class ApproveParticipantsView(View):
    template_name = "approve_hospitals.html"

    def get(self, request, p_type):
        # If you are not a staff user, the method decorator takes care of showing a 404 page,
        # so if you are a staff user, we throw a 403 here with an error message
        if not (
            request.user.has_perm("matching.can_approve_type_%s" % p_type.lower())
            or request.user.has_perm("matching.delete_participant%s" % p_type.lower())
        ):
            raise PermissionDenied("You currently don't have the permission to access this page")

        table_approved = ApproveParticipantTable[p_type](
            Participant[p_type].objects.filter(is_approved=True)
        )
        table_approved.prefix = "approved"
        RequestConfig(
            request,
            paginate={"page": request.GET.get(table_approved.prefix + "page", 1), "per_page": 5},
        ).configure(table_approved)

        # table_approved.paginate(page=request.GET.get(table_approved.prefix + "page", 1), per_page=5)

        table_unapproved = ApproveParticipantTable[p_type](
            Participant[p_type].objects.filter(is_approved=False)
        )
        table_unapproved.prefix = "unapproved"
        RequestConfig(
            request,
            paginate={"page": request.GET.get(table_unapproved.prefix + "page", 1), "per_page": 5},
        ).configure(table_unapproved)

        return render(
            request,
            "staff/approve_participants.html",
            {
                "table_approved": table_approved,
                "table_unapproved": table_unapproved,
                "p_type": p_type,
            },
        )

    def post(self, request, *args, **kwargs):
        post_params = self.request.POST
        p_type = self.kwargs["p_type"]
        if "delete" in post_params:
            if not request.user.has_perm("matching.delete_participant%s" % p_type.lower()):
                raise PermissionDenied(
                    "You currently don't have the permission to delete %s type of users" % p_type
                )
            p = get_object_or_404(Participant[p_type], uuid=post_params["uuid"])
            name = p.user
            p.user.delete()
            text = format_lazy(_("You deleted the participant with email '{name}'."), name=name)
            messages.add_message(self.request, messages.INFO, text)
        elif "change_approval" in post_params:
            if not request.user.has_perm("matching.can_approve_type_%s" % p_type.lower()):
                raise PermissionDenied(
                    "You currently don't have the permission to approve %s type of users" % p_type
                )
            p = get_object_or_404(Participant[p_type], uuid=post_params["uuid"])
            p.change_approval(self.request.user)
            name = p.user
            text = format_lazy(
                _("You changed the approval of the participant with email '{name}'."), name=name
            )
            messages.add_message(self.request, messages.INFO, text)
        return self.get(request, p_type)
