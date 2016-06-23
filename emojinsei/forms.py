from allauth.account.forms import SignupForm
class SignupFormWithoutAutofocus(SignupForm):

    def __init__(self, *args, **kwargs):
        super(SignupFormWithoutAutofocus, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.pop("autofocus", None)