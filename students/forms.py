from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Student, Course


class StudentRegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=50,
        label="Ім'я"
    )

    last_name = forms.CharField(
        max_length=50,
        label="Прізвище"
    )

    email = forms.EmailField(
        label="Email"
    )

    age = forms.IntegerField(
        min_value=12,
        max_value=18,
        label="Вік"
    )

    phone = forms.CharField(
        max_length=13,
        label="Телефон"
    )

    class Meta:
        model = User
        fields = [
            "username",
            "password1",
            "password2",
            "first_name",
            "last_name",
            "email",
            "age",
            "phone",
        ]

    def clean_email(self):
        email = self.cleaned_data["email"]

        if Student.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Учень з таким email вже зареєстрований."
            )

        return email

    def clean_phone(self):
        phone = self.cleaned_data["phone"]

        if not phone.startswith("+380"):
            raise forms.ValidationError(
                "Телефон має починатися з +380"
            )

        return phone


class CourseForm(forms.Form):
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        label="Курс"
    )

    priority = forms.IntegerField(
        min_value=1,
        max_value=3,
        label="Пріоритет"
    )


class CourseBaseFormSet(forms.BaseFormSet):
    def clean(self):
        super().clean()

        courses = []
        priorities = []

        for form in self.forms:
            if not form.cleaned_data:
                continue

            course = form.cleaned_data.get("course")
            priority = form.cleaned_data.get("priority")

            if course in courses:
                raise forms.ValidationError(
                    "Курси не можуть повторюватися."
                )

            if priority in priorities:
                raise forms.ValidationError(
                    "Пріоритети не можуть повторюватися."
                )

            courses.append(course)
            priorities.append(priority)


CourseFormSet = forms.formset_factory(
    CourseForm,
    formset=CourseBaseFormSet,
    extra=3
)