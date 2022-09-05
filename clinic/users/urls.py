from django.contrib import admin
from django.urls import path

from .api import admin_all_appointmennts, admin_all_appointmennts_by_state,  update_appoint_state, user_all_appointmennts, user_all_appointmennts_by_state

from .views import activate, appointment_approved, appointment_cancel, appointment_canceld_by_admin, appointment_details, appointment_update, homepage, logout_user, signin_user, signup

app_name='users'
urlpatterns = [
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',  
        activate, name='activate'), 
    path('signup/', signup, name = 'signup'), 
    path('signin/', signin_user, name = 'signin'),
    path('logout/', logout_user, name = 'logout'),
    path('homepage/', homepage, name = 'homepage'),
    path('appointment_details/<int:id>', appointment_details, name = 'appointment_details'),
    path('appointment_cancel/<int:id>', appointment_cancel, name = 'appointment_cancel'),
    path('appointment_update/<int:id>', appointment_update, name = 'appointment_update'),
    path('appointment_approved/<int:id>', appointment_approved, name = 'appointment_approved'),
    path('appointment_canceld_by_admin/<int:id>', appointment_canceld_by_admin, name = 'appointment_canceld_by_admin'),
    path('api/appointments/admin',admin_all_appointmennts, name='admin_all_appointmennts'),
    path('api/appointments/admin/<slug:state>',admin_all_appointmennts_by_state, name='admin_all_appointmennts_by_state'),
    path('api/appointments/user',user_all_appointmennts, name='user_all_appointmennts'),
    path('api/appointments/user/<slug:state>',user_all_appointmennts_by_state, name='user_all_appointmennts_by_state'),
    path('api/appointments/update/<int:id>/',update_appoint_state, name='update_appoint_state'),
    
]