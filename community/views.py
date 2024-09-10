from django.shortcuts import render, redirect, reverse
from django.shortcuts import get_object_or_404, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Community
from library.models import Genre, Author, Book
from reader.models import UserProfile
from checkout.models import Order

from .forms import *

import datetime


@login_required
def community_general(request):
    """
    This view retrieves and displays a user's communities. Each community in
    this view links to a dedicated community view.

    The user's communities' access is defined by the genres from previously
    purchased booklinitems. If there are no booklineitems in the user's order
    history, the view renders the same template with a dedicated context and
    relevant, relevant information header, and redirection links.

    Returns:
    Render: If there are booklineitems, renders the communities page with the
    relevant list of communities for iteration within the template.
    Render: If there are no booklineitems, renders the communities page with a
    template variable.
    """
    user_profile = UserProfile.objects.get(user=request.user)
    user_orders = Order.objects.filter(user_profile=user_profile)

    # Retrieve orders + communities.
    user_booklineitems = []
    for order in user_orders:
        books = order.booklineitem.all()
        user_booklineitems.extend(books)

    user_genres = []
    for item in user_booklineitems:
        if item.book.genre not in user_genres:
            user_genres.append(item.book.genre)

    user_communities = []
    for genre in user_genres:
        if genre.community not in user_communities:
            user_communities.append(genre.community)

    # Handle registered user with no book orders.
    if not user_booklineitems:
        context = {
            'no_user_booklineitems': True
        }
        return render(
            request,
            'community/community.html',
            context
        )
    else:
        context = {
            'user_communities': user_communities,
        }

        return render(
            request,
            'community/community.html',
            context
        )


@login_required
def community(request, slug):
    """
    This view is responsible for retrieving and displaying the details of a
    specific community, including related forums and books within this genre,
    and allows users to create new forums within that community. If the
    appropriate community is not found, the view displays a 404 page.

    This view retrieves and displays the details of a community based on the
    provided slug. Users may create new forums within the community, or
    participate in the existing. If the request method is POST, the view
    processes the submitted forum creation form and, if valid, saves the forum
    to the community. Following successful forum creation, the user is
    redirected inside the new forum. Error messages are displayed if the forum
    creation fails or if any form fields are invalid.

    Only authenticated users can access this view, as indicated by the
    @login_required decorator.

    Additional Parameters:
    slug (str): The slug of the community to be retrieved and displayed.

    Returns:
    Renders: Renders the community detail page.
    Redirect: Following successful forum creation, redirects to the forum
    detail view with a success message.
    Redirect: Following unsuccessful forum creation, redirects to the community
    detail view with an informative error message.

    Decorators:
    @login_required: Ensures only authenticated users can access the view.
    """
    community = get_object_or_404(Community, slug=slug)

    # Other Books in this Genre.
    current_genre = get_object_or_404(Genre, community=community)
    # Add .exclude to filter out books user already owns?
    books_in_genre = Book.objects.filter(genre=current_genre)
    forums = Forum.objects.filter(community=community)

    user_profile = UserProfile.objects.get(user=request.user)
    user_orders = Order.objects.filter(user_profile=user_profile)

    if request.method == 'POST':
        forumForm = ForumForm(data=request.POST)
        if forumForm.is_valid():
            try:
                forum = forumForm.save(commit=False)
                forum.community = community
                forum.save()
                messages.success(
                    request,
                    "Successfully created your forum!"
                )
                return redirect(reverse('forum_detail', args=[forum.slug]))
            except Forum.community.RelatedObjectDoesNotExist:
                messages.error(
                    request,
                    """An error occurred while trying to create your
                    discussion. If the error persists, please get in
                    touch with our dedicated customer support team to
                    resolve this issue.
                    Thank you for your understanding!
                    """
                )
                return redirect(reverse('community', args=[slug]))
        else:
            messages.error(
                request,
                "Please enter a valid name for your forum."
            )
    forumForm = ForumForm()

    context = {
        'forums': forums,
        'forumForm': forumForm,
        'books_in_genre': books_in_genre,
        'current_genre': current_genre,
        'community': community,
        'community_view': True,
    }

    return render(
        request,
        'community/community_detail.html',
        context
    )


