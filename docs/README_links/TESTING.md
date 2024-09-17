> > > ## Testing & Debugging

This section outlines procedures for manual testing. For automated testing, please see all files `test*.py`.

> > ### Manual Testing

| Feature | Expected Outcome | Testing Procedure | Result | Remark |
| ------- | ---------------- | ----------------- | ------ | ------ |

> > ### Automated Testing

> ### Models (library app)
### `class TestibraryModels():`

A class for testing models in the Library app. Testing includes asserting equal values to those in the model setup, relational testing (including signal triggers) and basic validation.

Models: `Author`, `Genre`, `Book`, `Review`

`def setUp():`
```Python
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
```

`def test_author_profile_creation_and_validation():`

```Python
    Asserts the author user profile is the same as the current user's user profile.
    Asserts that an author profile can be blank (for authors uploaded via admin panel). For registering users, the author profile is created automatically.

    Asserts the author's first name matches the model's setup value.
    Asserts a ValidationError is raised if the author's firstname is empty.

    Asserts the author's last name matches the model's setup value.
    Asserts a ValidationError is raised if the author's lastname is empty.

    Asserts the author's d_o_b is a datetime object that matches the model's setup value.
    Asserts a ValidationError is raised if:
        - the author's d_o_b is of the wrong format - this is handled via a date input but just in case.
        - the author's d_o_b is empty.

    Asserts the author's nationality matches the model's setup value.
    Asserts the author's nationality can be blank.

    Asserts the author's bio matches the model's setup value.
    Asserts a ValidationError is raised if the author's bio is empty.
```

`def test_genre_and_genre_community_creation():`
```Python
    Retrieves the appropriate genre instance.
    Asserts the genre's **str**() returns the expected string for the appropriate genre instance.

    Asserts the genre name matches the model's setup value.
    Asserts a ValidationError is raised if the genre's name is empty.

    Asserts the genre's community field can be blank.
    Asserts the genre's community's name matches the expected value. A community instance is automatically created and linked following a new genre creation. This is handled via library.signals.~
```

`def test_book_creation():`
```Python
    Retrieves the appropriate book instance.
    Asserts the book's **str**() returns the expected string for the appropriate book instance.

    Asserts the book name matches the model's setup value.
    Asserts a ValidationError is raised if:
        - the book's name is empty.
        - the book's name is longer than 100 characters.

    Asserts the book isbn matches the model's setup value.
    Asserts a ValidationError is raised if
        - the book's isbn is empty.
        - the book's isbn is longer than 13 characters.

    Asserts a slug is automatically generated after a book instance is saved.

    Asserts the book author's firstname matches the model's setup value.
    Asserts a ValidationError is raised if there is no author.

    Asserts the book genre matches the model's setup value.
    Asserts a ValidationError is raised if there is no genre.

    Asserts the book blurb matches the model's setup value.
    Asserts a ValidationError is raised if the book's blurb is empty.

    Asserts the book's year_published field matches the model's setup value.
    Asserts a ValidationError is raised if
        - the book's year_published is of the wrong format.
        - the book's year_published is empty.
        - there is no year_published value.

    Asserts the book publisher matches the model's setup value.
    Asserts the book publisher can be empty.

    Asserts the book cover-type matches the model's setup value.
    Asserts a ValidationError is raised if
        - there is no cover-type value.
        - the book's cover-type is empty.

    Asserts the book's date_added field value is a datetime object that matches the model's setup value.
    Asserts a ValidationError is raised if
        - there is no date_added value.
        - the book's date_added is empty.
        - the book's date_added is of the wrong format.

    Asserts the book's price field is a Decimal format that matches the model's setup value.
    Asserts a ValidationError is raised if
        - the book's price is empty.
        - the book's price is over 5 decimals, i.e., a book's value is raised too high.
```

`def test_review_creation():`
```Python
    Retrieves the appropriate review instance for testing.
    Asserts the review's **str**() returns the expected string for the appropriate review instance.

    Asserts the reviewer is the user profile as per model setup.
    Asserts the user profile belongs to the user as per model setup.
    Asserts a ValidationError is raised if a review is without a reviewer.

    Asserts the book reviewed matches the model's setup value.
    Asserts a ValidationError is raised if there is no book title (no book) associated with the review.

    Asserts the review title matches the model's setup value.
    Asserts a ValidationError is raised if
        - the review title is empty.
        - the review title is over the 80 character limit as defined in models.py.

    Asserts the review rating matches the model's setup value.
    Asserts a ValidationError is raised if
        - there is no review rating.
        - the rating is over 10.
        - the rating is below 0.

    Asserts the review comment matches the model's setup value.
    Asserts a ValidationError is raised if there is no comment.

    Asserts today's (11-09-2024) date is automatically saved to the review's reviewed_on field.
    Asserts a validation error is raised if the reviewed_on date is missing.

    Asserts the newly saved review is saved as an unapproved instance.
```

