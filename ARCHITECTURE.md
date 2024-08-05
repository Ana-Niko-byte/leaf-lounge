## Structure
- Navigation
  - Main Navigation Bar
    - Logo
    - Links
      - `Home`
      - `Contact`
      - `Library`
      - `My Communities` (if user is authenticated)
      - Basket
      - Authentication Links
        - `Sign Up` Button (if user is not authenthicated)
        - `Sign Out` Button (if user is authenticated)
  - Secondary Navigation Bar (visible only on some pages)
    - Breadcrumb Trail
    - Links
      - `My Books`
      - `My Profile`
      - `Become an Author`
    - Search Bar

- Home Page
  - Jumbotron
    - Welcoming Header
    - `Sign In` Button
  
___TBD___

- Contact Page
  - Contact POIs (visible on large screens only)
  - Contact Form
    - Validation
    - Messages-to-email-address
    - Success Message

- Library
  - Secondary Navigation Bar
  - All Books
    - `Read More` Button

- Book Detail Pages
  - Book View
  - `About the Author` Text
  - `Book Blurb`
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
    - `Read Reviews`

- Basket
  - Content Table
    - Book
    - Price
    - Quantity
      - `Update Quantity` Button
        - Input Field
          - Delete Button
          - Increment Button
        - `Cancel` Button
        - `Save Changes` Button
    - Subtotal
  - Total Summary + Breakdown
  - `Keep Shopping` Button
  - `Secure Checkout` Button

- Checkout
  - Checkout Form
    - Stripe Card Input
  - Order Summary

- Reviews
- Community

- Footer
  - Links
    - `Home`
    - `Contact`
    - `Library`
    - `My Communities` (if user is authenticated)
    - Basket
    - Authentication Links
      - `Sign Up` Button (if user is not authenthicated)
      - `Sign Out` Button (if user is authenticated)
  - Newsletter
  - Copyright
    - Dynamic Year

## Models
Below is a simple ERD for `moment`'s models.

![Leaf Lounge ERD]()

#### The Author Model (library app)
Fields: `first_name`, `last_name`, `d_o_b`, `nationality`, `bio`

1. `first_name` : CharField - represents the author's firstname.
- Constraints: 
  - _max-length_ of 20 characters.

2. `last_name` : CharField - represents the author's lastname.
- Constraints: 
  - _max-length_ of 20 characters.

3. `d_o_b` : DateField - represents the author's date of birth.
- Constraints: 
  - _default_ value of 'unknown'.
  - _verbose-name_ of 'BirthDate'.

4. `nationality` : CharField : choices - represents a selection field for the author's nationality.
- Constraints: 
  - predefined _choices_ from `NATIONALITIES` tuple.
  - _max-length_ of 30 characters.

5. `bio` : TextField - represents the author's bio.
- Constraints: 
  - _max-length_ of 500 characters.

###### Methods:
```Python
def __str__(): Returns : (str) : '(author's first name) (author's last name)'
```

---

#### The Book Model (library app)
Fields: `title`, `isbn`, `slug`, `author`, `genre`, `blurb`, `year_published`, `publisher`, `rating`, `type`, `date_added`, `price`, `image`

1. `title` : CharField - represents the book title.
- Constraints:
  - _max-length_ of 100 characters.

2. `isbn` : CharField - represents the book's Internation Standard Book Number.
- Constraints:
  - _max-length_ of 13 characters (all books after 2007 are 13 digits long, all before are 10 digits long).

3. `slug` : SlugField - represents the book slug (name-author fields).
- Constraints:
  - _max-length_ of 100 characters.
  - Can be left _blank_.
  - Can be _null_.
  - Has _help text_ to explain why it can be left _blank_ and may be _null_.

4. `author` : FK : Author - represents the author of the book.

5. `genre` : CharField : choices - represents the book genre.
- Constraints:
  - predefined _choices_ from `GENRES` tuple.
  - _max-length_ of 50 characters.

6. `blurb` : TextField - represents the book blurb.
- Constraints:
  - _max-length_ of 500 characters.