def forum_detail(request, slug):
    """
    This view is responsible for retrieving and displaying the details of a
    user-created community forum, including the message form, and active
    participants. If the appropriate forum is not found, the view displays a
    404 page.

    If the request method is POST, the view processes the submitted message
    form, and, if valid, redirects the user to the form and saves the message
    to the forum. Error messages are displayed if the message does not send.

    Additional Parameters:
    slug (str): The slug of the forum to be retrieved and displayed.

    Returns:
    HttpResponseRedirect: Redirects to the forum detail page.
    Render: Renders the forum detail page.
    """
    forum = get_object_or_404(Forum, slug=slug)
    user_profile = UserProfile.objects.get(user=request.user)
    forum_messages = Message.objects.filter(forum=forum)
    todays_date = datetime.date.today()

    if forum_messages:
        last_message = forum_messages.latest('date_sent').date_sent
    else:
        last_message = None

    forum_participants = []
    for message in forum_messages:
        if message.messenger not in forum_participants:
            forum_participants.append(message.messenger)
    
    for participant in forum_participants:
        first_member_message = Message.objects.filter(messenger=participant).first()
        participant.first_message = first_member_message

    if request.method == 'POST':
        message_form = MessageForm(data=request.POST)
        if message_form.is_valid():
            try:
                message = message_form.save(commit=False)
                message.forum = forum
                message.messenger = user_profile
                message.save()
                message_form.save()
                messages.success(
                    request,
                    "Your message has been sent!"
                )
                # PRG Pattern.
                return HttpResponseRedirect(
                    reverse('forum_detail', args=[slug])
                )
            except Exception as e:
                messages.error(
                    request,
                    """An error occurred while trying to send your message.
                    If the error persists, please get in touch with our
                    dedicated customer support team to resolve
                    this issue.
                    Thank you for your understanding!"""
                )
                print(f'{e}')
                return HttpResponseRedirect(
                    reverse('forum_detail', args=[slug])
                )
        else:
            messages.error(
                request,
                """
                Please double check your message for errors and try again.
                If the error persists, please get in touch with our
                dedicated customer support team to resolve this issue.
                Thank you for your understanding!
                """
            )
            return HttpResponseRedirect(
                reverse('forum_detail', args=[slug])
            )
    message_form = MessageForm()

    context = {
        'forum': forum,
        'user_profile': user_profile,
        'forum_participants': forum_participants,
        'forum_messages': forum_messages,
        'message_form': message_form,
        'todays_date': todays_date,
        'last_message': last_message,
    }
    return render(
        request,
        'community/forum_detail.html',
        context
    )


def delete_message(request, slug, id):
    """
    This view handles the deletion of messages from community forums.

    Prior to deleting the message, the view checks whether the
    message author id matches that of the user requesting deletion.
    If the IDs match, the message is deleted from the forum and database,
    and the user is redirected back to the forum_detail page with an
    informative success message. If not, the user is redirected to the
    forum_detail with an error message.
    """
    message_delete = get_object_or_404(Message, id=id)
    if message_delete.messenger.id == request.user.id:
        message_delete.delete()
        messages.success(
            request,
            "Your message was successfully deleted!"
        )
    else:
        messages.error(
            request,
            """You do not have permission to delete this message.
            If this is a mistake, please contact our dedicated support team
            to get this issue resolved."""
        )
    return HttpResponseRedirect(reverse('forum_detail', args=[slug]))


