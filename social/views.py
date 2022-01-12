from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView

from .decorators import signin_required
from .forms import RegisterForm, LoginForm, ProfileForm, ContactFormEmail
from .models import User, Profile, Relationship


class SignUp(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'SignUp.html'

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            profile, created = Profile.objects.get_or_create(user=user)

        return redirect('/social/signin')


class UserLogin(View):
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        context = {'form': form}
        return render(request, 'SignIn.html', context)

    def post(self, request):
        form = LoginForm()
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/posts/timeline')
        else:
            return render(request, 'SignIn.html', {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/social/signin')


@method_decorator(signin_required, name="dispatch")
class ProfileDetailView(UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'profile.html'
    success_url = '/posts/timeline'
    pk_url_kwarg = 'id'


@method_decorator(signin_required, name="dispatch")
class ProfileView(DetailView):
    model = Profile
    template_name = 'profileview.html'


@method_decorator(signin_required, name="dispatch")
class ListFriends(ListView):
    model = Profile
    template_name = 'friends.html'
    context_object_name = 'users'

    def get_queryset(self):
        return Profile.objects.exclude(user=self.request.user).exclude(user__is_superuser=True)


@method_decorator(signin_required, name="dispatch")
class SendRequest(View):
    def get(self, request, id, *args, **kwargs):
        sender = self.request.user.profile
        receiver = Profile.objects.get(id=id)
        try:
            friend_request, created = Relationship.objects.get_or_create(sender=sender, receiver=receiver,
                                                                         status='sent')
            if not created:
                messages.error(request, 'Already sent')
            else:
                friend_request.save()
                messages.success(request, 'Request sent')
        except:
            messages.error(request, 'Already sent ')
        return redirect('/social/friends')


@method_decorator(signin_required, name="dispatch")
class RemoveRequest(View):
    def get(self, request, id, *args, **kwargs):
        sender = self.request.user.profile
        receiver = Profile.objects.get(id=id)
        friend_request = Relationship.objects.get(sender=sender, receiver=receiver)
        friend_request.delete()
        messages.error(request, 'Request removed')
        return redirect('/social/friends')


@method_decorator(signin_required, name="dispatch")
class ListRequests(ListView):
    model = Relationship
    template_name = 'requests.html'
    context_object_name = 'friend_requests'

    def get_queryset(self):
        return Relationship.objects.filter(receiver=self.request.user.profile)


@method_decorator(signin_required, name="dispatch")
class AcceptRequest(View):
    def get(self, request, id, *args, **kwargs):
        friend_request = Relationship.objects.get(id=id)
        friend_request.sender.user.friends.add(friend_request.receiver)
        friend_request.receiver.user.friends.add(friend_request.sender)
        messages.success(request, 'Request accepted')
        if friend_request.status == Relationship.SENT:
            friend_request.status = Relationship.ACCEPTED
            friend_request.save()

        return redirect('/social/requests')


@method_decorator(signin_required, name="dispatch")
class RejectRequest(View):
    def get(self, request, id, *args, **kwargs):
        friend_request = Relationship.objects.get(id=id)
        friend_request.sender.user.friends.remove(friend_request.receiver)
        friend_request.receiver.user.friends.remove(friend_request.sender)
        messages.error(request, 'Request rejected')
        if friend_request.status == Relationship.ACCEPTED:
            friend_request.status = Relationship.REJECTED
            friend_request.save()
        elif friend_request.status == Relationship.SENT:
            friend_request.status = Relationship.REJECTED
            friend_request.save()
        return redirect('/social/requests')


@method_decorator(signin_required, name="dispatch")
class FriendList(ListView):
    model = Profile

    def get(self, request, id, *args, **kwargs):
        profile = Profile.objects.get(id=id)
        friends = profile.friends.all()
        context = {
            'friends': friends
        }

        return render(request, 'friendslist.html', context)


@method_decorator(signin_required, name="dispatch")
class DeleteProfile(DeleteView):
    model = User
    pk_url_kwarg = 'id'
    template_name = 'deleteprofile.html'
    success_url = "/socialapp/signin"


def contactsendmail(request):
    if request.method == 'GET':
        form = ContactFormEmail()

    else:
        form = ContactFormEmail(request.POST)
        if form.is_valid():
            fromemail = form.cleaned_data['fromemail']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            send_mail(subject, message, fromemail, ['dobblesocial@gmail.com', fromemail])
            messages.success(request, 'Mail sent')
            return redirect('/social/contact/')
    return render(request, 'contactpage.html', {'form': form})


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'change_password.html', {
        'form': form
    })
