from django_filters import AllValuesFilter, DateTimeFilter, NumberFilter, FilterSet
from django_filters import rest_framework as filters
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
from drones.models import DroneCategory, Drone, Pilot, Competition
from drones.serializers import DroneCategorySerializer, DroneSerializer, \
    PilotSerializer, PilotCompetitionSerializer
from rest_framework import permissions
from drones import custompermission


class DroneCategoryList(generics.ListCreateAPIView):
    queryset = DroneCategory.objects.all()
    serializer_class = DroneCategorySerializer
    name = 'dronecategory-list'
    filterset_fields = (
        'name',
    )
    search_fields = (
        '^name',
    )
    ordering_fields = (
        'name',
    )


class DroneCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DroneCategory.objects.all()
    serializer_class = DroneCategorySerializer
    name = 'dronecategory-detail'


class DroneList(generics.ListCreateAPIView):
    queryset = Drone.objects.all()
    serializer_class = DroneSerializer
    name = 'drone-list'
    filterset_fields = ('name', 'drone_category', 'manufacturing_date', 'has_it_competed', )
    search_fields = ('^name', )
    ordering_fields = ('name', 'manufacturing_date', )
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, custompermission.IsCurrentUserOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class DroneDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Drone.objects.all()
    serializer_class = DroneSerializer
    name = 'drone-detail'
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, custompermission.IsCurrentUserOwnerOrReadOnly)


class PilotList(generics.ListCreateAPIView):
    queryset = Pilot.objects.all()
    serializer_class = PilotSerializer
    name = 'pilot-list'
    filterset_fields = ('name', 'gender', 'races_count', )
    search_fields = ('^name', )
    ordering_fields = ('name', 'races_count', )


class PilotDetail(generics.ListCreateAPIView):
    queryset = Pilot.objects.all()
    serializer_class = PilotSerializer
    name = 'pilot-detail'


class CompetitionFilter(filters.FilterSet):
    from_achievement_date = DateTimeFilter(
        field_name='distance_achievement_date', lookup_expr='gte')
    to_achievement_date = DateTimeFilter(
        field_name='distance_achievement_date', lookup_expr='lte')
    min_distance_in_feet = NumberFilter(
        field_name='distance_in_feet', lookup_expr='gte')
    max_distance_in_feet = NumberFilter(
        field_name='distance_in_feet', lookup_expr='lte')
    drone_name = AllValuesFilter(
        field_name='drone__name')
    pilot_name = AllValuesFilter(
        field_name='pilot__name')

    class Meta:
        model = Competition
        fields = (
            'distance_in_feet',
            'from_achievement_date',
            'to_achievement_date',
            'min_distance_in_feet',
            'max_distance_in_feet',
            # drone__name will be accessed as drone_name
            'drone_name',
            # pilot__name will be accessed as pilot_name
            'pilot_name',
            )


class CompetitionList(generics.ListCreateAPIView):
    queryset = Competition.objects.all()
    serializer_class = PilotCompetitionSerializer
    name = 'competition-list'
    filterset_class = CompetitionFilter
    ordering_fields = ('distance_in_feet', 'distance_achievement_date', )


class CompetitionDetail(generics.ListCreateAPIView):
    queryset = Competition.objects.all()
    serializer_class = PilotCompetitionSerializer
    name = 'competition-detail'


class ApiRoot(generics.GenericAPIView):
    name = 'api-root'
    
    def get(self, request, *args, **kwargs):
        return Response({
            'drone-categories': reverse(DroneCategoryList.name, request=request),
            'drones': reverse(DroneList.name, request=request),
            'pilots': reverse(PilotList.name, request=request),
            'competitions': reverse(CompetitionList.name, request=request),
        })