> #### Model (community app)
### `class TestCommunityModel():`

A class for testing the community model. Testing includes asserting equal values to those in the model setup, save method testing, and format validation for datetime objects and slugs.

Fields: `Community`

`def setUp():`
```Python
    REGISTRATION:
        Simulates user registration to allow for users to access community-related functionality and models.

    GENRE & COMMUNITY:
        Simulates the creation of a genre. After the mock genre is saved, a community is automatically created.

    Saves the relevant models to the test sqlite3 database.
```

`def test_community_creation_following_genre_creation():`
```Python
    Retrieves the appropriate community instance for testing and saves it.
    This process generates the community slug as per the defined format.

    Asserts the community's __str__() returns the expected string for the appropriate community instance.

    Asserts the correct community is retrieved.
    Asserts a ValidationError is raised if
        - the community's name is empty.
        - there is no community name.
        - the community's name exceeds the 80 character limit.

    Asserts the community's description matches the model's setup value.

    Asserts the community's slug matches the expected slug string format.
    Asserts a ValidationError is thrown if the slug is inputted or generated in an incorrect format.
```

### `class TestForumAndMessageModels():`

A class for testing the forum and message models in the Community app.
Testing includes asserting equal values to those in the model setup, save method testing, user profile association, and format validation for datetime objects and slugs.

Fields: `Forum`, `Message`

`def setUp()`
```Python
    REGISTRATION:
        Simulates user registration to allow for the creation of a user profile.

    USER PROFILE & AUTHOR PROFILE:
        reate_or_save_profile.

    GENRE & COMMUNITY & FORUM:
        Simulates the creation of a genre. After the mock genre is saved, a community is automatically created. After the community is saved, forums can be created inside the community.
        Simulates the creation of a forum and saves it.

    MESSAGE:
        Simulates the creation of a message and saves it.

    Saves the relevant models to the test sqlite3 database.
```

`def test_forum_creation():`
```Python
    Retrieves the appropriate forum instance for testing.
    Asserts the forum's __str__() returns the expected string for the appropriate forum instance.

    Asserts the correct forum is retrieved by checking the name.
    Asserts a ValidationError is raised if
        - the forum's name is empty.
        - there is no forum name.
        - the forum's name exceeds the 80 character limit.

    Asserts the forum slug is automatically generated in the correct format after the instance is saved.
    Asserts a ValidationError is thrown if the slug is inputted or generated in an incorrect format.

    Asserts the forum's date_added matches today's date.
    Asserts a ValidationError is thrown if the date_added is does not match today's date.

    Asserts the forum is created inside the correct community by checking the name of the community.
```

`def test_message_creation():`
```Python
    Retrieves the appropriate message instance for testing.
    Asserts the message's __str__() returns the expected string for the appropriate message instance.

    Asserts the message is created inside the correct forum by checking its associated forum name.

    Asserts the message's content matches the model's setup value.
    Asserts a ValidationError is raised if
        - the message's content is empty.
        - there is no message content.

    Asserts the message sender matches the expected user profile.
    Asserts the message sender's username matches the expected value.

    Asserts the message's date_sent matches today's date.
    Asserts a ValidationError is thrown if the date_sent does not match today's date.
```

> ### Models (checkout app)

### `class TestCheckoutModels():`

A class for testing the order and booklineitem models in the checkout app.
Testing includes asserting equal values to those in the model setup, save method testing, and format validation for timezone objects and slugs.

Fields: `order`

`def setUp():`
```Python
    REGISTRATION:
        Simulates user registration to allow for the creation of a user profile.

    USER PROFILE & AUTHOR PROFILE:
        Retrieves the user profile automatically created following successful user registration. This is handled via reader.signals.create_or_save_profile.
        Simulates the creation of an author profile and assigns the relevant user profile to the author.user_profile field.

    GENRE & COMMUNITY:
        Simulates the creation of a genre.

    BOOK:
        Simulates the creation of a book with relevant relationships to the author and genre models.

    ORDER & BOOKLINEITEM:
        Simulates the creation of an order with no order number.
        Simulates the creation of a booklineitem, with relevant relationships to the order and book models. These models in turn depend on the genre, user profile, and author models.

    Saves the relevant models to the test sqlite3 database.
```

