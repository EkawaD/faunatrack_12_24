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
    quantite = forms.IntegerField(
        label="Quantité",
        min_value=1,
        max_value=3000
    )

    def clean_quantite(self):
        quantite = self.cleaned_data.get("quantite")
        if quantite <= 0 or quantite > 1000:
            raise forms.ValidationError("Vous devez avoir observé au moins 1 individu et pas plus de 1000!")
        return quantite # Forgetting this leads to forms errors !

        
    
class ProjetForm(FaunatrackForm):
    class Meta:
        model = Projet
        fields = "__all__"