>>> ## Structure
- Navigation
  - Main Navigation Bar
    - Logo
    - Links
      - `Home`
      - `Contact`
      - `Library`
      - `My Communities` (if user is authenticated)
      - `My Profile` (if user is authenticated)
        - Billing Details
        - Order History
        - Communities (Community Page)
        - User Reviews
        - Help (Contact Page)
      - Basket
      - Authentication Links
        - `Sign Up` Button (if user is not authenthicated)
        - `Sign Out` Button (if user is authenticated)
  - Secondary Navigation Bar (visible only on some pages)
    - Breadcrumb Trail (visible only inside a book detail view)
    - Links
      - `My Books`
        - Registered Books
        - Purchased Books
          - Filter By Genre
      - `Become an Author`
        - Form for registering as a Leaf Lounge author
        - Form for registering books
    - Search Field

- Home Page
  - Jumbotron
    - Welcoming Header
    - `Sign In` Button (if user is not authenticated)
    - `My Communities` Button (if user is authenticated)
    - Search Field
    - Social Media Links
      - Facebook Page
      - Instagram (Personal)
      - Linkedin (Personal)

- Contact Page
  - Contact POIs
  - Contact Form
    - Validation
    - Messages-to-email
    - Success Message

- Library
  - Secondary Navigation Bar
    - `My Books` (as defined)
    - `Become an Author` (as defined)
  - Library Shelves
    - Books (links) Filtered by Genre (default)
  - Filtering Functionality
    - Authors
    - Genres
    - Both

- Book Detail
  - Breadcrumb Trail
  - Book Cover
  - Book Information
    - `Book Title`
    - `Dynamic Reviews`
    - General author information
    - `Book Blurb`
    - `About the Author` Text
  - `Add to Basket`
    - Book Type Selection Field
      - Softcover
      - Hardcover
      - Epub
    - Quantity Input Field
      - Buttons
      - Validation
    - Buttons
      - `Return to Library`
      - `Add to Basket`
  - `Reviews` (only visible if there are reviews)

- Basket
  - Content Table
    - `Book`
    - `Price/Book`
    - `Quantity`
      - `Update` Button
        - Input Field
          - Delete Button
          - Increment Button
        - Buttons
          - `Cancel`
          - `Save Changes`
    - `Subtotal`
  - Summary Breakdown
    - Subtotal
    - Delivery
    - Total
    - Buttons
      - `Secure Checkout`
      - `Keep Shopping`

- Checkout
  - Checkout Form
    - Stripe Card Input
    - T&Cs
  - Order Summary (same as basket)

- My Books
  - `My Books`
  - `My Purchases`
    - `Leave a Review` Button
  - Genre Buttons (filtering)

- Reviews
  - Review Form
  - Dynamic Rating Fill
  - Status Messages

- Become an Author
  - Author Registration Page
    - `Find My Profile`
  - Book Registration Page

- My Profile
  - `My Billing Details`
    - Billing Details Form
  - `My Order History`
    - Order Instance Accordion
      - Order Number
      - Date Placed
      - Books Ordered
      - Subtotal
      - Shipping
      - Total
      - Shipping Details (accordion)
  - `My Communities` (Community Page)
  - `My Reviews`
    - All user reviews
    - Buttons
      - `Edit` (if not admin approved)
      - `Delete`
  - `Need Help?` (Contact Page)

- Communities
  - User Community Tabs (Links)

- Community Detail
  - Forums
    - Forum Links
  - Other Books in the Genre

- Forum
  - Forum Chat
  - Forum Participants

- Footer
  - Newsletter
  - Links
    - `Home`
    - `Contact`
    - `Library`
    - `My Communities` (if user is authenticated)
    - `My Profile` (if user is authenticated)
    - Authentication Links
      - `Sign Up` Button (if user is not authenthicated)
      - `Sign Out` Button (if user is authenticated)
  - Copyright
    - Dynamic Year

>>> ## Models
Below is an ERD for `Leaf Lounge`'s db models.

![Leaf Lounge ERD](static/images/quickdbdiagrams.png)

>> #### The Author Model (library app)
Represents a Leaf Lounge author. Authors can register new books on the website, with new books being saved under their UserProfile.

Fields: `user_profile`, `first_name`, `last_name`, `d_o_b`, `nationality`, `bio`

1. `user_profile` : FK : Userprofile - represents the author's registered account. Authors without an account can be registered via admin only.
- Contraints:
  - _on-delete_: _models.SET-NULL_.
  - can be _null_.
  - can be _blank_.
  - _related-name_: _'author-profile'_.

2. `first_name` : CharField - represents the author's firstname.
- Constraints: 
  - _max-length_ : 20 characters.

3. `last_name` : CharField - represents the author's lastname.
- Constraints: 
  - _max-length_ : 20 characters.

4. `d_o_b` : DateField - represents the author's date of birth.
- Constraints: 
  - _default_ value of 'unknown'.
  - _verbose-name_ of 'BirthDate'.

5. `nationality` : CharField : choices - represents a selection field for the author's nationality.
- Constraints: 
  - predefined _choices_ from `NATIONALITIES` tuple.
  - _max-length_ : 30 characters.

6. `bio` : TextField - represents the author's bio.
- Constraints: 
  - _max-length_ : 500 characters.

###### Methods:
```Python
def __str__() -> str : (author's first name) (author's last name)
```

---

>> #### The Genre Model (library app)
Represents the breakdown of a book Genre. Each genre has an associated community, which is created at the same time as a new Genre is created. Each book registered on the app is given an associated Genre. After purchasing the book, the user gets access to the community associated with the genre.

Fields: `name`, `community`

1. `name` : CharField - represents the Genre name.
- Constraints: 
  - _max-length_ : 50 characters.
  - can not be _null_.
  - can not be _blank_.

2. `community` : FK : Community - rerpresents the Community the Genre belongs to.
- Constraints:
  - _on-delete_: _models.CASCADE_.
  - can be _null_.
  - can be _blank_.
  - help text : 'This field will be auto-filled after save.'
  - _related-name_: _'genre-community'_.

###### Methods:
```Python
def __str__() -> str : (genre name)
```

---

>> #### The Book Model (library app)
Represents a Book on Leaf Lounge. Books can be uploaded directly by admin, or registered on the website by registered Leaf Lounge authors. After selecting (clicking) on a book on the 'Library' page, users are taken into a detail view of that book. All books have associated reviews, genres, authors, and communities.

Fields: `title`, `isbn`, `slug`, `author`, `genre`, `blurb`, `year_published`, `publisher`, `type`, `date_added`, `price`, `image`

1. `title` : CharField - represents the book title.
- Constraints:
  - _max-length_ : 100 characters.

2. `isbn` : CharField - represents the book's Internation Standard Book Number.
- Constraints:
  - _max-length_ : 13 characters (all books after 2007 are 13 digits long, all before are 10 digits long).

3. `slug` : SlugField - represents the book slug (name-author fields).
- Constraints:
  - _max-length_ : 100 characters.
  - Can be _blank_.
  - Can be _null_.
  - Has _help text_ to explain why it can be left _blank_ and may be _null_.

4. `author` : FK : Author - represents the author of the book.

5. `genre` : CharField : choices - represents the book genre.
- Constraints:
  - predefined _choices_ from `GENRES` tuple.
  - _max-length_ : 50 characters.

6. `blurb` : TextField - represents the book blurb.
- Constraints:
  - _max-length_ : 500 characters.

7. `year_published` : IntegerField - represents the year the book was published.
- Constraints:
  - _MaxValueValidator_ : 2024.

8. `publisher` : CharField - represents the book publisher.
- Constraints:
  - _max-length_ : 100 characters.

9. `type` : CharField - represents the book cover type.

10. `date_added` : DateField - represents the date the book was added to the database.
- Constraints:
  - Adds current date.

11. `price` : DecimalField - represents the book price.
- Constraints:
  - _decimal-places_ : 2.
  - _max-digits_ : 5.

12. `image` : ImageField - represents the book cover image.
- Constraints:
  - Can be _blank_.
  - Can be _null_.

###### Methods:
```Python
def __str__() -> str : "(book title)" by (book author).
```

```Python
def save():
  try:
      Saves the concatenated `slug`.
      Additionally checks if the title of the book has been changed (if it no longer matches the one in the db).
      If true - re-saves the slug to match the new title-author concatenation.
  except `Book.DoesNotExist`:
      Catches the `DoesNotExist` error and saves the model as a new instance. This error was encountered when attempting to perform a similar action in a previous project.
```

```Python
def get_absolute_url(): returns the absolute url with the book 'slug' paramter (detail page).
```

###### Meta:
Orders by earliest date added.

---

>> #### The Review Model (library app)
Represents a book review. Reviews can be left by registered users, who have purchased at least one book. The link for this is under the 'My Books' tab in the secondary navigation bar. Reviews can be edited prior to approval, and deleted at any stage. Approved reviews are displayed on the relevant book detail page. Reviews are displayed as star fillings on all relevant pages.

Fields: `reviewer`, `book`, `title`, `rating`, `comment`, `reviewed_on`, `approved`

1. reviewer : FK : User - represents the user leaving the review.
- Constraints:
  - _on-delete_: _models.CASCADE_.
  - _related-name_: _'reviewer'_.

2. book : FK : Book - represents the book being reviewed.
- Constraints:
  - _on-delete_: _models.CASCADE_.
  - _related-name_: _'reviewed-book'_.

3. title : CharField - represents the review title.
- Constraints:
  - _max-length_ : 80 characters.
  - can not be _null_.
  - can not be _blank_.

4. rating : IntegerField - represents the book rating out of 10.
- Constraints:
  - _MinValueValidator_ : 1
  - _MaxValueValidator_ : 10
  - can not be _null_.
  - can not be _blank_.

5. comment : TextField - represents the user's verbal book rating.
- Constraints:
  - can not be _null_.
  - can not be _blank_.
  - _max-length_ : 500 characters.

6. reviewed_on : DateField - represents the date the review was left on.
- Constraints:
  - can not be _null_.
  - can not be _blank_.
  - _auto-now-add_ : `True`

7. approved : BooleanField - represents whether the comment is admin approved.
- Constraints:
  - default : `False`

---

>> #### The Order Model (checkout app)
Represents a user's book Order. Orders are placed via the checkout page. Order histories can be viewed under the 'My Profile' tab.

Fields: `order_number`, `user_profile`, `full_name`, `email`, `phone_number`, `country`, `postcode`, `town_city`, `street_1`, `street_2`, `county`, `date`, `delivery_cost`, `order_total`, `grand_total`, `original_basket`, `stripe_pid`

1. `order_number` : CharField - represents the auto-generated uuid order number.
- Constraints:
  - _max-length_ : 32 characters.
  - can not be _null_.
  - non-editable.

2. `user_profile` : FK : UserProfile - represents the profile to which the order belongs.
- Constraints: 
  -_on-delete_ : _MODELS.SET-NULL_
  - can be _null_.
  - can be _blank_.
  - _related-name_ : 'orders'

3. `full_name` : CharField - represents the full name associated with the order.
- Constraints:
  - _max-length_ : 50 characters.
  - can not be _null_.
  - can not be _blank_.

4. `email` : EmailField - represents the email associated with the order.
- Constraints:
  - _max-length_ : 254 characters.
  - can not be _null_.
  - can not be _blank_.

5. `phone_number` : CharField - represents the phone number associated with the order.
- Constraints:
  - _max-length_ : 20 characters.
  - can not be _null_.
  - can not be _blank_.

6. `country` : CharField - represents the country to which the order is to be posted.
- Constraints:
  - _max-length_ : 40 characters.
  - can not be _null_.
  - can not be _blank_.

7. `postcode` : CharField - represents the postcode associated with the order address.
- Constraints:
  - _max-length_ : 20 characters.
  - can be _null_.
  - can be _blank_.

8. `town_city` : CharField - represents the town/city to which the order is to be posted.
- Constraints:
  - _max-length_ : 40 characters.
  - can not be _null_.
  - can not be _blank_.

9. `street_1` : CharField - represents the first address line on the order.
- Constraints:
  - _max-length_ : 80 characters.
  - can not be _null_.
  - can not be _blank_.

10. `street_2` : CharField - represents the second address line on the order.
- Constraints:
  - _max-length_ : 80 characters.
  - can be _null_.
  - can be _blank_.

11. `county` : CharField - represents the county to which the order is to be posted.
- Constraints:
  - _max-length_ : 80 characters.
  - can be _null_.
  - can be _blank_.

12. `date` : DateTimeField - represents the date the order was placed.
- Constraints:
  - Adds current date.

13. `delivery_cost` : DecimalField - represents the delivery cost associated with the order.
- Constraints:
  - _max-digits_: 6.
  - _decimal-places_: 2.
  - can not be _null_.
  - _default_: 0

14. `order_total` : DecimalField - represents the total associated with the price/book and quantity.
- Constraints:
  - _max-digits_: 10.
  - _decimal-places_: 2.
  - can not be _null_.
  - _default_: 0.

15. `grand_total` : DecimalField - represents the order_total + delivery_cost.
- Constraints:
  - _max-digits_: 10.
  - _decimal-places_: 2.
  - can not be _null_.
  - _default_: 0.

16. `original_basket` : TextField - represents the order basket's original basket.
- Constraints:
  - can not be _null_.
  - can not be _blank_.
  - _default_: ''.

17. `stripe_pid` : CharField - represents the Stripe order pid.
- Constraints:
  - _max-length_ : 254 characters.
  - can not be _null_.
  - can not be _blank_.
  - _default_: ''.

###### Methods:
```Python
def _generate_uuid_order_number(): Generates a random, unique order number using UUID.
```

```Python
def save():
  try:
      Asserts whether an order number exists.
      Saves a new `order_number` from def _generate_uuid_order_number().
  except Order.DoesNotExist:
      Catches the DoesNotExist error and saves the model as a new
      instance.
```

```Python
def update_order_total():
  Updates `order_total`, `delivery_cost`, and `grand_total` based on order_total and quantity.
  Asserts whether the `order_total` is above the `FREE_DELIVERY_THRESHOLD`, as defined in settings.py.
  If above, assigns 0 to `delivery_cost`.
  If below, assigns 10% of `order_total` value as `delivery_cost`.
  Assigns `grand_total` the sum of `order_total` + `delivery_cost`.
```

```Python
def __str__() -> int : order number.
```

---

>> #### The BookLineItem Model (checkout app)
Represents a book lineitem for each book inside an order.

Fields: `order`, `book`, `type`, `quantity`, `book_order_cost`

1. `order` : FK : Order - represents the book order.
- Constraints:
  - can not be _null_.
  - can not be _blank_.
  - _on-delete_: _models.CASCADE_.
  - _related-name_: _'booklineitem'_.

2. `book` : FK : Book - represents the book instance that was ordered.
- Constraints:
  - can not be _null_.
  - can not be _blank_.
  - _on-delete_: _models.CASCADE_.

3. `type` : CharField - represents the book cover type.
- Constraints:
  - _max-length_ : 9 characters.
  - can not be _null_.
  - can not be _blank_.

4. `quantity` : IntegerField - represents the quantity that was ordered.
- Constraints:
  - can not be _null_.
  - can not be _blank_.
  - _default_: 0.

5. `book_order_cost` : DecimalField - represents the total cost for the book order instance.
- Constraints:
  - _max-digits_: 5.
  - can not be _null_.
  - can not be _blank_.
  - _decimal-places_: 2.
  - non-editable.

###### Methods:
```Python
def save(): Assigns the total lineitem cost based on price/unit and quantity if not already assigned.
```

```Python
def __str__() -> str : 'ISBN: (book ISBN), order: (order number uuid)'.
```

---

>> #### The Community Model (community app)
Represents a genre community where users can access forums, chats and messages. Users are granted access to the community matching the book genre after making purchasing a book in that genre.

Fields: `name`, `description`, `slug`, `image`

1. `name` : CharField - represents the name of the community. 
- Constraints: 
  - _max-length_ : 80 characters.
  - can not be _null_.
  - can not be _blank_.

2. `description` : TextField - represents the community intro/description.
- Constraints: 
  - _max-length_ : 500 characters.
  - can be _null_.
  - can be _blank_.

