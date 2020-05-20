from django.apps import AppConfig


class DrivingInstructorBuddy(AppConfig):
    name = 'drivingInstructorBuddy'

    def ready(self):
        import drivingInstructorBuddy.signals