def create_author(request):
    """
    This view is responsible for allowing users to register as Leaf
    Lounge authors. After registration, users are redirected to the
    book registration page.

    The view checks for a UserProfile belonging to the user. If the
    profile is found, it associates the author information with their
    existing profile; otherwise, it creates a new profile. Author
    registry needs to be completed once only, and users wishing to
    register several books can click 'find my profile' at the top of
    the author_form displayed in the view.

    This view handles logic for the author's age during registery.
    If the user's age is outside the allowed range (under 16 or
    over 99), an appropriate error message is displayed, and
    they are redirected back to the homepage. The form is
    re-rendered if there are any validation errors or if
    the request is a GET request.

    POST Data:
    Fields for author details: first_name, last_name, d_o_b, nationality,
    and bio.

    Returns:
    HttpResponse: Renders the author registration page with the author_form.
    HttpResponseRedirect: Redirects to the book registration page
    upon successful registration or back to the homepage on age restriction.
    """
    if request.user.username != 'AnonymousUser':
        # Check for existing profiles before creating new.
        profile_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                p = UserProfile.objects.get(
                    user=request.user
                )
                profile_exists = True
                break
            except UserProfile.DoesNotExist:
                attempt += 1
                time.sleep(1)

    if request.method == 'POST':
        author_form = AuthorForm(data=request.POST)
        if author_form.is_valid():
            user = UserProfile.objects.get(user=request.user)
            firstname = author_form.cleaned_data['first_name']
            lastname = author_form.cleaned_data['last_name']
            d_o_b = author_form.cleaned_data['d_o_b']
            nationality = author_form.cleaned_data['nationality']
            bio = author_form.cleaned_data['bio']

            today = datetime.date.today()
            age = (today-d_o_b).days / 365.25
            if age > 16 and age < 100:
                if profile_exists:
                    print('EXISTS')
                    Author.objects.create(
                        user_profile=user,
                        first_name=f'{firstname}',
                        last_name=f'{lastname}',
                        d_o_b=f'{d_o_b}',
                        nationality=f'{nationality}',
                        bio=f'{bio}',
                    )
                else:
                    print('trying to create new profile')
                    new_profile = UserProfile.objects.create(
                        user=request.user
                    )
                    print('created new profile!')
                    Author.objects.create(
                        user_profile=new_profile,
                        first_name=f'{firstname}',
                        last_name=f'{lastname}',
                        d_o_b=f'{d_o_b}',
                        nationality=f'{nationality}',
                        bio=f'{bio}'
                    )
                    print('created author from new profile!')
                messages.success(
                    request,
                    """Success! Now let's register your book :)"""
                )
                return redirect('upload_book')
            elif age > 100:
                messages.error(
                    request,
                    """Our policy does not allow persons over 99 to register!
                    :(
                    If this is a mistake, please contact our team directly to
                    verify your attempt and we'll get you set up :)\n We
                    apologise for any inconvenience caused."""
                )
            else:
                messages.error(
                    request,
                    """Our policy does not allow persons under 16 to register!
                    :(
                    If this is a mistake, please contact our team directly to
                    verify your attempt and we'll get you set up :)\n We
                    apologise for any inconvenience caused."""
                )
            return redirect('home')
    else:
        author_form = AuthorForm()
        context = {
            'authorForm': author_form,
            'profile_exists': profile_exists,
        }
        return render(
            request,
            'community/create_author.html',
            context
        )


def upload_book(request):
    """
    This view handles the book registration process performed
    by registered Leaf Lounge authors. Following successful
    registration, the user is redirected to their books page,
    where they may view the new addition. If the registration
    is unsuccessful, the user is redirected home with an error
    message.
    """
    profile = UserProfile.objects.get(user=request.user)
    author = get_object_or_404(Author, user_profile=profile)
    if request.method == 'POST':
        book_form = BookForm(data=request.POST)
        if book_form.is_valid():
            book = book_form.save(commit=False)
            book.author = author
            book.save()
            messages.success(
                request,
                """Your book has been registered successfully!
                You may view it under 'My Books' :)"""
            )
            return redirect('user_books')
        else:
            messages.error(
                request,
                """We are unable to register your book at this
                time. If the error persists, please get in touch
                with our dedicated customer support team to resolve
                this issue.
                Thank you for your understanding!"""
            )
            return redirect('home')
    else:
        book_form = BookForm()

    context = {
        'bookForm': book_form,
    }
    return render(
        request,
        'community/upload_book.html',
        context
    )
