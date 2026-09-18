from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .forms import StudentRegistrationForm, CourseFormSet
from .models import Student


def register(request):
    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)
        formset = CourseFormSet(request.POST)

        print("FORM ERRORS:", form.errors)
        print("FORMSET ERRORS:", formset.errors)
        print("FORMSET NON FORM ERRORS:", formset.non_form_errors())

        if form.is_valid() and formset.is_valid():
            print("ВСЕ ВАЛІДНО")

            user = form.save()

            student = Student.objects.create(
                user=user,
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
                email=form.cleaned_data["email"],
                age=form.cleaned_data["age"],
                phone=form.cleaned_data["phone"],
            )

            courses = []

            for course_form in formset:
                course = course_form.cleaned_data["course"]
                courses.append(course)

            student.courses.set(courses)

            login(request, user)

            return redirect("dashboard")

    else:
        form = StudentRegistrationForm()
        formset = CourseFormSet()

    return render(
        request,
        "students/register.html",
        {
            "form": form,
            "formset": formset,
        }
    )


@login_required
def dashboard(request):
    student = Student.objects.get(user=request.user)

    return render(
        request,
        "students/dashboard.html",
        {
            "student": student,
        }
    )


@login_required
def profile(request):
    student = Student.objects.get(user=request.user)

    return render(
        request,
        "students/profile.html",
        {
            "student": student,
        }
    )