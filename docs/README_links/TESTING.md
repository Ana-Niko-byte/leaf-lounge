> > > ## Testing & Debugging
> > >
> > > This section outlines procedures for manual testing. For automated testing, please see all files `test*.py`.

> > ### Manual Testing

| Feature | Expected Outcome | Testing Procedure | Result | Remark |
| ------- | ---------------- | ----------------- | ------ | ------ |

> > ### Automated Testing

> #### Models (library app)

`class TestibraryModels():`
A class for testing models in the Library app. Testing includes asserting equal values to those in the model setup, relational testing (including signal triggers) and basic validation.

Models: `Author`, `Genre`, `Book`, `Review`

###### Methods

`def setUp():`
    REGISTRATION:
    Simulates user registration to allow for the creation of a user profile and author profile.

    USER PROFILE & AUTHOR PROFILE:
    Retrieves the user profile automatically created following successful user registration. This is handled via reader.signals.create_or_save_profile.
    Simulates the creation of an author profile and assigns the relevant user profile to the author.user_profile field.

    GENRE & COMMUNITY:
    Simulates the creation of a genre. A community instance associated with the genre is created automatically via library.signals.create_community_on_genre_save.

    BOOK:
    Simulates the creation of a book with relevant relationships to the author and genre models.

    REVIEW:
    Simulates the creation of a review with relevant relationships to the user_profile and book models.

    Saves the relevant models to the test sqlite3 database.

`def test_author_profile_creation_and_validation():`
    Asserts the author user profile is the same as the current user's user profile.
    Asserts that an author profile can be blank (for authors uploaded via admin panel). For registering users, the author profile is created automatically.

    Asserts the author's first name matches the model's setup value.
    Asserts a ValidationError is raised if the author's firstname is empty.

    Asserts the author's last name matches the model's setup value.
    Asserts a ValidationError is raised if the author's lastname is empty.

    Asserts the author's d_o_b is a datetime object that matches the model's setup value.
    Asserts a ValidationError is raised if the author's d_o_b is of the wrong format - this is handled via a date input but just in case.
    Asserts a ValidationError is raised if the author's d_o_b is empty.

    Asserts the author's nationality matches the model's setup value.
    Asserts the author's nationality can be blank.

    Asserts the author's bio matches the model's setup value.
    Asserts a ValidationError is raised if the author's bio is empty.

`def test_genre_and_genre_community_creation():`
    Retrieves the appropriate genre instance.
    Asserts the genre's **str**() returns the expected string for the appropriate genre instance.

    Asserts the genre name matches the model's setup value.
    Asserts a ValidationError is raised if the genre's name is empty.

    Asserts the genre's community field can be blank.
    Asserts the genre's community's name matches the expected value. A community instance is automatically created and linked following a new genre creation. This is handled via library.signals.~

`def test_book_creation():`
    Retrieves the appropriate book instance.
    Asserts the book's **str**() returns the expected string for the appropriate book instance.

    Asserts the book name matches the model's setup value.
    Asserts a ValidationError is raised if the book's name is empty.
    Asserts a ValidationError is raised if the book's name is longer than 100 characters.

    Asserts the book isbn matches the model's setup value.
    Asserts a ValidationError is raised if the book's isbn is empty.
    Asserts a ValidationError is raised if the book's isbn is longer than 13 characters.

    Asserts a slug is automatically generated after a book instance is saved.

    Asserts the book author's firstname matches the model's setup value.
    Asserts a ValidationError is raised if there is no author.

    Asserts the book genre matches the model's setup value.
    Asserts a ValidationError is raised if there is no genre.

    Asserts the book blurb matches the model's setup value.
    Asserts a ValidationError is raised if the book's blurb is empty.

    Asserts the book's year_published field matches the model's setup value.
    Asserts a ValidationError is raised if the book's year_published is of the wrong format.
    Asserts a ValidationError is raised if the book's year_published is empty.
    Asserts a ValidationError is raised if there is no year_published value.

    Asserts the book publisher matches the model's setup value.
    Asserts the book publisher can be empty.

    Asserts the book cover-type matches the model's setup value.
    Asserts a ValidationError is raised if there is no cover-type value.
    Asserts a ValidationError is raised if the book's cover-type is empty.

    Asserts the book's date_added field value is a datetime object that matches the model's setup value.
    Asserts a ValidationError is raised if there is no date_added value.
    Asserts a ValidationError is raised if the book's date_added is empty.
    Asserts a ValidationError is raised if the book's date_added is of the wrong format.

    Asserts the book's price field is a Decimal format that matches the model's setup value.
    Asserts a ValidationError is raised if the book's price is empty.
    Asserts a ValidationError is raised if the book's price is over 5 decimals, i.e., a book's value is raised too high.

