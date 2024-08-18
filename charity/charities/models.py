from django.db import models
from accounts.models import User


class Benefactor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    experience = models.SmallIntegerField(
        choices=[
            (0, 'Beginner'),
            (1, 'Average'),
            (2, 'Expert'),
        ],
        default=0
    )
    free_time_per_week = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f"Benefactor: {self.user.username}"


class Charity(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    reg_number = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class TaskManager(models.Manager):
    def related_tasks_to_charity(self, user):
        user_charity = list(Charity.objects.filter(user=user))
        if user_charity:
            return super().get_queryset().filter(charity=user_charity[0])
        return Charity.objects.none()

    def related_tasks_to_benefactor(self, user):
        user_benefactor = list(Benefactor.objects.filter(user=user))
        if user_benefactor :
            return super().get_queryset().filter(assigned_benefactor=user_benefactor[0])
        return Benefactor.objects.none()

    def all_related_tasks_to_user(self, user):
        user_charity = list(Charity.objects.filter(user=user))
        qs1 = super().get_queryset().filter(charity=user_charity[0])
        user_benefactor = list(Benefactor.objects.filter(user=user))
        qs2 = super().get_queryset().filter(assigned_benefactor=user_benefactor[0])
        qs3 = super().get_queryset().filter(state='P')
        return qs1 | qs2 | qs3


class Task(models.Model):
    assigned_benefactor = models.ForeignKey(Benefactor, on_delete=models.SET_NULL, null=True)
    charity = models.ForeignKey(Charity, on_delete=models.CASCADE)
    age_limit_from = models.IntegerField(blank=True, null=True)
    age_limit_to = models.IntegerField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    gender_limit = models.CharField(
        max_length=1,
        blank=True,
        null=True,
        choices=[
            ('M', 'Male'),
            ('F', 'Female'),
        ])
    state = models.CharField(
        max_length=1,
        choices=[
            ('P', 'Pending'),
            ('W', 'Waiting'),
            ('A', 'Assigned'),
            ('D', 'Done'),
        ],
        default='P'
    )
    title = models.CharField(max_length=60)
    objects = TaskManager()

    def __str__(self):
        return self.title
