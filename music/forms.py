import django.forms as forms
from music.models import Participant


class ParticipantForm(forms.ModelForm):
    """
        Participant form
    """

    class Meta:
        model = Participant
        fields = ('first_name',
                  'last_name',
                  'age',
                  'gender')