`def test_review_creation():`
    Retrieves the appropriate review instance for testing.
    Asserts the review's **str**() returns the expected string for the appropriate review instance.

    Asserts the reviewer is the user profile as per model setup.
    Asserts the user profile belongs to the user as per model setup.
    Asserts a ValidationError is raised if a review is without a reviewer.

    Asserts the book reviewed matches the model's setup value.
    Asserts a ValidationError is raised if there is no book title (no book) associated with the review.

    Asserts the review title matches the model's setup value.
    Asserts a ValidationError is raised if the review title is empty.
    Asserts a ValidationError is raised if the review title is over the 80 character limit as defined in models.py.

    Asserts the review rating matches the model's setup value.
    Asserts a ValidationError is raised if there is no review rating.
    Asserts a ValidationError is raised if the rating is over 10.
    Asserts a ValidationError is raised if the rating is below 0.

    Asserts the review comment matches the model's setup value.
    Asserts a ValidationError is raised if there is no comment.

    Asserts today's (11-09-2024) date is automatically saved to the review's reviewed_on field.
    Asserts a validation error is raised if the reviewed_on date is missing.

    Asserts the newly saved review is saved as an unapproved instance.


> #### Models (reader app)

`class TestUserProfile():`
A class for testing models in the Reader app. Testing includes asserting a user profile is successfully created following user registration, and that the created user profile belongs to the registered user.

Models: `UserProfile`

###### Methods:
`def setUp():`
    REGISTRATION:
    Simulates user registration to allow for the creation of a user profile.

`def test_user_profile_creation_on_user_registration():`
    Retrieves the appropriate user profile instance for testing.
    Asserts a user profile is successfully created following user registration.
    Asserts the user profile's __str__() returns the expected string for the appropriate user profile instance.



> > > ## Issues

1. #### Contact Page `ConnectionRefusedError`
   ![Connection Refused Error](../../docs/images/connectionrefusederror.png)
   The error was encountered when attempting to send emails from the contact page. Instead of redirecting users to the home page with a success message, the application would throw the 500 Server Error page, and the email wouldn't reach the recipients' addresses.

> #### Solution
As it happens, the issue was down to a simple typo in the following line in `blurb/views.py`: `recipient_list=[settings.EMAIL_HOST_USER, f'{email}'],` - the misplaced comma at the end. This syntax rendered the `recipient_list` as an invalid value in the `send_mail()` method, thus throwing the method and redirecting users to the 500 server error page. Removing the comma and saving the file resolved this issue. Testing and eventual resolution were done in `VS Code` by cloning the repository and debugging the relevant code due to Gitpod permissions and limitations.

> > > ## Accessibility & Performance

> > #### Lighthouse

> > #### Colour Accessibility Validator

> > #### HTML Validation

> > #### CSS Validation

> > #### JSHint Validation
All js files are regularly validated during development using [JSHint](https://jshint.com/).

> > #### Pep8 Validation
All python files are regularly validated during development using the [Code Institute PEP8 Linter](https://pep8ci.herokuapp.com/).
