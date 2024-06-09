from django import forms
from .models import Subject, Material, MaterialFile
from django.forms.widgets import Input, TimeInput, URLInput
from user.models import CustomUser


class CourseForm(forms.ModelForm, forms.Form):
    title = forms.CharField(max_length=255, widget=Input(attrs={'class': 'm-3 h-12 rounded-lg p-2 bg-gray-900 text-white', 'placeholder': 'Title'}))
    summary = forms.CharField(max_length=1024, widget=Input(attrs={'class': 'm-3 h-12 rounded-lg p-2 bg-gray-900 text-white', 'placeholder': 'Description'}))
    students = forms.ModelMultipleChoiceField(queryset=CustomUser.objects.filter(is_student=True, is_superuser=False), widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = Subject
        fields = ['title', 'summary', 'students']



class AddStudentForm(forms.Form):
    students = forms.ModelMultipleChoiceField(queryset=CustomUser.objects.filter(is_student=True, is_superuser=False), widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = Subject
        fields = ['students']


class MaterialForm(forms.ModelForm):

    class Meta:
        model = Material
        fields = ['description', 'title']


class MaterialFileForm(forms.ModelForm):

    class Meta:
        model = MaterialFile
        fields = ['file']




