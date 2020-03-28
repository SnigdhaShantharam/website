from django.db import models

# from PIL import Image

ratings = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
)
class Camera(models.Model):
    company         = models.CharField(max_length=50)
    model_name      = models.CharField(max_length=50)
    description     = models.TextField()
    inventory       = models.IntegerField()
    ratings         = models.IntegerField(choices=ratings)

    def __str__(self):
        return '{} {}'.format(self.company, self.model_name)

    class Meta:
        verbose_name = "Camera"
        verbose_name_plural = "Cameras"


class Lens(models.Model):
    company         = models.CharField(max_length=50)
    model_name      = models.CharField(max_length=50)
    description     = models.TextField()
    inventory       = models.IntegerField()
    ratings         = models.IntegerField(choices=ratings)
    
    def __str__(self):
        return '{} {}'.format(self.company, self.model_name)

    class Meta:
        verbose_name = "Lens"
        verbose_name_plural = "Lenses"


class Accessories(models.Model):
    company         = models.CharField(max_length=50)
    model_name      = models.CharField(max_length=50)
    name            = models.CharField(max_length=150)
    description     = models.TextField()
    inventory       = models.IntegerField()
    ratings         = models.IntegerField(choices=ratings)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Accessories"
        verbose_name_plural = "Accessories"


class Equipments(models.Model):
    camera_key      = models.ForeignKey(Camera, on_delete=models.CASCADE, null=True, blank=True)
    lens_key        = models.ForeignKey(Lens, on_delete=models.CASCADE, null=True, blank=True)
    accessories_key = models.ForeignKey(Accessories, on_delete=models.CASCADE, null=True, blank=True)
    image           = models.ImageField(max_length=500, blank=True, null=True, upload_to="media/equipments")

    class Meta:
        verbose_name = "Equipments"
        verbose_name_plural = "Equipments"
