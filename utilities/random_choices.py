from random import randint


class ChoiceRandomization:
    _choices = [True, False]
    choice_one = None
    choice_two = None
    choice_three = None

    def __init__(self):
        choices = self._choice_check()
        self.choice_one = choices[0]
        self.choice_two = choices[1]
        self.choice_three = choices[2]

    def _choice_check(self):
        self._make_choice()

        if self.choice_one is self.choice_two is self.choice_three:
            return self._choice_check()

        return [self.choice_one, self.choice_two, self.choice_three]

    def _make_choice(self):
        self.choice_one = self._choices[randint(0, 1)]
        self.choice_two = self._choices[randint(0, 1)]
        self.choice_three = self._choices[randint(0, 1)]
