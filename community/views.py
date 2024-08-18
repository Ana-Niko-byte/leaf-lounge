from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponseRedirect
from django.contrib import messages

from .models import Community
from library.models import Genre, Author, Book
from reader.models import UserProfile
from checkout.models import Order

from .forms import *

import datetime


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


def community(request, slug):
    """
    A view for displaying each community.
    """
    community = Community.objects.get(slug=slug)

    # Other Books in this Genre.
    current_genre = Genre.objects.get(community=community)
    books_in_genre = Book.objects.filter(genre=current_genre)

    forums = Forum.objects.all()

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
    forum = Forum.objects.get(slug=slug)
    slug = forum.slug
    try:
        message_delete = Message.objects.get(id=id)
        message_delete.delete()
        messages.success(
            request,
            'Your message was successfully deleted!'
        )
    except Exception as e:
        print(f'{e}')
    return redirect(reverse('forum_detail', args=[slug]))


def create_author(request):
    """
    """
    if request.method == 'POST':
        author_form = AuthorForm(data=request.POST)
        if author_form.is_valid():
            user = UserProfile.objects.get(user=request.user)
            firstname = author_form.cleaned_data['first_name']
            lastname = author_form.cleaned_data['last_name']
            d_o_b = author_form.cleaned_data['d_o_b']
            nationality = author_form.cleaned_data['nationality']
            bio = author_form.cleaned_data['bio']
            if request.user.username != 'AnonymousUser':
                Author.objects.create(
                    user_profile=user,
                    first_name=f'{firstname}',
                    last_name=f'{lastname}',
                    d_o_b=f'{d_o_b}',
                    nationality=f'{nationality}',
                    bio=f'{bio}'
                )
            else:
                # For authors that don't have an account - loaded.
                Author.objects.create(
                    user_profile=None,
                    first_name=f'{firstname}',
                    last_name=f'{lastname}',
                    d_o_b=f'{d_o_b}',
                    nationality=f'{nationality}',
                    bio=f'{bio}'
                )
            messages.success(
                request,
                'Successfully created Author!'
            )
            return redirect('upload_book')
        else:
            author_form = AuthorForm()
            messages.error(
                request,
                'Please double check your information and try again'
            )
        return redirect('sell_books')
    else:
        author_form = AuthorForm()
        context = {
            'authorForm': author_form,
        }
        return render(
            request,
            'community/create_author.html',
            context
        )


def upload_book(request):
    """
    """
    if request.method == 'POST':
        book_form = BookForm(data=request.POST)
        if book_form.is_valid():
            print('VALID')
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
