from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponseRedirect, reverse
from django.views import View
from djropbox.user.forms import SignupForm
from djropbox.user.models import BoxUser
from djropbox.file_uploader.models import Folder


def signup_user(request):
    form = None
    html = '../templates/main.html'
    header = 'Signup'
    button_val = 'Signup'

    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(
                username=data['username'], password=data['password']
            )
            login(request, user)
            boxuser = BoxUser.objects.create(
                username=data['username'],
                user=user
            )
            Folder.objects.create(
                name="home",
                creator=boxuser
            )
            return HttpResponseRedirect(request.GET.get('next', '/'))

    else:
        form = SignupForm()

    return render(request, html, {'header': header, 'form': form,
                                  'button_val': button_val})