from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from shiksha.models import User,CollegeUser,College,Course,Admission

class RegisterUserForm(forms.ModelForm):
    password1=forms.CharField(widget=forms.PasswordInput)
    password2=forms.CharField(label="Confirm Password",widget=forms.PasswordInput)
    fullname=forms.CharField()

    class Meta:
        model=User
        fields=("email",)
    def clean_email(self):
        email=self.cleaned_data.get('email')
        qs=User.objects.filter(email=email)
        if qs.exists():
            raise ValueError("Email already exists!")
        return email
    def clean_password(self):
        password1=self.cleaned_data.get('password1')
        password2=self.cleaned_data.get('password2')
        if password1 and password2 and password1!=password2:
            raise ValueError("Passwords didn't match!")
        return password2

class UserAdminCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)


    class Meta:
        model = User
        fields = ('email','first_name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['first_name'].label="Full Name"

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserAdminChangeForm(forms.ModelForm):
    password=ReadOnlyPasswordHashField()

    class Meta:
        model=User
        fields=("email","password","is_active","is_superuser")
    def clean_password(self):
        return self.initial["password"]

class CollegeRegisterer(forms.ModelForm):
    pincode=forms.CharField(widget=forms.NumberInput)
    phone_no=forms.CharField(widget=forms.NumberInput)
    consent=forms.CharField(label="Yes, I have read and provide my consent for my data to be processed for the purposes as mentioned in the Privacy Policy and the  Terms and Conditions",widget=forms.CheckboxInput)
    class Meta:
        model=CollegeUser
        fields=('college_name','contact_name','contact_address','city','state','country')

    def clean_pincode(self):
        pin=self.cleaned_data.get('pincode')
        if len(str(pin))!=6:
            raise ValueError("Invalid pincode")
        return pin
    def clean_phone_no(self):
        phone = self.cleaned_data.get('phone_no')
        if len(str(phone))!=10:
            raise ValueError("Invalid phone number")
        return phone
    def save(self, commit=True):
        user = super(CollegeRegisterer, self).save(commit=False)
        user.pincode=self.cleaned_data.get("pincode")
        user.phone_no= self.cleaned_data.get("phone_no")
        user.consent=self.cleaned_data.get("consent")
        if commit:
            user.save()
        return user

class CollegeForm(forms.ModelForm):
    msg={
        'max_length':'Incorrect pincode',
        'min_length':'Incorrect pincode'
    }
    yrmsg={
        'max_length':'Invalid year',
        'min_length':'Invalid year'
    }
    pincode = forms.CharField(widget=forms.NumberInput,max_length=6,min_length=6,error_messages=msg)
    clg_contactno = forms.CharField(label="College contact no",widget=forms.NumberInput)
    year=forms.CharField(label="Year of Establishment",widget=forms.NumberInput,max_length=4,min_length=4,error_messages=yrmsg)
    class Meta:
        model=College
        fields=("clg_name","clg_mail","clg_address","city","state","nirf","ownership")
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['clg_name'].label="College Name"
        self.fields['clg_mail'].label="College Mail"
        self.fields['clg_address'].label="College Location"
        self.fields['nirf'].label="NIRF Ranking"
        self.fields['ownership'].label="Ownership"

    def clean_name(self):
        clg_name=self.cleaned_data.get('clg_name')
        a=College.objects.filter(clg_name=clg_name)
        addr=a.clg_address
        if a and addr:
            raise ValueError("Repeated College details")
        return a
    def save(self, commit=True):
        clg= super(CollegeForm, self).save(commit=False)
        clg.pincode=self.cleaned_data.get("pincode")
        clg.clg_contactno= self.cleaned_data.get("clg_contactno")
        clg.year=self.cleaned_data.get('year')
        if commit:
            clg.save()
        return clg

class CourseForm(forms.ModelForm):
    stream=forms.CharField()
    programme=forms.CharField()
    class Meta:
        model=Course
        fields=("course_name","number_seats","fees","duration","rating")

    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course_name'].label = "Course Name"
        self.fields['number_seats'].label = "Available Seats"
        self.fields['fees'].label = "Fees"
        self.fields['duration'].label = "Course Duration"
        self.fields['rating'].label = "Course Rating"

    def save(self,commit=True):
        corse=super(CourseForm,self).save(commit=False)
        corse.stream=self.cleaned_data.get('stream')
        corse.programme=self.cleaned_data.get('programme')
        if commit:
            corse.save()
        return corse

class AdmissionForm(forms.ModelForm):
    appform_fee=forms.CharField(label="Application Form Fee",widget=forms.NumberInput)
    entrance_exam=forms.CharField(label="Entrance Exam",help_text="Enter None if no entrance exam")
    class Meta:
        model=Admission
        fields=("appform_link","submit_date",)
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['appform_link'].label="Application Form Link"
        self.fields['submit_date'].label="Submit Date"

    def save(self,commit=True):
        adm=super(AdmissionForm,self).save(commit=False)
        adm.appform_fee=self.cleaned_data.get('appform_fee')
        adm.entrance_exam=self.cleaned_data.get('entrance_exam')
        if commit:
            adm.save()
        return adm









