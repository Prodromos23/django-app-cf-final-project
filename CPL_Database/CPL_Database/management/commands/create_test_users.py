from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group

class Command(BaseCommand):
    help = 'Create test users and assign them to groups'

    def handle(self, *args, **kwargs):
        # Create test users
        user1 = User(username='testuser1')
        user1.set_password('pass123')
        user1.is_active = True
        user1.is_staff = True  # Ensure staff status is activated
        user1.save()

        user2 = User(username='testuser2')
        user2.set_password('pass1234')
        user2.is_active = True
        user2.is_staff = True  # Ensure staff status is activated
        user2.save()

        # Check if users are created
        if user1 and user2:
            self.stdout.write(self.style.SUCCESS('Successfully created test users'))

        # Get the groups
        try:
            group1 = Group.objects.get(name='Group1')
            group2 = Group.objects.get(name='Group2')
        except Group.DoesNotExist:
            self.stdout.write(self.style.ERROR('One or more groups do not exist'))
            return

        # Assign users to groups
        user1.groups.add(group1)
        user2.groups.add(group2)

        # Save the users
        user1.save()
        user2.save()

        self.stdout.write(self.style.SUCCESS('Successfully assigned users to groups'))