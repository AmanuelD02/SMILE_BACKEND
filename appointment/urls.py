from django.urls import path

from appointment.models import AppointmentMessage

from .views import AvailabilityView, AvailabiltyListView, AvailabilityDetailView \
               , PendingAppointmentView, PendingAppointmentListView,PendingAppointmentDetailView \
                , AppointmentView , AppointmentListView, AppointmentDetailView,AppointmentMessagView, \
                    GetAppointmentMessageView

urlpatterns = [
    path('available/', AvailabilityView.as_view()),
    path('available/list', AvailabiltyListView.as_view()),
    path('available/<int:available_id>/', AvailabilityDetailView.as_view()),
    path('pending/', PendingAppointmentView.as_view()),
    path('pending/list', PendingAppointmentListView.as_view()),
    path('pending/<int:pending_id>/', PendingAppointmentDetailView.as_view()),
    path('', AppointmentView.as_view()),
    path('list/',AppointmentListView.as_view()),
    path('<int:appointment_id>/',AppointmentDetailView.as_view()),
    path('message/',AppointmentMessagView.as_view()),
    path('message/list/', GetAppointmentMessageView.as_view())
]