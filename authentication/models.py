from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,PermissionsMixin,BaseUserManager)
from helpers.models import TrackingModel
from django.contrib.auth.validators import UnicodeUsernameValidator

from todolistapi.settings import SECRET_KEY
from .managers import MyUserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import jwt
from django.conf import settings
from datetime import datetime, timedelta
# Create your models here.
class User(AbstractBaseUser, PermissionsMixin,TrackingModel):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username and password are required. Other fields are optional.
    """

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_("email address"), blank=False,unique=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    email_verified=models.BooleanField(
        _("email_verified"),
        default=False,
        help_text=_(
            "Designates whether this user is verified "
        ),
    )
    objects = MyUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    
    @property
    def token(self):
        token=jwt.encode({'username':self.username,
        'email':self.email,
        'exp':datetime.utcnow()+timedelta(hours=24)},
        settings.SECRET_KEY,algorithm='HS256' )

        return token