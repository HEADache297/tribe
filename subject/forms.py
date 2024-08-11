from django import forms
from .models import Subject, Material, MaterialFile
from django.forms.widgets import Input, TimeInput, URLInput
from user.models import CustomUser
from tinymce.widgets import TinyMCE
from .models import Homework, HomeworkFile



# The `CourseForm` class is a form in Django that allows users to input a title and summary for a
# subject.
class CourseForm(forms.ModelForm, forms.Form):
    title = forms.CharField(max_length=255, widget=Input(attrs={'class': 'm-3 h-12 rounded-lg p-2 bg-gray-900 text-white', 'placeholder': 'Title'}))
    summary = forms.CharField(max_length=1024, widget=Input(attrs={'class': 'm-3 h-12 rounded-lg p-2 bg-gray-900 text-white', 'placeholder': 'Description'}))

    class Meta:
        model = Subject
        fields = ['title', 'summary']



# The `AddStudentForm` class is a Django form used to add multiple students to a subject with
# checkboxes for selection.
class AddStudentForm(forms.Form):
    students = forms.ModelMultipleChoiceField(queryset=CustomUser.objects.filter(is_student=True, is_superuser=False), widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = Subject
        fields = ['students']



# The class `MultipleFileInput` allows for multiple files to be selected in a form input field.
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


# This class extends the ClearableFileInput class to handle multiple file inputs.
class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


# The `MaterialForm` class allows users to input a title and description for a material, using TinyMCE for rich text editing.
class MaterialForm(forms.ModelForm):
    title = forms.CharField(max_length=255, widget=Input(attrs={'class': 'h-12 rounded-lg p-2 bg-gray-900 text-white w-96', 'placeholder': 'Title'}))
    description = forms.CharField(widget=TinyMCE(attrs={
        'class': 'm-2 h-12 rounded-lg p-2 bg-gray-900 text-white', 
        'placeholder': 'Description'
    }))

    class Meta:
        model = Material
        fields = ['title', 'description']

# The `MaterialFileForm` class allows users to upload multiple files related to a material.
class MaterialFileForm(forms.ModelForm):
    file = MultipleFileField()

    class Meta:
        model = MaterialFile
        fields = ['file']


class AddHomeworkForm(forms.ModelForm):
    description = forms.CharField(widget=TinyMCE(attrs={
        'class': 'm-2 h-12 rounded-lg p-2 bg-gray-900 text-white', 
        'placeholder': 'Description'
    }))

    class Meta:
        model = Homework
        fields = ['description']

class HomeworkFileForm(forms.ModelForm):
    file = MultipleFileField()

    class Meta:
        model = HomeworkFile
        fields = ['file']

