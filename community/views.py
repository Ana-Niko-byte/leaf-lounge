from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponseRedirect
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
    A view for displaying each community.
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
        return render(
            request,
            'community/no_communities.html',
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
    A view for each community.
    """
    community = Community.objects.get(slug=slug)

    # Other Books in this Genre.
    current_genre = Genre.objects.get(community=community)
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
                    'Successfully created your forum!'
                )
                return redirect(reverse('community', args=[slug]))
            except Forum.community.RelatedObjectDoesNotExist:
                messages.error(
                    request,
                    '''An error occurred while trying to create your
                    discussion. Please try again in a later while or contact
                    our customer service department.\n
                    We apologise for any inconvenience caused.'''
                )
                return redirect(reverse('community', args=[slug]))
        else:
            messages.error(
                request,
                'Please enter a valid name for your discussion.'
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
    A dedicated view for each forum.
    """
    forum = Forum.objects.get(slug=slug)
    user_profile = UserProfile.objects.get(user=request.user)
    forum_messages = Message.objects.filter(forum=forum)
    todays_date = datetime.date.today()

    forum_participants = []
    for message in forum_messages:
        if message.messenger not in forum_participants:
            forum_participants.append(message.messenger)

    if request.method == 'POST':
        messageForm = MessageForm(data=request.POST)
        if messageForm.is_valid():
            try:
                message = messageForm.save(commit=False)
                message.forum = forum
                message.messenger = user_profile
                message.save()
                messageForm.save()
                messages.success(
                    request,
                    'Your message has been sent!'
                )
                # PRG Pattern.
                return HttpResponseRedirect(reverse('forum_detail', args=[slug]))
            except Exception as e:
                print(f'an error occurred: {e}')
                messages.error(
                    request,
                    'An error has occurred.'
                )
    messageForm = MessageForm()

    context = {
        'forum': forum,
        'user_profile': user_profile,
        'forum_participants': forum_participants,
        'forum_messages': forum_messages,
        'messageForm': messageForm,
        'todays_date': todays_date
    }
    return render(
        request,
        'community/forum_detail.html',
        context
    )


def delete_message(request, slug, id):
    """
    A view for deleting messages.
    """
    try:
        message_delete = Message.objects.get(id=id)
        if message_delete.messenger.id == request.user.id:
            message_delete.delete()
            messages.success(
                request,
                'Your message was successfully deleted!'
            )
    except Exception as e:
        print(f'{e}')
    return HttpResponseRedirect(reverse('forum_detail', args=[slug]))


def create_author(request):
    """
    A view for users to register themselves as authors.
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
                    bio=f'{bio}'
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
                    """We're sorry but our policy does not allow persons over 99 to register! :(
                    If this is a mistake, please contact our team directly to verify
                    your attempt and we'll get you set up :)\n We apologise for any inconvenience caused."""
                )
            else:
                messages.error(
                    request,
                    """We're sorry but our policy does not allow persons under 16 to register! :("""
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
    A view for registered authors to upload books.
    """
    profile = UserProfile.objects.get(user=request.user)
    author = Author.objects.get(user_profile=profile)
    if request.method == 'POST':
        book_form = BookForm(data=request.POST)
        if book_form.is_valid():
            book = book_form.save(commit=False)
            book.author=author
            book.save()
        else:
            print('INVALID')
    else:
        print('NOT POST')
    book_form = BookForm()

    context = {
        'bookForm': book_form,
    }
    return render(
        request,
        'community/upload_book.html',
        context
    )
