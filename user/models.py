from django.core.validators import RegexValidator
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, UnicodeUsernameValidator, UserManager, \
    PermissionsMixin
from django.utils.translation import ugettext_lazy as _
# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_('email address'), blank=True)
    phone_number = models.CharField(_("phone number"), max_length=11, blank=True)
    avatar = models.ImageField(upload_to='users/avatat', blank=True)
    bio = models.TextField(_("bio"), blank=True)
    website = models.URLField(_("website"), blank=True)
    is_verified = models.BooleanField(_("is_verified"), default=False)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s ' % (self.username)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.username
