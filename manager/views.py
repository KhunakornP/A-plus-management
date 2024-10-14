"""Module for all view classes for pages in the manager app."""

from django.views import generic
from .models import Taskboard, Task, Event
from django.shortcuts import get_object_or_404, redirect
from django.http import Http404, HttpResponse
from django.contrib import messages
from django.forms import ModelForm
from django.urls import reverse
from typing import Any, Union


class TaskboardIndexView(generic.ListView):
    """A view that displays all task boards."""

    template_name = "manager/taskboard_index.html"
    context_object_name = "taskboard_list"
    model = Taskboard


class TaskboardView(generic.DetailView):
    """A view that display a specific taskboard."""

    template_name = "manager/taskboard.html"
    model = Taskboard


class CalendarView(generic.ListView):
    """A view that display the calendar that show events and tasks."""

    template_name = "manager/calendar.html"
    model = Event

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Create context dictionary used to render the template.

        :return: A dictionary containing a list of dicts about events
                 information to be converted into array.
        """
        all_events = Event.objects.all()
        events_array = []
        for event in all_events:
            event_info = {
                "title": event.title,
                "start": event.start_date.isoformat(),
                "end": event.end_date.isoformat(),
            }
            events_array.append(event_info)
        context = {"events": events_array}
        return context


class EventForm(ModelForm):
    """A class for creating an event object from the given POST request."""

    class Meta:
        """Metaclass for the form."""

        model = Event
        fields = ["title", "start_date", "end_date", "details"]

    def __init__(self, *args, **kwargs):
        """Modify the init method to specify which fields are optional."""
        super().__init__(*args, **kwargs)
        # Note while event does have defaults for dates please enter
        # the date that the user clicked on the calendar for the default.
        self.fields["details"].required = False


def create_event(request) -> redirect:
    """
    Create an event object from the POST request.

    :param request: A django HttpRequest object.
    :return: A redirect to the Calendar page.
    """
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, f"Event: {request.POST['title']} added!")
            return redirect(reverse("manager:calendar"))
    # if method is not POST or form is not valid
    messages.error(request, "Event data is invalid.")
    return redirect(reverse("manager:calendar"))


def delete_event(request, event_id: int) -> redirect:
    """
    Delete the given event from the database.

    :param request: A django HttpRequest object.
    :param event_id: The Primary Key (id) of the event.
    :return: A redirect to the calendar page.
    """
    try:
        event = Event.objects.get(pk=event_id)
    except Event.DoesNotExist:
        messages.error(request, "Event does not exist")
        return redirect(reverse("manager:calendar"))
    event_title = event.title
    event.delete()
    messages.info(request, f"Event: {event_title}, has been deleted.")
    return redirect(reverse("manager:calendar"))


def update_event(request, event_id: int) -> redirect:
    """
    Update an event attributes with the given data.

    This function takes a POST request and updates the event with the given
    event_id. It updates all attributes specified in the POST request for the
    event object.

    :param request: A django HttpRequest object.
    :param event_id: The Primary Key (id) of the event.
    :return: A redirect to the calendar page.
    """
    try:
        event = Event.objects.get(pk=event_id)
    except Event.DoesNotExist:
        messages.error(request, "Event does not exist")
        return redirect(reverse("manager:calendar"))
    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.info(request, f"Event: {request.POST['title']} updated.")
            return redirect(reverse("manager:calendar"))
    # if the request was not POST or form is not valid
    messages.error(request, "Event data provided is invalid.")
    return redirect(reverse("manager:calendar"))


class TaskForm(ModelForm):
    """Create a task object from POST request.

    More info at https://docs.djangoproject.com/en/5.1/topics/forms/modelforms
    """

    class Meta:
        """The Meta class."""

        model = Task
        fields = ["title", "status", "end_date", "details", "taskboard"]

    def __init__(self, *args, **kwargs):
        """Mark optional fields as not required."""
        super().__init__(*args, **kwargs)
        self.fields["status"].required = False
        self.fields["end_date"].required = False
        self.fields["details"].required = False


class TaskboardForm(ModelForm):
    """Create a Taskboard object from POST request."""

    class Meta:
        """The Meta class."""

        model = Taskboard
        fields = ["name"]


def get_taskboard(taskboard_id: int) -> Union[Taskboard, None]:
    """Return a Taskboard which has a specific taskboard id.

    :param taskboard_id: the ID of the taskboard
    :return: a Taskboard object, return None if it does not exists
    """
    try:
        return get_object_or_404(Taskboard, pk=taskboard_id)
    except Http404:
        return None


def create_task(request, taskboard_id: int) -> HttpResponse:
    """Create a new task bounded to a specific taskboard from POST request.

    :param request: django request object
    :param taskboard_id: id of the taskboard we're going to bound the task to
    cannot be tested until the taskboard.html page is finished.
    """
    post_data = request.POST.copy()
    post_data["taskboard"] = taskboard_id
    form = TaskForm(post_data)
    if form.is_valid():
        form.save()
        messages.success(request, f'Successfully created task {request.POST["title"]}')
        return redirect(reverse("manager:taskboard", args=(taskboard_id,)))
    else:
        messages.error(request, "Invalid data.")
        return redirect(reverse("manager:taskboard_index"))


def delete_task(request, task_id: int) -> HttpResponse:
    """Delete a specific task from the database.

    :param request: Django's request object
    :param task_id: the ID of the task which is to be deleted
    :return: redirects to the Taskboard page that this task belongs
    """
    try:
        task = Task.objects.get(pk=task_id)
        tb_id = task.taskboard.id
        task.delete()
        return redirect(reverse("manager:taskboard", args=(tb_id,)))
    except (KeyError, Task.DoesNotExist):
        messages.error(request, "This task does not exist")
        return redirect(reverse("manager:taskboard_index"))


def update_task(request, task_id: int) -> HttpResponse:
    """Update task attributes from POST request.

    This method will OVERRIDE the task with everything that's put in the
    POST request if the post request contains all non-optional attributes of
    a task, namely the title and the taskboard. it will DO NOTHING if the either
    the title, or the taskboard, or both, are not specified.

    :param request: Django's request object
    :param task_id: the ID of the task that is to be updated
    :return: redirects to the Taskboard page that this task belongs
    """
    try:
        task = Task.objects.get(pk=task_id)
    except (KeyError, Task.DoesNotExist):
        messages.error(request, "This task does not exist")
        return redirect(reverse("manager:taskboard_index"))
    post_data = request.POST.copy()
    assert task.taskboard is not None
    post_data["taskboard"] = task.taskboard.id
    form = TaskForm(post_data, instance=task)
    if form.is_valid():
        form.save()
        messages.success(request, "The task has been updated")
    else:
        messages.error(request, "Task does not exist")
    return redirect(reverse("manager:taskboard", args=(task_id,)))


def create_taskboard(request) -> HttpResponse:
    """Create a taskboard from POST request.

    :param request: django's request object
    :return: redirect to taskboard index page
    """
    try:
        taskboard_name = request.POST["name"]
        new_taskboard = Taskboard.objects.create(name=taskboard_name)
        new_taskboard.save()
    except KeyError:
        messages.error(request, "Please enter taskboard name.")

    return redirect(reverse("manager:taskboard_index"))


def delete_taskboard(request, taskboard_id: int) -> HttpResponse:
    """Delete a specific taskboard from the database.

    :param request: Django's request object
    :param taskboard_id: the ID of the taskboard which is to be deleted
    :return: redirect to the taskboard index page
    """
    taskboard = get_taskboard(taskboard_id)
    if isinstance(taskboard, Taskboard):
        messages.success(request, f"Deleted Taskboard {taskboard.name}")
        taskboard.delete()
    else:
        messages.error(request, "Taskboard does not exists.")
    return redirect(reverse("manager:taskboard_index"))


def update_taskboard(request, taskboard_id: int) -> HttpResponse:
    """Modify the taskboard form POST request.

    :param request: Django's request object
    :param taskboard_id: the ID of the taskboard which is to be deleted
    :return: redirect to the taskboard index page
    """
    taskboard = get_taskboard(taskboard_id)
    if isinstance(taskboard, Taskboard):
        form = TaskboardForm(request.POST, instance=taskboard)
        if form.is_valid():
            messages.success(request, "Taskboard updated")
            form.save()
        else:
            messages.error(request, "Cannot update taskboard")
    return redirect(reverse("manager:taskboard_index"))