`def test_order_creation_and_string_fields():`
```Python
    Retrieves the appropriate order instance for testing.
    Asserts the order's __str__() returns the expected string for the appropriate order instance.

    Asserts order associated user profile matches the expected user profile.
    Asserts the order's user's username matches the expected value.

    Asserts the order's order number is not empty or None. This ensures that the model was saved and an order number was automatically generated and assigned.

    Asserts the order's associated user's full name matches the model's setup.
    Asserts a ValidationError is raised if:
        - the full_name field is empty.
        - there is no full_name value.
        - the full_name is longer than 50 characters.

    Asserts the order's associated email matches the model's setup.
    Asserts a ValidationError is raised if
        - the email field is empty.
        - there is no email value.
        - the email is of an unexpected format.

    Asserts the order's associated phone_number matches the model's setup.
    Asserts a ValidationError is raised if
        - the phone_number field is empty.
        - there is no phone_number value.
        - the phone_number is longer than 20 characters.

    Asserts the order's associated country matches the model's setup.
    Asserts a ValidationError is raised if
        - the country field is empty.
        - there is no country value.
        - the country is of an unexpected format.

    Asserts the order's associated postcode matches the model's setup.
    Asserts a ValidationError is raised if the postcode is of an unexpected format.

    Asserts the order's associated town_city matches the model's setup.
    Asserts a ValidationError is raised if
        - the town_city field is empty.
        - there is no town_city value.
        - the town_city is longer than 40 characters.

    Asserts the order's associated street_1 matches the model's setup.
    Asserts a ValidationError is raised if
        - the street_1 field is empty.
        - there is no street_1 value.
        - the street_1 is longer than 80 characters.

    Asserts the order's associated street_2 matches the model's setup.
    Asserts a ValidationError is raised if
        - the street_2 field is empty.
        - there is no street_2 value.
        - the street_2 is longer than 80 characters.

    Asserts the order's associated county matches the model's setup.
    Asserts a ValidationError is raised if the county is longer than 80 characters.
```

`def test_order_creation_and_decimal_fields():`
```Python
    Retrieves the appropriate order instance for testing.
    Asserts the order's __str__() returns the expected string for the appropriate order instance.

    Asserts the order's associated date matches the current date.
    Asserts a ValidationError is raised if:
        - the date field is empty.
        - there is no date value.

    Asserts the order's delivery_cost field is a Decimal format that matches the model's setup value.
    Asserts the delivery_cost cannot be null or empty.
    Asserts a ValidationError is raised if the delivery_cost is over 6 decimals, i.e., a book's value is raised too high, or is below 0.

    Asserts the order's order_total field is a Decimal format that matches the model's setup value.
    Asserts the order_total cannot be null or empty.
    Asserts a ValidationError is raised if the order_total is over 10 decimals, i.e., the order_total is raised too high, or is below 0.

    Asserts the order's grand_total field is a Decimal format that matches the model's setup value.
    Asserts the grand_total cannot be null or empty.
    Asserts a ValidationError is raised if the grand_total is over 10 decimals, i.e., the grand_total is raised too high, or is below 0.

    Asserts the order's original basket identifier matches the model's setup value.
    Asserts there must be an original_basket value.

    Asserts the order's associated stripe_pid matches the models's setup value.
    Asserts a ValidationError is raised if there is no stripe_pid or it is empty.
```

`def test_booklineitem_creation():`
```Python
    Retrieves the appropriate booklineitem instance for testing.
    Asserts the booklineitem's __str__() returns the expected string for the appropriate booklineitem instance.

    Asserts the booklineitem's order's user matches the appropriate user.
    Asserts the booklineitem's book matches the appropriate book.
    Asserts the booklineitem book type matches the model's set up and raises a ValidationError if there is no type or the type value is empty.

    Asserts the booklineitem quantity matches the model's set up and raises a ValidationError is there is no quantity, the quantity is under the minimum value of 1, or over the maximum value of 99.

    Asserts the booklineitem book_order_cost is calculated and saved correctly.
```

> ### Models (reader app)
### `class TestUserProfile():`

A class for testing models in the Reader app. Testing includes asserting a user profile is successfully created following user registration, and that the created user profile belongs to the registered user.

Models: `UserProfile`

`def setUp():`
```Python
    REGISTRATION:
        Simulates user registration to allow for the creation of a user profile.
```

