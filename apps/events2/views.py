from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from apps.events.models import Event



class EventsList(ListView):
    model = Event
    template_name = "events_list.html"
    context_object_name = "events"
    ordering = ["date", "start_time"]


class EventDetail(LoginRequiredMixin, DetailView):
    model = Event
    template_name = "events/event_detail.html"
    context_object_name = "event"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.get_object()
        participant = self.request.user
        context["is_participant"] = event.participants.filter(
            id=participant.id
        ).exists()
        return context