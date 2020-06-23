from django import forms


class AvailabilityForm(forms.Form):

    start_date = forms.DateField(required=True)
    # start_time = forms.TimeField(required=True)
    end_date = forms.DateField(required=True)
    # end_time = forms.TimeField(required=True)


class EnquiryForm(forms.Form):
    phone_num = forms.IntegerField(required=True)
    # phone_num = forms.CharField(max_length=10, required=True)
    Firstname = forms.CharField(max_length=50, required=True)
    Lastname = forms.CharField(max_length=50, required=False)
    start_date = forms.DateField(required=True)
    end_date = forms.DateField(required=True)
    # email = forms.CharField(max_length=255, required=False)
    email = forms.EmailField(max_length=255, required=False)
