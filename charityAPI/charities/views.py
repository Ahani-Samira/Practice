from django.utils.log import request_logger
from rest_framework import status, generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsCharityOwner, IsBenefactor
from charities.models import Task, Benefactor
from charities.serializers import (
    TaskSerializer, CharitySerializer, BenefactorSerializer
)


class BenefactorRegistration(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BenefactorSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CharityRegistration(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CharitySerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class Tasks(generics.ListCreateAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.all_related_tasks_to_user(self.request.user)

    def post(self, request, *args, **kwargs):
        data = {
            **request.data,
            "charity_id": request.user.charity.id
        }
        serializer = self.serializer_class(data = data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data, status = status.HTTP_201_CREATED)

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            self.permission_classes = [IsAuthenticated, ]
        else:
            self.permission_classes = [IsCharityOwner, ]

        return [permission() for permission in self.permission_classes]

    def filter_queryset(self, queryset):
        filter_lookups = {}
        for name, value in Task.filtering_lookups:
            param = self.request.GET.get(value)
            if param:
                filter_lookups[name] = param
        exclude_lookups = {}
        for name, value in Task.excluding_lookups:
            param = self.request.GET.get(value)
            if param:
                exclude_lookups[name] = param

        return queryset.filter(**filter_lookups).exclude(**exclude_lookups)


class TaskRequest(APIView):
    permission_classes = (IsBenefactor,)

    def get(self,request, task_id ):
        task = get_object_or_404(Task, pk=task_id)
        if task.state is not 'P':
            data = {'detail': 'This task is not pending.'}
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        benefactor = get_object_or_404(Benefactor, user=request.user)
        task.assign_to_benefactor(benefactor)
        data = {'detail': 'Request sent.'}
        return Response(data, status=status.HTTP_200_OK)


class TaskResponse(APIView):
    permission_classes = (IsCharityOwner,)

    def post(self, request, task_id):
        task = get_object_or_404(Task, pk=task_id)
        ch_response = request.data['response']
        if ch_response != 'A' and ch_response != 'R':
            data = {'detail': 'Required field ("A" for accepted / "R" for rejected)'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        if task.state is not 'W':
            data = {'detail': 'This task is not waiting.'}
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        task.response_to_benefactor_request(ch_response)
        data={'detail': 'Response sent.'}
        return Response(data, status=status.HTTP_200_OK)


class DoneTask(APIView):
    pass