from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, TemplateView
from django.contrib import messages

from commons.decorators import redirect_to_home_if_authenticated
from commons.utils import send_account_activation_mail
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm
from .models import UserAccountActivationKey, User, UserProfile


@method_decorator(redirect_to_home_if_authenticated, name="get")
class UserRegistrationView(CreateView):
    template_name = 'account/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Sign Up"
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            messages.success(request, "Please Check Your Inbox and Activate Your Account !!")
            response = self.form_valid(form)
            user = self.object
            send_account_activation_mail(request, user)
            return response
        else:
            messages.error(request, "Invalid User Data !!")
            return self.form_invalid(form)


class UserLoginView(CreateView):
    template_name = "account/login.html"
    form = UserLoginForm

    @redirect_to_home_if_authenticated
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context={"form": self.form()})

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            email, pw = form.cleaned_data['email'], form.cleaned_data['password']
            user = authenticate(request, email=email, password=pw)
            if not user:
                messages.error(request, "Invalid Email or Password !!")
                return redirect('user_login')
            login(request, user)
            messages.success(request, "User Logged In Successfully !!")
            return redirect("home")
        else:
            messages.error(request, "Improperly Submitted Email or Password !!")
            return redirect("user_login")


def user_logout(request):
    logout(request)
    messages.success(request, "User Logged Out Successfully !!")
    return redirect("home")


def user_account_activation(request, username, activation_key):
    if UserAccountActivationKey.objects.filter(user__username=username, key=activation_key).exists():
        User.objects.filter(username=username).update(account_activated=True)
        UserAccountActivationKey.objects.filter(user__username=username).delete()
        messages.success(request, "Your Account Has Been Activated !!")
        return redirect("user_login")
    messages.error(request, "Invalid Activation Link or the Link Expired !!")
    return redirect("user_login")


@method_decorator(login_required, name='dispatch')
class UserProfileView(TemplateView):
    template_name = "account/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "User Profile"
        return context


@method_decorator(login_required, name='dispatch')
class UserProfileUpdateView(CreateView):
    template_name = "account/profile_update.html"
    form_class = UserProfileForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Profile Update"
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            profile_picture = form.cleaned_data.pop('profile_picture', None)
            resume = form.cleaned_data.pop('resume', None)
            profile, _ = UserProfile.objects.update_or_create(user=self.request.user, defaults=form.cleaned_data)
            if profile_picture or resume:
                if profile_picture:
                    profile.profile_picture = profile_picture
                if resume:
                    profile.resume = resume
                profile.save()
            messages.success(request, "Your Profile Has Been Updated !!")
            return redirect('user_profile')
        else:
            print(form.errors.get_json_data())
            messages.error(request, form.errors.as_text())
            return self.form_invalid(form)
