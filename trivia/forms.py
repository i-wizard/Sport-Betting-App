from django import forms
from django.utils import timezone

from trivia.models import Question


class QuestionForm(forms.ModelForm):
    closed_at = forms.CharField(required=False)

    class Meta:
        model = Question
        fields = ('team_a', 'team_b', 'closed_at')

    def clean_closed_at(self):
        closed_at = self.cleaned_data.get('closed_at')

        try:
            closed_at = int(closed_at)
        except ValueError:
            raise forms.ValidationError('Enter valid duration')

        if closed_at < 1:
            raise forms.ValidationError('Entry duration must be at least 1 hour from now')

        return timezone.now() + timezone.timedelta(hours=closed_at)


class ResultQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = (
            'team_a_score', 'team_b_score', 'total_corner_kicks', 'total_cards', 'status'
        )
