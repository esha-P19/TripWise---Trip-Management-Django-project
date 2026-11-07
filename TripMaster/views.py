from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from TripMaster.serializers import UserSerializer,TripSerializer
from django.contrib.auth.models import User
from TripMaster.models import TripDb
from rest_framework import permissions,authentication,serializers



# Create your views here.
class SignupView(APIView):
    def post(self,request):
        form_data = request.data
        serializer_instance = UserSerializer(data=form_data)

        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data={"msg":"user created..!"},status=201)
        else:
            return Response(data=serializer_instance.errors,status=400)

class TripListCreateView(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]


    def get(self,request):
        qs = TripDb.objects.filter(created_by = request.user)
        serializer_instance = TripSerializer(qs,many=True)
        return Response(data=serializer_instance.data,status=200)

    def post(self,request):
        form_data = request.data
        serializer_instance = TripSerializer(data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save(created_by=request.user)
            return Response(data={"msg":"trip created..",
                                  "trip":serializer_instance.data},status=201)
        else:
            return Response(data=serializer_instance.errors,status=400)

class TripRetrieveUpdateDeleteView(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request,pk):
        trip_object = get_object_or_404(TripDb,id=pk)
        if trip_object.created_by == request.user:
            serializer_instance = TripSerializer(trip_object)
            return Response(data=serializer_instance.data)

        else:
            raise serializers.ValidationError("you are not authorized to view this..!")

    def put(self,request,pk):
        trip_object = get_object_or_404(TripDb,id=pk)
        if trip_object.created_by != request.user:
            raise serializers.ValidationError("you cannot update this data")

        form_data = request.data
        serializer_instance = TripSerializer(data = form_data,instance = trip_object)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data={"message" : "Trip updated successfully..!",
                            "updated Trip Details" : serializer_instance.data})
        else:
            return Response(data=serializer_instance.errors)


    def delete(self,request,pk):
        trip_object = get_object_or_404(TripDb,id=pk)
        if trip_object.created_by == request.user:
            qs = TripDb.objects.filter(id=pk).delete()
            return Response(data={"msg" : "the trip is deleted"})
        else:
            raise serializers.ValidationError("you cannot delete this data")
