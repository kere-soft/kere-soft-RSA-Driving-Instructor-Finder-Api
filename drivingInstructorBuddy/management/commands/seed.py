from django.core.management.base import BaseCommand, CommandError
from drivingInstructorBuddy.modelsFactory import *


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the total number of users to be created')

    def handle(self, *args, **options):
        if options['total']:
            user = options['total']
            try:
                for i in range(user):
                    user = UserFactory.create()
                    if user:
                        # Create user profile
                        profile = ProfileFactory.build()
                        profile.user = user
                        profile.save()
                        # Create Instructor profile, we only need 20 instructor
                        if i < 20:
                            instructor = InstructorFactory.build()
                            instructor.user = user
                            instructor.save()
                        else:
                            learner = LearnerFactory.build()
                            learner.user = user
                            learner.save()
            except Exception as e:
                self.stdout.write("Error occurred with message " + str(e))
        else:
            self.stdout.write("Please provide all required param with the command", ending='')
