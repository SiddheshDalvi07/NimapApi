from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError
class Client(models.Model):
    name = models.CharField(max_length=100, verbose_name='client_name')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='created_clients', on_delete=models.SET_NULL, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

class Project(models.Model):
    name = models.CharField(max_length=100, verbose_name='project_name')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='projects')
    users = models.ManyToManyField(User, related_name='assigned_projects')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='created_projects', on_delete=models.SET_NULL, null=True)

    def clean(self):
        if Project.objects.filter(name=self.name).exclude(client=self.client).exists():
            raise ValidationError(f"A project with the name '{self.name}' already exists for {self.client.name}.")

    def save(self, *args, **kwargs):
        self.full_clean() 
        super(Project, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
