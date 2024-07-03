from django.shortcuts import render, redirect
from .forms import ScheduleForm
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from subject.models import Subject
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def create_schedule(request, subject_id):
    """
    The `create_schedule` function handles the creation of a schedule for a specific subject.
    
    :param request: The HTTP request object containing request data.
    :param subject_id: The ID of the subject for which the schedule is being created.
    :return: A JsonResponse indicating the success or failure of the schedule creation process.
    """
    # Retrieve the subject object based on the given subject_id, or return a 404 error if not found.
    subject = get_object_or_404(Subject, pk=subject_id)
    
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            # Create a schedule object without saving it to the database yet.
            schedule = form.save(commit=False)
            # Add a success message to be displayed to the user.
            messages.success(request, 'Schedule created successfully!')
            # Assign the subject to the schedule.
            schedule.subject = subject
            # Save the schedule object to the database.
            schedule.save()
            # Render the schedule template with the newly created schedule.
            html = render_to_string('courses/schedule_template.html', {'schedule': schedule, 'subject': subject})
            
            return JsonResponse({'status': 'success', 'html': html})
    
    # Return a JSON response indicating failure if the request is not valid.
    return JsonResponse({'status': 'failed', 'error': 'invalid request'}), 400


@login_required
def schedule(request):
    from .models import Schedule
    import calendar

    calendar = calendar.Calendar()
    c = calendar.monthdayscalendar(year=2024, month=7)
    scheduleList = []

    for week in c:
        for day in week:
            schedules = Schedule.objects.filter(datetime__year=2024, datetime__month=7, datetime__day=day).all()
            scheduleList.append({'day': day, 'schedules': schedules})

    print(scheduleList)

    return render(request, 'schedule/schedule.html', context={'calendar': c, 'scheduleList': scheduleList})
