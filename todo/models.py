from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def get_tasks(self):
        return self.task_set.all()

    def count_complited_tasks(self):
        return self.task_set.filter(checked=True).count()

# Мы используем данный сигнал, который автоматически сохраняет изменения в модели Profile при изменении модели User
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Task(models.Model):
    title = models.CharField(max_length=50)
    body = models.CharField(max_length=500)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    checked = models.BooleanField(default=False)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)

    class Meta():
        ordering = ['checked', 'title']

    def change_complite_state(self):
        """Изменяет состояние выполненности задания"""
        if self.checked:
            self.checked = False
        else:
            self.checked = True
        self.save()

    def __str_(self):
        return f'<Task {self.title}>'

class Category(models.Model):
    title = models.CharField(max_length=50)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True)

    def get_absolute_url(self):
        return f'/?cat={self.id}'

    def __str__(self):
        return f'{self.title}'
