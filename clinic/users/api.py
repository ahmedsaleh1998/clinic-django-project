from rest_framework.decorators import api_view
from rest_framework.response import Response
from users.models import Appointments
from users.seralizers import AppointmentsSerializer
from rest_framework.response import Response
from django.contrib.auth.models import User  
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

#### admin to get all appointments##########
@permission_classes((IsAuthenticated, ))
@api_view(['GET'])
def admin_all_appointmennts(request):
  alldate=Appointments.objects.all()
  data = AppointmentsSerializer(alldate, many=True).data
  return Response({'data':data})
#### admin to get all appointments by state##########
@permission_classes((IsAuthenticated, ))
@api_view(['GET'])
def admin_all_appointmennts_by_state(request,state):
  alldate=Appointments.objects.filter(state=state)
  data = AppointmentsSerializer(alldate, many=True).data
  return Response({'data':data})
#### user to get all his appointments ##########
@permission_classes((IsAuthenticated, ))
@api_view(['GET'])
def user_all_appointmennts(request):
  alldate=Appointments.objects.filter(user=request.user)
  data = AppointmentsSerializer(alldate, many=True).data
  return Response({'data':data})

#### admin to get all his appointments by state##########
@permission_classes((IsAuthenticated, ))
@api_view(['GET'])
def user_all_appointmennts_by_state(request,state):
  alldate=Appointments.objects.filter(user=request.user,state=state)
  data = AppointmentsSerializer(alldate, many=True).data
  return Response({'data':data})
#### admin or user update state ##########
@permission_classes((IsAuthenticated, ))
@api_view(['POST'])
def update_appoint_state(request,id):
 if request.method=='POST':
    alldate=Appointments.objects.filter(id=id)[0]
    serializer = AppointmentsSerializer(alldate,request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'data':serializer.data})
    else:
      return Response({'msg':serializer.errors})
  