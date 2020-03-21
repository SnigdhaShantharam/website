from django.db import models

ratings = (
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
)
class Camera(models.Model):
    company = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    description = models.TextField()
    inventory = models.IntegerField()
    ratings = models.IntegerField(choices=ratings)
    image1 = models.ImageField(max_length=500, blank=True, null=True, upload_to="media/equipments")
    image2 = models.ImageField(max_length=500, blank=True, null=True, upload_to="media/equipments")
    image3 = models.ImageField(max_length=500, blank=True, null=True, upload_to="media/equipments")
    image4 = models.ImageField(max_length=500, blank=True, null=True, upload_to="media/equipments")

def __str__(self):
    return '{} {}'.format(self.company, self.model)
    class Meta:
        verbose_name = "Camera"
        verbose_name_plural = "Cameras"

class Lens(models.Model):
    company = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    description = models.TextField()
    inventory = models.IntegerField()
    ratings = models.IntegerField(choices=ratings)
    image1 = models.ImageField(max_length=500, blank=True, null=True, upload_to="media/equipments")
    image2 = models.ImageField(max_length=500, blank=True, null=True, upload_to="media/equipments")
    image3 = models.ImageField(max_length=500, blank=True, null=True, upload_to="media/equipments")
    image4 = models.ImageField(max_length=500, blank=True, null=True, upload_to="media/equipments")
    
    def __str__(self):
        return '{} {}'.format(self.company, self.model)

    class Meta:
        verbose_name = "Lens"
        verbose_name_plural = "Lenses"

class Accessories(models.Model):
    company = models.CharField(max_length=50)
    name = models.CharField(max_length=150)
    description = models.TextField()
    inventory = models.IntegerField()
    ratings = models.IntegerField(choices=ratings)
    image1 = models.ImageField(max_length=500, blank=True, null=True, upload_to="media/equipments")
    image2 = models.ImageField(max_length=500)