3. `slug` : SlugField - represents the community slug.
- Constraints:
  - can be _blank_.
  - can not be _null_.

4. `image` : ImageField - represents the community header image.
- Constraints: 
  - can be _null_.
  - can be _blank_.

```Python
def __str__() -> str : (community name)
```

---


>> #### The Forum Model (community app)
Represents a community forum. Each community can have multiple forums. All users inside the community have full access to forums in the community, and users may create new forums inside the community for chats and networking.

Fields: `name`, `slug`, `date_created`, `community`

`name` : CharField - represents the forum name.
- Constraints:
  - _max-length_ : 50 characters.
  - can not be _null_.
  - can not be _blank_.

`slug` : SlugField - represents the forum slug as name-community-id.
- Constraints:
  - _max-length_ : 50 characters.
  - can be _null_.
  - can be _blank_.

`date_created` : DateField - represents the date the forum was created on.
- Constraints:
  - _auto-now-add_ : `True`

`community` : FK : Community - represents the forum community.
- Constraints:
  - _on-delete_: _models.CASCADE_.
  - _related-name_: _'community-forums'_.

###### Methods:
```Python
def __str__(): Returns -> (str) (forum name)
```

```Python
def save():
  try:
    Saves the model.
    Two-step saves a custom url to the (self.slug) parameter as (forum title)-(forum community)-(forum id).
  except `Forum.DoesNotExist`:
    Catches the `DoesNotExist` error and saves the model as a new instance.
```
```Python
def get_absolute_url(): Returns -> the forum detail page with (self.slug) as url argument.
```

---

>> #### The Message Model (community app)
Represents a message within a community forum. Messages can be viewed by all members of the forum, but can only be deleted by the user who sent the message.

Fields: `forum`, `content`, `messenger`, `date_sent`

1. `forum`: FK : Forum - represents the forum to which the message belongs.
- Constraints:
  - _on-delete_: _models.CASCADE_.
  - _related-name_: _'forum-messages'_.

2. `content` : CharField - represents the message content.
- Constraints:
  - _max-length_ : 1000 characters.
  - can not be _null_.
  - can not be _blank_.

3. `messenger` : FK : UserProfile - represents the user author of the message.
- Constraints:
  - _on-delete_: _models.CASCADE_.
  - _related-name_: _'user-messenger'_. 

4. `date_sent` : DateField - represents the date the message was sent on.
- Constraints:
  - _auto-now-add_ : `True`

###### Methods:
```Python
def __str__() -> str : "Message in '(forum name)'"
```

---

>> #### The UserProfile Model (reader app)
A user profile for maintaining default delivery information, order history, and saved books.

Fields: `user`, `default_street_1`, `default_street_2`, `default_town_city`, `default_county`, `default_postcode`, `default_country`


1. user : OneToOneField : User - represents the user to whom the profile belongs.
  - Constraints:
    - _on-delete_: _models.CASCADE_.

2. default_phone_number - represents the user's saved phone number.
- Constraints:
  - _max-length_ : 20 characters.
  - can be _null_.
  - can be _blank_.

3. default_street_1 : CharField - represents the saved default street address.
- Constraints:
  - _max-length_ : 80 characters.
  - can be _null_.
  - can be _blank_.

4. default_street_2 : CharField - represents the saved default street address.
- Constraints:
  - _max-length_ : 80 characters.
  - can be _null_.
  - can be _blank_.

5. default_town_city : CharField - represents the saved default town/city address.
- Constraints:
  - _max-length_ : 40 characters.
  - can be _null_.
  - can be _blank_.

6. default_county : CharField - represents the saved default county address.
- Constraints:
  - _max-length_ : 80 characters.
  - can be _null_.
  - can be _blank_.

7. default_postcode : CharField - represents the saved default postcode address.
- Constraints:
  - _max-length_ : 20 characters.
  - can be _null_.
  - can be _blank_.

8. default_country : Field - represents the saved default country address.
- Constraints:
  - _blank-label_ : 'Country'.
  - can be _null_.
  - can be _blank_.

###### Methods:
```Python
def __str__() -> str : (user's username)
```
