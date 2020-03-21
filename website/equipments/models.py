from django.db import models

class Camera(models.Model):
    company     = models.CharField(max_length=50)
    model       = models.CharField(max_length=50)
    description = models.TextField()
    inventory   = models.IntegerField()
    ratings     = models.models.FloatField(min=1, max=5)

    def __str__(self):
        return '{} {}'.format(self.company, self.model)
    
    class Meta:
        verbose_name = "Camera"
        verbose_name_plural = "Cameras"

class Lens(models.Model):
    company     = models.CharField(max_length=50)
    model       = models.CharField(max_length=50)
    description = models.TextField()
    inventory   = models.IntegerField()
    ratings     = models.models.FloatField(min=1, max=5)

    def __str__(self):
        return '{} {}'.format(self.company, self.model)

    class Meta:
        verbose_name = "Lens"
        verbose_name_plural = "Lenses"

class Accessories(models.Model):
    company     = models.CharField(max_length=50)
    model       = models.CharField(max_length=50)
    name        = models.CharField(max_length=150)
    description = models.TextField()
    inventory   = models.IntegerField()
    ratings     = models.models.FloatField(min=1, max=5)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Accessories"
        verbose_name_plural = "Accessories"