`def test_user_profile_creation_on_user_registration():`
```Python
    Retrieves the appropriate user profile instance for testing.

    Asserts a user profile is successfully created following user registration.

    Asserts the user profile's __str__() returns the expected string for the appropriate user profile instance.
```


> ### URLS (basket app)
### `class TestBasketURLs():`
A class for testing URLs associated with the basket app. This class tests urls resolve from their FBVs and that certain views are allowed to handle DELETE requests.

`def test_basket_resolves():`
```Python
    Reverses the URL name and checks if it returns the correct FBV of basket.

    Asserts the basket view (basket) is resolved from 'basket'.
```

`def test_add_to_basket_resolves():`
```Python
    Reverses the URL name with arguments [int:book_id] and checks if it returns the correct FBV of add_basket.

    Asserts the view for adding items to basket (add_basket) is resolved from 'add_to_basket' with an int argument.
```

`def test_update_basket_resolves():`
```Python
    Reverses the URL name with arguments [int:book_id] and checks if it returns the correct FBV of amend_basket.

    Asserts the view for updating items in basket (amend_basket) is resolved from 'update_basket' with an int argument.
```

`def test_delete_from_basket_resolves():`
```Python
    Reverses the URL name with arguments [slug, int:book_id] and checks if it returns the correct FBV of delete_basket.

    Asserts the view for deleting items from basket (delete_basket) is resolved from 'delete_basket' with an int argument.

    Asserts the view is allowed to handle DELETE requests.
```

> ### URLS (blurb app)
### `class TestBlurbURLs():`
A class for testing URLs associated with the blurb app.

`def test_home_resolves():`
```Python
    Reverses the URL name and checks the correct FBV of blurb returns.
    Asserts the home view (blurb) is resolved from 'home'.
```

`def test_contact_resolves():`
```Python
    Reverses the URL name and checks the correct FBV of contact returns.
    Asserts the contact view (contact) is resolved from 'contact'.
```

> ### URLS (checkout app)
### `class TestCheckoutURLs():`

A class for testing URLs associated with the checkout app.
This class tests urls resolve from their FBVs.

`def test_checkout_resolves():`
```Python
    Reverses the URL name and checks if it returns the correct FBV of checkout.

    Asserts the checkout view (checkout) is resolved from 'checkout'.
```

`def test_success_resolves():`
```Python
    Reverses the URL name with arguments [str:order_number] and checks if it returns the correct FBV of success.

    Asserts the view called after successful checkout (success) is resolved from 'success' with a str argument of the order number.
```

> ### URLS (community app)
### `class TestCommunityURLs():`

A class for testing URLs associated with the community app.
This class tests urls resolve from their FBVs.

`def test_community_general_resolves():`
```Python
    Reverses the URL name and checks if it returns the correct FBV of community_general.

    Asserts the community general view (community) is resolved from 'communities'.
```

`def test_community_specific_resolves():`
```Python
    Reverses the URL name with arguments [slug:slug] and checks if it returns the correct FBV of community.

    Asserts specific community views (community) resolve from 'community' with slug arguments generated from the community name.
```

`def test_forum_detail_resolves():`
```Python
    Reverses the URL name with arguments [slug:slug] and checks if it returns the correct FBV of forum_detail.

    Asserts the genre-specific forum details (forum_detail) resolve from 'forum-detail' with slug arguments generated from the forum name.
```

`def test_author_registration_resolves():`
```Python
    Reverses the URL name and checks if it returns the correct FBV of create_author.

    Asserts the author registration view (create_author) is resolved from 'create_author'.
```

`def test_book_registration_resolves():`
```Python
    Reverses the URL name and checks if it returns the correct FBV of upload_book.

    Asserts the book upload/registration view (upload_book) is resolved from 'upload_book'.
```

`def test_delete_message_from_forum_resolves():`
```Python
    Reverses the URL name with arguments [slug:slug] and [int:id] and checks if it returns the correct FBV of delete_message.

    Asserts the view for deleting forum messages (delete_message) resolves from 'delete_message' with arguments of slug: forum name and int: message id.
```

> ### URLS (library app)
### `class TestLibraryURLs():`
A class for testing URLs associated with the library app.
This class tests urls resolve from their FBVs.

`def test_library_resolves():`
```Python
    Reverses the URL name and checks if it returns the correct FBV of library.

    Asserts the library view (library) is resolved from 'library'.
```

`def test_book_detail_resolves():`
```Python
    Reverses the URL name with arguments [slug:slug] and checks if it returns the correct FBV of book_detail.

    Asserts book detail views (book_detail) resolve from 'book-summary' with slug arguments generated from the book title and author last name.
```

> ### URLS (marketing app)
### `class TestMarketingURLs():`

A class for testing URLs associated with the marketing app.
This class tests urls resolve from their FBVs.

`def test_subscribe_resolves():`
```Python
    Reverses the URL name and checks if it returns the correct FBV of
    subscribe.

    Asserts the newsletter subscribe view (subscribe_view) resolves from
    'subscribe'.
```

`def test_unsubscribe_resolves():`
```Python
    Reverses the URL name and checks if it returns the correct FBV of
    unsubscribe.

    Asserts the newsletter unsubscribe view (unsubscribe_view) resolves
    from 'unsubscribe'.
```

> ### URLS (reader app)
### `class TestUserProfileAssociatedURLs():`

A class for testing URLs associated with the reader app.
This class tests urls resolve from their FBVs.

`def test_user_profile_resolves():`
```Python
    Reverses the URL name and checks if it returns the correct FBV of
    my_profile.

    Asserts the user profile view (my_profile) resolves
    from 'user_profile'.
```

def test_user_books_resolves():
```Python
    Reverses the URL name and checks if it returns the correct FBV of
    my_books.

    Asserts the user book storage view (my_books) resolves
    from 'user_books'.
```

`def test_review_resolves():`
```Python
    Reverses the URL name and checks if it returns the correct FBV of
    leave_review.

    Asserts the view for leaving book reviews (leave_review) resolves
    from 'leave_review' with an int book id argument.
```

`def test_update_review_resolves():`
```Python
    Reverses the URL name and checks if it returns the correct FBV of
    update_review.

    Asserts the view for updating book reviews (update_review) resolves
    from 'update_review' with an int book id argument.
```

`def test_delete_review_resolves():`
```Python
    Reverses the URL name and checks if it returns the correct FBV of
    delete_review.

    Asserts the view for deleting book reviews (delete_review) resolves
    from 'delete_review' with an int book id argument.
```

`def test_unauthenticated_user_is_redirected():`
```Python
        Asserts unauthenticated users are redirected instead of allowing
        access to all views associated with the reader app, as per the
        @login_required decorator.
```

`def test_admin_approve_review_resolves():`
```Python
    Reverses the URL name and checks if it returns the correct FBV of
    approve_review.

    Asserts the view for admins to approve book reviews (approve_review) resolves
    from 'approve_review' with an int book id argument.
```

> ### Views (Basket App)

### `class TestBasketViews(TestCase):`

A class to test views associated with the Basket app. Testing scope
includes testing correct redirection, status codes and template usage.


`def setUp():`
```Python
    REGISTRATION:
        Simulates user registration to allow for users to create an
        author profile to allow for the creation of a book.

    USER & AUTHOR PROFILES:
        A user profile is created automatically following successful
        registration and retrieved. This profile is associated with
        an author profile.

    GENRE + BOOK:
        A test genre is created and assigned to the test book instance.
        This instance is used in the testing of URLs in POST requests.

    Saves the relevant models to the test sqlite3 database.
    Retrieves the relevant URLs and assigns them to variables for testing.
```

`def test_basket_get_request_is_retrieved():`
```Python
    Retrieves the basket URL and asserts the view renders successfully.
    Asserts the view status code is 200.
    Asserts the template used matches the expected template defined in
    views.py.
```

`def test_add_to_basket_post_request_is_retrieved():`
```Python
    Retrieves the add_to_basket URL and asserts the view handles post data.
    Asserts the view redirects after data handling.
    Asserts the client is redirected to the correct URL, correctly
    redirects and has a status code of 302 indicating redirection, a
    target status of 200 meaning the view is rendered correctly.
```

`def test_update_basket_post_request_is_resolved():`
```Python
    Retrieves the update_basket URL and asserts the view handles post data.
    Asserts the view redirects after data handling.
    Asserts the client is redirected to the correct URL, correctly
    redirects and has a status code of 302 indicating redirection, a target
    status of 200 meaning the view is rendered correctly.
```

`def test_delete_from_basket_post_request_is_resolved():`
```Python
    Retrieves the delete_from_basket URL and asserts the view handles
    post data.
    Asserts the view status code is 200.
```

> ### Views (Blurb App)
### `class TestBlurbViews(TestCase):`

A class to test views associated with the Blurb app. Testing scope
includes testing correct redirection, status codes and template usage.

`def setUp():`
```Python
    Retrieves the relevant URLs and assigns them to variables for testing.
```

`def test_home_page_is_retrieved():`
```Python
    Retrieves the home page URL and asserts the view renders successfully.
    Asserts the view status code is 200.
    Asserts the template used matches the expected template defined in
    views.py.
```

`def test_contact_page_get_request_is_retrieved():`
```Python
    Retrieves the contact page URL and asserts the view renders correctly.
    Asserts the view status code is 200.
    Asserts the template used matches the expected template defines in
    views.py
```

`def test_contact_page_post_request_is_successful():`
```Python
    Simulates form data passed to the contact view for testing a POST
    request.
    Asserts the client is redirected to the correct URL if the view receives
    correct contact form data, the view correctly redirects and has a status
    code of 302 indicating redirection, and a target status of 200 meaning
    the view is rendered correctly.
```

> ### Views (Checkout App)
> ### Views (Community App)
> ### Views (Library App)
> ### Views (Marketing App)
> ### Views (Reader App)

> ### Forms (Blurb App)
### `class TestContactForm(TestCase):`
A class for testing the Contact Form associated with the Blurb app.
This form allows users to contact the Leaf Lounge team with queries.

`def test_contact_for_name_is_required():`
```Python
    Asserts the contact form is invalid without a name value.
    Asserts the error raised as a result of the empty value stems
    from the "name" key.
    Asserts the error raises matches the expected error.
```

`def test_contact_form_email_is_required():`
```Python
    Asserts the contact form is invalid without an email value.
    Asserts the error raised as a result of the empty value stems
    from the "email" key.
    Asserts the error raises matches the expected error.
```

`def test_contact_form_email_format_is_correct():`
```Python
    Asserts the contact form is invalid if the email value is of
    an incorrect format.
    Asserts the error raised as a result of the incorrectly-formatted
    value stems from the "email" key.
    Asserts the error raises matches the expected error.
```

`def test_contact_form_subject_is_required():`
```Python
    Asserts the contact form is invalid without a subject value.
    Asserts the error raised as a result of the empty value stems
    from the "subject" key.
    Asserts the error raises matches the expected error.
```

`def test_contact_form_message_is_required():`
```Python
    Asserts the contact form is invalid without a message value.
    Asserts the error raised as a result of the empty value stems
    from the "message" key.
    Asserts the error raises matches the expected error.
```

`def test_correctly_filled_form_is_valid():`
```Python
    Asserts a correctly filled form is valid.
```









> > > ## Issues

1. #### Contact Page `ConnectionRefusedError`
   ![Connection Refused Error](../../docs/images/connectionrefusederror.png)
   The error was encountered when attempting to send emails from the contact page. Instead of redirecting users to the home page with a success message, the application would throw the 500 Server Error page, and the email wouldn't reach the recipients' addresses.

> #### Solution

The issue was down to a simple typo in the following line in `blurb/views.py`: `recipient_list=[settings.EMAIL_HOST_USER, f'{email}'],` - the misplaced comma at the end. This syntax rendered the `recipient_list` as an invalid value in the `send_mail()` method, thus throwing the method and redirecting users to the 500 server error page. Removing the comma and saving the file resolved this issue. Testing and eventual resolution were done in `VS Code` by cloning the repository and debugging the relevant code due to Gitpod permissions and limitations.

> > > ## Accessibility & Performance

> > #### Lighthouse

- `Home Page`
![Home Page Lighthouse Report](../images/lighthouse-home.png)

- `Contact Page`
![Contact Page Lighthouse Report](../images/lighthouse-contact.png)
![Contact Accessibility Lighthouse Report](../images/lighthouse-contact-accessibility.png)

- `Library Page`
![Library Page Lighthouse Report](../images/lighthouse-library.png)
![Library Best Practices Lighthouse Report](../images/lighthouse-library-best-practices.png)

- `Basket Page`
![Basket Page Lighthouse Report](../images/lighthouse-basket.png)
![Basket Accessibility Lighthouse Report](../images/lighthouse-basket-accessibility.png)

- `Sign Up Page`
![Sign Up Page Lighthouse Report](../images/lighthouse-basket.png)

> > #### HTML Validation

> > #### CSS Validation

> > #### JSHint Validation

All js files are regularly validated during development using [JSHint](https://jshint.com/).

> > #### Pep8 Validation

All python files are regularly validated during development using the [Code Institute PEP8 Linter](https://pep8ci.herokuapp.com/).
