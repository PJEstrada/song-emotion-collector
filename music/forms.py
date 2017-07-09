import django.forms as forms
from music.models import Participant
from django_countries.widgets import CountrySelectWidget


class ParticipantForm(forms.ModelForm):
    """
        Participant form
    """

    class Meta:
        model = Participant
        fields = ('first_name',
                  'last_name',
                  'email',
                  'age',
                  'gender',
                  'scolarity',
                  'country',
                  'knows_music_theory',
                  'has_physical_problem',
                  'physical_problem',
                  'hearing_problem',
                  'has_psychological_problem',
                  'psychological_problem',
                  'has_hearing_problem')
        widgets = {'country': CountrySelectWidget()}

    def __init__(self, *args, **kwargs):
        super(ParticipantForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        self.fields['physical_problem'].widget.attrs['cols'] = 30
        self.fields['physical_problem'].widget.attrs['rows'] = 5
        self.fields['hearing_problem'].widget.attrs['cols'] = 30
        self.fields['hearing_problem'].widget.attrs['rows'] = 5
        self.fields['psychological_problem'].widget.attrs['cols'] = 30
        self.fields['psychological_problem'].widget.attrs['rows'] = 5