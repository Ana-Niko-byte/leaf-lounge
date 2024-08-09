from django.http import JsonResponse


def send_view(request):
    return JsonResponse({
        'detail': 'This view is going to send an email.',
    })