from django.db import models
from django.contrib.auth.models import  BaseUserManager, AbstractBaseUser

# here we make the user_manager
class UserManager(BaseUserManager):
    def create_user(self, email, name,term_condition, password=None,password2=None):
        """
        Creates and saves a User with the given email, name,term_condition  and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            term_condition=term_condition
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name,term_condition, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
            term_condition=term_condition,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user




# create a my user

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='EMAIL',
        max_length=255,
        unique=True,
    )
    name=models.CharField(max_length=200)
    term_condition=models.BooleanField()
    is_active = models.BooleanField(default=True) # this is use for to check the user is active or not 
    is_admin = models.BooleanField(default=False) # this is use for to not make admin 
    # here we make two another object which show the time and date like created at or updated at 
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','term_condition'] # this is required fields means user enter it by hook or crook 

    def __str__(self):
        return self.email
    # these three are different function which type of  permission  are given to the user 
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin