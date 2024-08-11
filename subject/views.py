from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import CourseForm, AddStudentForm, MaterialForm, MaterialFileForm
from .models import Subject, Material, MaterialFile
from user.models import CustomUser
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.forms import modelformset_factory
from django.http import JsonResponse

@login_required
def course(request, id):
    """
    The `course` function in Python handles the creation of materials and files for a specific subject
    in a course.
    
    :param request: The `request` parameter in the `course` function is an HttpRequest object that
    represents the current HTTP request. It contains information about the request made by the client,
    such as the request method (GET, POST, etc.), request data, user session information, and more. In
    this function, the
    :param id: The `id` parameter in the `course` function is used to identify the specific Subject
    object for which the course materials are being managed. It is used to retrieve the Subject object
    from the database using `get_object_or_404` and then associate the course materials with that
    particular subject
    :return: The `course` view function returns a rendered HTML template named 'courses/course.html'
    along with the context data containing `material_form`, `file_formset`, and `subject`.
    """
    from schedule.models import Schedule
    from schedule.forms import ScheduleForm
    from user.models import CustomUser

    subject = get_object_or_404(Subject, pk=int(id))
    MaterialFileFormSet = modelformset_factory(MaterialFile, form=MaterialFileForm, extra=1)
    materials = subject.materials.order_by("-created_at").all()

    if request.method == 'POST':

        material_form = MaterialForm(request.POST)
        file_formset = MaterialFileFormSet(request.POST, request.FILES, queryset=MaterialFile.objects.none())

        if material_form.is_valid() and file_formset.is_valid():
            material = material_form.save(commit=False)
            material.subject = subject
            material.save()

            for form in file_formset.cleaned_data:
                if form:
                    files = form['file']

                    for f in files:
                        material_file = MaterialFile(material=material, file=f)
                        material_file.save()

            messages.success(request, 'Material and files have been successfully added.')
            return redirect('course', id=subject.id)
    else:
        material_form = MaterialForm()
        file_formset = MaterialFileFormSet(queryset=MaterialFile.objects.none())

    schedules = Schedule.objects.filter(subject=subject).all()
    form = ScheduleForm()

    return render(request, 'courses/course.html', {
        'material_form': material_form,
        'file_formset': file_formset,
        'subject': subject,
        'materials': materials,
        'schedules': schedules,
        'form': form,
    })

@login_required
def students_search(request, subject_id):
    from django.http import JsonResponse
    from django.template.loader import render_to_string

    if request.method == 'POST':
        search_data = request.POST.get('search')
        subject = get_object_or_404(Subject, pk=subject_id)
        if search_data:
            if '@' in search_data:
                students = CustomUser.objects.filter(email__contains=search_data).all()
            else:
                students = CustomUser.objects.filter(name__contains=search_data).all()
            html = render_to_string('courses/students_search.html', {'students': students, 'subject': subject})

            return JsonResponse({'status': 'success', 'html': html})
    
    return JsonResponse({'status': 'failed', 'error': 'invalid request'}), 400

@login_required
def create_course(request):
    """
    The `create_course` function in Python checks if the user is a teacher, processes a form to create a
    course, and displays appropriate messages.
    
    :param request: The `request` parameter in the `create_course` function is an object that represents
    the HTTP request made by a user. It contains information about the request, such as the user making
    the request, the method used (GET, POST, etc.), and any data sent with the request. In this
    :return: The `create_course` function returns a rendered HTML template for creating a course. If the
    user is not authorized as a teacher, a message is displayed and the user is redirected to the
    homepage. If the request method is POST and the form is valid, a new course is created and saved
    with the current user as the teacher. A success message is displayed, and the user is redirected to
    the homepage
    """
    if not request.user.is_teacher:
        messages.info(request, 'You are not authorized to create a course.')
        return redirect('homepage')

    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user
            
            course.save()
            form.save_m2m()

            messages.success(request, 'Course created successfully.')
            return redirect('/')
    else:
        form = CourseForm()
    return render(request, 'courses/create_course.html', {'form': form})

@login_required
def add_student(request, subject_id, student_id):
    from user.models import CustomUser
    from subject.models import Subject
    from django.template.loader import render_to_string

    if request.method == 'POST':
        try:
            subject = get_object_or_404(Subject, pk=subject_id)
            user = get_object_or_404(CustomUser, pk=student_id)
            subject.students.add(user)

            html = render_to_string('courses/student_template.html', {'student': user})

            return JsonResponse({'status': 'success', 'html': html})
        except:
            return JsonResponse({'status': 'failed', 'error': 'invalid request'}), 400

@login_required
def delete_student(request, subject_id, student_id):
    from user.models import CustomUser
    from subject.models import Subject
    if request.method == 'POST':
        try:
            subject = get_object_or_404(Subject, pk=subject_id)
            user = get_object_or_404(CustomUser, pk=student_id)
            subject.students.remove(user)
            return JsonResponse({'status': 'success'})
        except:
            return JsonResponse({'status': 'failed', 'error': 'invalid request'}), 400
        
@login_required
def material_page(request, subject_id, material_id):
    from . models import Subject, Material, HomeworkFile
    from .forms import AddHomeworkForm, HomeworkFileForm

    subject = get_object_or_404(Subject, pk=subject_id)
    material = get_object_or_404(Material, pk=material_id)

    homeworkForm = AddHomeworkForm()
    homeworkFileFormSet = modelformset_factory(HomeworkFile, form=HomeworkFileForm, extra=1)
    file_formset = homeworkFileFormSet(queryset=HomeworkFile.objects.none())

    if request.method == 'POST':
        homework_form = AddHomeworkForm(request.POST)
        file_formset = homeworkFileFormSet(request.POST, request.FILES, queryset=HomeworkFile.objects.none())

        if homework_form.is_valid() and file_formset.is_valid():
            pass

    context = {
        'subject': subject,
        'material': material,
        'form': homeworkForm,
        'file_formset': file_formset
    }

    return render(request, 'courses/material_page.html', context=context)

@login_required
def delete_material(request, subject_id, material_id):
    from .models import Material
    if request.method == 'POST':
        try:
            Material.objects.filter(id=material_id).first().delete()
            return JsonResponse({'status': 'success'})
        except:
            return JsonResponse({'status': 'failed', 'error': 'invalid request'}), 400

@login_required
def delete_schedule(request, subject_id, schedule_id):
    from schedule.models import Schedule
    if request.method == 'POST':
        try:
            Schedule.objects.filter(id=schedule_id).first().delete()
            return JsonResponse({'status': 'success'})
        except:
            return JsonResponse({'status': 'failed', 'error': 'invalid request'}), 400

@login_required
def course_url(request, subject_id):
    """
    The `course_url` function redirects the user to the homepage.
    
    :param request: The `request` parameter in the `course_url` function is typically an object that
    contains information about the current HTTP request, such as the user's browser information, session
    data, and any data sent in the request. It is commonly used in web development frameworks like
    Django or Flask to handle and process
    :return: A redirect to the 'homepage' URL is being returned.
    """
    from .models import Subject
    subject = Subject.objects.filter(id=subject_id).first()
    subject.students.add(request.user)
    return redirect('course', id=subject_id)
