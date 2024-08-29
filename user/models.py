from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MinLengthValidator, RegexValidator, EmailValidator
from django.core.exceptions import ValidationError
import re
import smtplib
import dns.resolver

# Create your models here.

HUNTER_API_KEY = 'fd385c8af6de8303f9cc61be05a3f1784c38e3c0'

class UserManager(BaseUserManager):
    def create_user(self, dni, first_name, last_name, email, numer_phone, password=None, **extra_fields):
        if not dni:
            raise ValueError('El usuario debe tener un DNI')
        if not first_name:
            raise ValueError('El usuario debe tener un Nombre')
        if not last_name:
            raise ValueError('El usuario debe tener un Apellido')
        if not email:
            raise ValueError('El usuario debe tener un Correo')
        if not numer_phone:
            raise ValueError('El usuario debe tener un Número de Teléfono')

        user = self.model(dni=dni, first_name=first_name, last_name=last_name, email=email, numer_phone=numer_phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, dni, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(dni, password=password, **extra_fields)

class User(AbstractBaseUser):
    dni = models.CharField(max_length=8, unique=True, primary_key=True, validators=[RegexValidator(regex=r'^\d{8}$', message='El DNI debe contener 8 dígitos')])
    first_name = models.CharField(max_length=30, null=False, validators=[MinLengthValidator(3, message='El nombre debe tener al menos 3 letras.'), RegexValidator(regex=r'^[a-zA-Z]+$', message='El nombre solo puede contener letras.')])
    last_name = models.CharField(max_length=30, null=False, validators=[MinLengthValidator(3, message='El apellido debe tener al menos 3 letras.'), RegexValidator(regex=r'^[a-zA-Z]+$', message='El apellido solo puede contener letras.')])
    email = models.EmailField(unique=True, null=False, validators=[EmailValidator(message='Ingrese un correo electrónico válido')])
    numer_phone = models.CharField(max_length=13, unique=True, null=False, validators=[RegexValidator(regex=r'^\+54\d{10}$', message='El teléfono debe contener 10 dígitos después del prefijo +54')], default='+54')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['dni', 'first_name', 'last_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.dni})'
    
    
    def clean_email(self):
        email = self.email
        # Aquí puedes agregar validaciones personalizadas, por ejemplo:
        if not email.endswith('@gmail.com'):
            raise ValidationError('El email debe ser un correo de Google.')
        return email
    
    def clean(self):
        self.clean_email()
        self.validate_google_email(self.email)
        self.verify_email_exists(self.email)
        super().clean()

    def validate_google_email(self, email):
        # Validar que el email sea de un dominio de Google
        if not re.match(r'^[a-zA-Z0-9_.+-]+@(?:gmail\.com|googlemail\.com)$', email):
            raise ValidationError("El correo debe ser de Google (gmail.com o googlemail.com).")

    def verify_email_exists(self, email):
        domain = email.split('@')[1]
        try:
            # Consultar el registro MX del dominio
            records = dns.resolver.resolve(domain, 'MX')
            mx_record = str(records[0].exchange)
            
            # Conectar al servidor de correo para verificar la existencia del email
            server = smtplib.SMTP()
            server.connect(mx_record)
            server.helo(server.local_hostname)
            server.mail('test@example.com')
            code, _ = server.rcpt(email)
            server.quit()
            
            if code != 250:
                raise ValidationError("El correo no existe.")
        except Exception as e:
            raise ValidationError(f"Error en la verificación del correo: {e}")



