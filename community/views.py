from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .forms import AuthorForm
from .models import Community
from library.models import Genre
from reader.models import UserProfile
from checkout.models import Order


def community_general(request):
    """
    A view for displaying each community.
    """
    user_profile = UserProfile.objects.get(user=request.user)
    user_orders = Order.objects.filter(user_profile=user_profile)

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

    context = {
        'community': community,
        'community_view': True,
    }

    return render(
        request,
        'community/community_detail.html',
        context
    )


def sell_books(request):

    if request.method == 'POST':
        print('POST')
        author_form = AuthorForm(data=request.POST)
        if author_form.is_valid():
            print('VALID')
        else:
            print('NOT VALID')
            author_form = AuthorForm()
            messages.error(
                request,
                'Please double check your information and try again'
            )
        return redirect('sell_books')
    else:
        print('NOT POST')
        author_form = AuthorForm()
        context = {
            'authorForm': author_form,
        }
        return render(
            request,
            'community/sell_books.html',
            context
        )