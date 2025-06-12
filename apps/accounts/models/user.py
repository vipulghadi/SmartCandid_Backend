from django.db import models
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
import uuid
import random
import string
import pytz
from django.core.exceptions import ValidationError
from django.conf import settings

from apps.core.models import TimeAuditModel
class UserManager(BaseUserManager):
    """Manager for the custom User model."""
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

def validate_timezone(value):
    if value not in pytz.all_timezones:
        raise ValidationError(f"{value} is not a valid timezone")

LOGIN_METHOD_CHOICES = [
    ('email', 'Email'),
    ('google', 'Google'),
    ('facebook', 'Facebook'),
]

class User(AbstractBaseUser, PermissionsMixin ):
    """Custom user model with email as the unique identifier."""
    
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, editable=False, db_index=True, primary_key=True
    )
    # user fields
    mobile_number = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True)
    # identity
    display_name = models.CharField(max_length=255, default="")
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    
    login_medium = models.CharField(
        max_length=50, 
        choices=LOGIN_METHOD_CHOICES, 
        default='email')
    extra_info=models.JSONField(default=dict)
    
    # tracking metrics
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Modified At")
    created_location = models.CharField(max_length=255, blank=True)
    
    # the is' es
    is_superuser = models.BooleanField(default=False)
    is_managed = models.BooleanField(default=False)
    is_password_expired = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    is_password_autoset = models.BooleanField(default=False)
    is_mobile_verified = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_online=models.BooleanField(default=False)
    
    # random token generated
    token = models.CharField(max_length=64, blank=True)
    
    #last activity
    last_location = models.CharField(max_length=255, blank=True)
    last_active = models.DateTimeField(default=timezone.now)
    last_login_time = models.DateTimeField(null=True)
    last_logout_time = models.DateTimeField(null=True)
    last_login_ip = models.CharField(max_length=255, blank=True)
    last_logout_ip = models.CharField(max_length=255, blank=True)
    last_login_medium = models.CharField(max_length=20, default="email",choices=LOGIN_METHOD_CHOICES)
    last_login_uagent = models.TextField(blank=True)
    token_updated_at = models.DateTimeField(null=True)
    
    #terms and conditions
    accepted_terms = models.BooleanField(default=False)
    accepted_terms_at = models.DateTimeField(null=True)
    accepted_conditions = models.BooleanField(default=False)
    accepted_conditions_at = models.DateTimeField(null=True)
    
    #onboarding
    is_web_onboarded = models.BooleanField(default=False)
    web_onboarding_step = models.JSONField(default=dict)
    is_mobile_onboarded = models.BooleanField(default=False)
    mobile_onboarding_step = models.JSONField(default=dict)
    mobile_timezone_auto_set = models.BooleanField(default=False)

    user_timezone = models.CharField(
    max_length=255, 
    default="UTC", 
    validators=[validate_timezone]
)

    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    class    Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['-date_joined']
        db_table = 'users'
        indexes = [
        models.Index(fields=['email']),
        models.Index(fields=['token']),
        models.Index(fields=['is_active']),
    ]
    def __str__(self):
        return self.email
    
    @property
    def fullname(self):
        return f"{self.first_name or ''} {self.last_name or ''}".strip()
    def generate_token(self):
        self.token = uuid.uuid4().hex + uuid.uuid4().hex
        self.token_updated_at = timezone.now()
        self.save()
    def save(self, *args, **kwargs):
        self.email = self.email.lower().strip()
        self.mobile_number = self.mobile_number.strip() if self.mobile_number else None

        if not self.token or self.token_updated_at:  
            self.token = uuid.uuid4().hex + uuid.uuid4().hex
            self.token_updated_at = timezone.now()

        if not self.display_name:
            self.display_name = self.email.split("@")[0]  
    

        if self.is_superuser:
            self.is_staff = True

        super(User, self).save(*args, **kwargs)
        
        
def user_profile_picture_upload_path(inst,filename):
    return f'user_{inst.user.id}/profile/{filename}'
class UserProfile(TimeAuditModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(
        upload_to=user_profile_picture_upload_path, 
        blank=True, null=True)
    follower_count = models.PositiveIntegerField(default=0)
    following_count = models.PositiveIntegerField(default=0)
    social_links=models.JSONField(default=dict, blank=True)
    is_private_account=models.BooleanField(default=True)
    achievements=models.JSONField(default=list)
    professions=models.JSONField(blank=True, default=list)
    stripe_customer_id = models.CharField(max_length=100, blank=True, null=True) 
    stripe_account_id = models.CharField(max_length=100, blank=True, null=True)   


    def __str__(self):
        return self.user.email if self.user else "No User"
    class Meta:
        verbose_name = "UserProfile"
        verbose_name_plural = "User Profiles"
        db_table = "user_profiles"
        ordering = ("-created_at",)
    