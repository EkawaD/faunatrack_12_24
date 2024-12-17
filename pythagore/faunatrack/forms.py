from django import forms

from faunatrack.models import Observation, Projet

class FaunatrackForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(FaunatrackForm, self).__init__(*args, **kwargs)
        for visible_field in self.visible_fields():
            visible_field.field.widget.attrs["class"] = "border w-full p-2 rounded-lg focus:ring-blue-500 focus:border-blue-500"


class ObservationForm(FaunatrackForm):
    class Meta:
        model = Observation
        fields = "__all__"
        widgets = {
            "date_observation":  forms.widgets.DateInput(
                attrs = {
                    'type': 'date'
                }
            )
        }

    
class ProjetForm(FaunatrackForm):
    class Meta:
        model = Projet
        fields = "__all__"