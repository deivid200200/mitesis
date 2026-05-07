from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import PerfilUsuario


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=150, required=True, label="Nombres")
    last_name = forms.CharField(max_length=150, required=True, label="Apellidos")
    rol = forms.ChoiceField(
        choices=PerfilUsuario.ROLES_CHOICES,
        required=True,
        label="Rol del Usuario",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplicar clase Bootstrap a los campos de contraseña
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['class'] = 'form-control'
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email ya está registrado.")
        return email


class UsuarioEditarForm(forms.ModelForm):
    """Formulario para editar usuario - solo datos básicos"""
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active']
        labels = {
            'username': 'Nombre de Usuario',
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'email': 'Correo Electrónico',
            'is_active': 'Usuario Activo',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombres'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class PerfilUsuarioEditarForm(forms.ModelForm):
    """Formulario para editar perfil de usuario - solo rol y datos de perfil"""
    class Meta:
        model = PerfilUsuario
        fields = ['rol', 'numero_identidad', 'telefono', 'direccion', 'activo']
        labels = {
            'rol': 'Rol del Usuario',
            'numero_identidad': 'Número de Identidad',
            'telefono': 'Teléfono',
            'direccion': 'Dirección',
            'activo': 'Perfil Activo',
        }
        widgets = {
            'rol': forms.Select(attrs={'class': 'form-control'}),
            'numero_identidad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de identidad'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    

class PerfilUsuarioForm(forms.ModelForm):
    """Formulario para actualizar perfil de usuario"""
    first_name = forms.CharField(max_length=150, required=True, label="Nombres")
    last_name = forms.CharField(max_length=150, required=True, label="Apellidos")
    email = forms.EmailField(required=True)
    
    class Meta:
        model = PerfilUsuario
        fields = ['numero_identidad', 'telefono', 'direccion', 'foto']
        labels = {
            'numero_identidad': 'Número de Identidad',
            'telefono': 'Teléfono',
            'direccion': 'Dirección',
            'foto': 'Foto de Perfil',
        }
        widgets = {
            'numero_identidad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de identidad'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección'}),
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.usuario:
            self.fields['first_name'].initial = self.instance.usuario.first_name
            self.fields['last_name'].initial = self.instance.usuario.last_name
            self.fields['email'].initial = self.instance.usuario.email
        if self.instance.pk:
            self.fields['numero_identidad'].initial = self.instance.numero_identidad
            self.fields['telefono'].initial = self.instance.telefono
            self.fields['direccion'].initial = self.instance.direccion
            self.fields['foto'].initial = self.instance.foto
        
        # Aplicar estilos Bootstrap
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
    
    def save(self, commit=True):
        perfil = super().save(commit=False)
        perfil.usuario.first_name = self.cleaned_data['first_name']
        perfil.usuario.last_name = self.cleaned_data['last_name']
        perfil.usuario.email = self.cleaned_data['email']
        if commit:
            perfil.usuario.save()
            perfil.save()
        return perfil