7. `year_published` : IntegerField - represents the year the book was published.
- Constraints:
  - _MaxValueValidator_ : 2024.

8. `publisher` : CharField - represents the book publisher.
- Constraints:
  - _max-length_ of 100 characters.

9. `rating` : DecimalField - represents the book rating (out of 10).
- Constraints:
  - _decimal-places_ : 2.
  - _MinValueValidator_ of 0.01 with message.
  - _max-digits_ : 3.

10. `type` : CharField - represents the book cover type.

11. `date_added` : DateField - represents the date the book was added to the database.
- Constraints:
  - Adds current date.

12. `price` : DecimalField - represents the book price.
- Constraints:
  - _decimal-places_ : 2.
  - _max-digits_ : 5.

13. `image` : ImageField - represents the book cover image.
- Constraints:
  - Can be left _blank_.
  - Can be _null_.

###### Methods:
```Python
def __str__(): Returns "(book title)" by (book author).
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

#### The Order Model (checkout app)
Fields: `order_number`, `full_name`, `email`, `phone_number`, `country`, `postcode`, `town_city`, `street_1`, `street_2`, `county`, `date`, `delivery_cost`, `order_total`, `grand_total`

1. `order_number` : CharField - represents the auto-generated uuid order number.
- Constraints:
  - _max-length_ of 32 characters.
  - can not be _null_.
  - non-editable.

2. `full_name` : CharField - represents the full name associated with the order.
- Constraints:
  - _max-length_ of 50 characters.
  - can not be _null_.
  - can not be _blank_.

3. `email` : EmailField - represents the email associated with the order.
- Constraints:
  - _max-length_ of 254 characters.
  - can not be _null_.
  - can not be _blank_.

4. `phone_number` : CharField - represents the phone number associated with the order.
- Constraints:
  - _max-length_ of 20 characters.
  - can not be _null_.
  - can not be _blank_.

5. `country` : CharField - represents the country to which the order is to be posted.
- Constraints:
  - _max-length_ of 40 characters.
  - can not be _null_.
  - can not be _blank_.

6. `postcode` : CharField - represents the postcode associated with the order address.
- Constraints:
  - _max-length_ of 20 characters.
  - can be _null_.
  - can be _blank_.

7. `town_city` : CharField - represents the town/city to which the order is to be posted.
- Constraints:
  - _max-length_ of 40 characters.
  - can not be _null_.
  - can not be _blank_.

8. `street_1` : CharField - represents the first address line on the order.
- Constraints:
  - _max-length_ of 80 characters.
  - can not be _null_.
  - can not be _blank_.

9. `street_2` : CharField - represents the second address line on the order.
- Constraints:
  - _max-length_ of 80 characters.
  - can be _null_.
  - can be _blank_.

10. `county` : CharField - represents the county to which the order is to be posted.
- Constraints:
  - _max-length_ of 80 characters.
  - can be _null_.
  - can be _blank_.

11. `date` : DateTimeField - represents the date the order was placed.
- Constraints:
  - Adds current date.

12. `delivery_cost` : DecimalField - represents the delivery cost associated with the order.
- Constraints:
  - _max-digits_: 6.
  - _decimal-places_: 2.
  - can not be _null_.
  - _default_: 0

13. `order_total` : DecimalField - represents the total associated with the price/book and quantity.
- Constraints:
  - _max-digits_: 10.
  - _decimal-places_: 2.
  - can not be _null_.
  - _default_: 0.

14. `grand_total` : DecimalField - represents the order_total + delivery_cost.
- Constraints:
  - _max-digits_: 10.
  - _decimal-places_: 2.
  - can not be _null_.
  - _default_: 0.

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
def __str__():` Returns : (int) : order number.
```

---

#### The BookLineItem Model (checkout app)
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
  - _max-length_ of 9 characters.
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
def __str__(): Returns : (str) : 'ISBN: (book ISBN), order: (order number uuid)'.
```

## Views & Templates