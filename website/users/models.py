from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin
from django.core.validators import RegexValidator

from django.contrib.gis.db import models as gismodels
from django.contrib.gis.geos import Point


class UserManager(BaseUserManager):

    def create_user(self, phone_number, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not phone_number:
            raise ValueError('User must have a phone number')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, phone_number, password):
        """Creates and saves a new superuser"""
        user = self.create_user(phone_number, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports phone_number instead of username"""
    phone_regex  = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=10, unique=True) # validators should be a list
    alternative_phone = models.CharField(validators=[phone_regex], max_length=10, blank=True, null=True)
    reference    = models.CharField(max_length=255, blank=True, null=True)
    alternative_phone = models.CharField(validators=[phone_regex], max_length=10, blank=True, null=True)
    reference_phone = models.CharField(validators=[phone_regex], max_length=10, blank=True, null=True)
    first_name   = gismodels.CharField(max_length=255)
    last_name    = gismodels.CharField(max_length=255, blank=True, null=True)
    email        = models.CharField(max_length=255, blank=True, null=True)

    ###################################################################################
    ac = 'Aadhaar card'
    dl = 'Driving licence'
    pn = 'Pan card'
    rc = 'RC book'
    ps = 'Passport'
    
    id_choices = (
        (rc, 'RC book'),
        (ps, 'Passport'),
        (dl, 'Driving licence'),
        (ac, 'Aadhaar card'),
        (pn, 'Pan card'),       
    )
    id_proof        = models.CharField(verbose_name="Id proof", choices=id_choices, max_length= 20, blank=True, null=True)
    id_proof_number = models.CharField(verbose_name='Id Proof number', max_length=20, blank=True, null=True)
    image           = models.ImageField(upload_to=None, height_field=300, width_field=300, max_length=500, blank=True, null=True)
    ###################################################################################
    
    address      = models.CharField(max_length=150, blank=True, null=True)
    city         = models.CharField(max_length=50, blank=True, null=True)
    location     = gismodels.PointField(blank=True, null=True)

    is_active    = gismodels.BooleanField(default=True)
    is_staff     = gismodels.BooleanField(default=False)

    date_created = models.DateTimeField(auto_now=True, editable=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
