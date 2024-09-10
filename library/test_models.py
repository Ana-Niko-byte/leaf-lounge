from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.exceptions import ValidationError

# Signal triggering user_profile creation after user login.
from reader.signals import create_or_save_profile
from reader.models import UserProfile
from .models import *

import datetime


class TestibraryModels(TestCase):
    """
    A class for testing models in the Library app. Testing includes asserting
    equal values to those in the model setup, relational testing (including
    signal triggers) and basic validation.

    Methods:
    def setUp():
        Simulates user log in to allow the creation for workspaces and tasks.
        Simulates the creation of a workspace where workspace.creator field is
        automatically assigned the current User instance.
        Simulates the creation of a task where task.creator is automatically
        assigned the current User instance, and task.workspace is automatically
        assigned the current workspace.

    def test_author_profile_creation_and_validation():
        Asserts the author user profile is the same as the current user's user profile.
        Asserts that an author profile can be blank (for authors uploaded via admin panel). For registering users, the author profile is created automatically.

        Asserts the author's first name matches that of the model's setup value.
        Asserts a ValidationError is raised if the author's first name is empty.

        Asserts the author's last name matches that of the model's setup value.
        Asserts a ValidationError is raised if the author's last name is empty.

        Asserts the author's d_o_b is a datetime object that matches the model's setup value.
        Asserts a ValidationError is raised if the author's d_o_b is of the wrong format - this is handled via a date input but just in case.
        Asserts a ValidationError is raised if the author's d_o_b is empty.

        Asserts the author's nationality matches that of the model's setup value.
        Asserts the author's nationality can be blank.

        Asserts the author's bio matches that of the model's setup value.
        Asserts a ValidationError is raised if the author's bio is empty.

    def test_task_model_creation():
        Runs a series of asserions for each Task Model field to validate
        the expected values of the instance.

    def test_workspace_delete_when_user_delete():
        Deletes the user and checks whether workspaces and tasks associated
        with the user were deleted as well, as per cascade.

    def test_task_delete_when_workspace_delete():
        Deletes the current workspace and checks whether tasks associated
        with the workspace were deleted as well, as per cascade.
    """
    def setUp(self):
        """
        Simulates user registration to allow for the creation of a user profile and author profile.
        Retrieves the user profile automatically created following successful user registration.
        Simulates the creation of an author profile and assigns the relevant user profile to the author.user_profile field.
        Saves the relevant models to the test sqlite3 database.
        """
        self.client = Client()
        self.user = User(username="ananiko")
        self.user.set_password("modeltesting")
        self.user.save()

        self.user_profile = UserProfile.objects.get(user=self.user)
        self.author = Author(
            user_profile=self.user_profile,
            first_name="Test Firstname",
            last_name="Test Lastname",
            d_o_b="1999-01-28",
            nationality="Ireland",
            bio="Test author model bio!"
        )
        self.author.save()

    def test_author_profile_creation_and_validation(self):
        """
        Asserts the author user profile is the same as the current user's user profile.
        Asserts that an author profile can be blank (for authors uploaded via admin panel). For registering users, the author profile is created automatically.

        Asserts the author's first name matches that of the model's setup value.
        Asserts a ValidationError is raised if the author's first name is empty.

        Asserts the author's last name matches that of the model's setup value.
        Asserts a ValidationError is raised if the author's last name is empty.

        Asserts the author's d_o_b is a datetime object that matches the model's setup value.
        Asserts a ValidationError is raised if the author's d_o_b is of the wrong format - this is handled via a date input but just in case.
        Asserts a ValidationError is raised if the author's d_o_b is empty.

        Asserts the author's nationality matches that of the model's setup value.
        Asserts the author's nationality can be blank.

        Asserts the author's bio matches that of the model's setup value.
        Asserts a ValidationError is raised if the author's bio is empty.
        """
        self.assertEqual(self.author.user_profile, self.user_profile)
        self.assertTrue(self.author.user_profile, "")

        self.assertEqual(self.author.first_name, "Test Firstname")
        with self.assertRaises(ValidationError):
            self.author.first_name = ""
            self.author.full_clean()

        self.assertEqual(self.author.last_name, "Test Lastname")
        with self.assertRaises(ValidationError):
            self.author.last_name = ""
            self.author.full_clean()

        self.assertEqual(self.author.d_o_b, datetime.date(1999, 1, 28))
        with self.assertRaises(ValidationError):
            self.author.d_o_b = "28/01/1999"
            self.author.full_clean()
        with self.assertRaises(ValidationError):
            self.author.d_o_b = ""
            self.author.full_clean()

        self.assertEqual(self.author.nationality, "Ireland")
        self.assertTrue(self.author.nationality, "")

        self.assertEqual(self.author.bio, "Test author model bio!")
        with self.assertRaises(ValidationError):
            self.author.bio = ""
            self.author.full_clean()

    # def test_task_model_creation(self):
    #     '''
    #     Asserts the task id is 6, as per model setup.
    #     Asserts the task name is 'Test Task', as per model setup.
    #     Asserts the task notes are 'Testing Task Model', as per model setup.
    #     Asserts the task creator's username is 'ananiko', as per user login.
    #     Asserts the task workspace title is 'Test Workspace',
    #     as per model setup.
    #     Asserts the task priority is 'Minor', as per model setup.
    #     Asserts the task status is 'To Do', as per model setup.
    #     Asserts the task due_date is '2024-07-21', as per model setup.
    #     Asserts whether the task updated field is set to False,
    #     as per model setup.
    #     '''
    #     self.assertEqual(self.task.id, 6)
    #     self.assertEqual(self.task.name, 'Test Task')
    #     self.assertEqual(self.task.notes, 'Testing Task Model')
    #     self.assertEqual(self.task.creator.username, 'ananiko')
    #     self.assertEqual(self.task.workspace.title, 'Test Workspace')
    #     self.assertEqual(self.task.priority, 'Minor')
    #     self.assertEqual(self.task.status, 'To Do')
    #     self.assertEqual(self.task.due_date, '2024-07-21')

    # def test_workspace_delete_when_user_delete(self):
    #     '''
    #     Deletes the current user.
    #     Asserts user's workspaces are also deleted.
    #     Asserts user's tasks are also deleted.
    #     '''
    #     self.user.delete()
    #     self.assertEqual(len(Workspace.objects.all()), 0)
    #     self.assertEqual(len(Task.objects.all()), 0)

    # def test_task_delete_when_workspace_delete(self):
    #     '''
    #     Deletes the current workspace.
    #     Asserts tasks associated with that workspace are also deleted.
    #     '''
    #     self.workspace.delete()
    #     self.assertEqual(len(Task.objects.all()), 0)