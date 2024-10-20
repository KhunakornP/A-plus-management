from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from .functions import today_midnight
from .user_info import StudentInfo, ParentInfo, UserPermissions
from .estimate_history import EstimateHistory, EstimateHistoryManager
from .event import Event
from .taskboard import Taskboard
from .task import Task
