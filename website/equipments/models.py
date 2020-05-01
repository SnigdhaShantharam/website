from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from ckeditor.fields import RichTextField
# from PIL import Image

ratings = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
)
equipment_type = (
    ('Camera', 'Camera'),
    ('Lens', 'Lens'),
    ('Accessories', 'Accessories'),
)


class Equipment(models.Model):
    equipment_type  = models.CharField(max_length=20, choices=equipment_type)
    company         = models.CharField(max_length=50)
    model_name      = models.CharField(max_length=50)
    image           = models.ImageField(max_length=500, blank=True, null=True, upload_to="equipments")
    description     = RichTextField()
    count           = models.IntegerField()
    cost            = models.DecimalField(verbose_name='cost/day',max_digits=10, decimal_places=2)
    ratings         = models.IntegerField(choices=ratings)
    slug            = models.SlugField(default='', editable=False, max_length=100)

    def __str__(self):
        return '{} {}'.format(self.company, self.model_name)
    
    def get_absolute_url(self):
        kwargs = {
            'pk': self.pk,
            'slug': self.slug
        }
        return reverse('gadgets-pk-slug-detail', kwargs=kwargs)

    def save(self, *args, **kwargs):
        value = self.company + self.model_name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Equipment"
        verbose_name_plural = "Equipments"


# class Equipment_Images(models.Model):
#     equipment_key      = models.ForeignKey(Equipment, on_delete=models.CASCADE)
#     image           = models.ImageField(max_length=500, blank=True, null=True, upload_to="media/equipments")

#     class Meta:
#         verbose_name = "Images"
#         verbose_name_plural = "Images"
