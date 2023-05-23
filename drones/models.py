from django.db import models


class DroneCategory(models.Model):
    name = models.CharField(max_length=250, unique=True)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name


class Drone(models.Model):
    drone_category = models.ForeignKey(to=DroneCategory, related_name='drones', on_delete=models.CASCADE)
    name = models.CharField(max_length=250, unique=True)
    manufacturing_date = models.DateTimeField()
    has_it_competed = models.BooleanField(default=False)
    inserted_timestamp = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(to='auth.User', related_name='drones', on_delete=models.CASCADE)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Pilot(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICE = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )
    name = models.CharField(max_length=150, blank=False,     unique=True)
    gender = models.CharField(
        max_length=2,
        choices=GENDER_CHOICE,
        default=MALE,
    )
    races_count = models.IntegerField()
    inserted_timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Competition(models.Model):
    pilot = models.ForeignKey(to=Pilot, related_name='competitions', on_delete=models.CASCADE)
    drone = models.ForeignKey(to=Drone, on_delete=models.CASCADE)
    distance_in_feet = models.IntegerField()
    distance_achievement_date = models.DateTimeField()

    class Meta:
        ordering = ('-distance_in_feet',)
