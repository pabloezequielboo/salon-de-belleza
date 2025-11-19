from django import forms


class ContactForm(forms.Form):
    """
    Formulario de contacto simple.

    Este formulario se puede usar en una página de contacto para que los
    usuarios envíen consultas. Los widgets incluyen clases CSS para integrarse
    con el estilo del proyecto (`static/css/style.css`).
    """
    name = forms.CharField(
        label='Nombre',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu nombre completo'})
    )
    email = forms.EmailField(
        label='Correo Electrónico',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'tu@email.com'})
    )
    message = forms.CharField(
        label='Mensaje',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Escribe tu consulta aquí...'})
    )
