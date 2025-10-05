from django.db import models
from django.contrib.auth.models import User

class University(models.Model):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('name', 'country')  # prevent duplicate entries

    def __str__(self):
        return f"{self.name} ({self.country})"

class FavoriteUniversity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='favorited_by')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'university')  # prevent duplicates

    def __str__(self):
        return f"{self.user.username} - {self.university.name}"
