from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import logout
from .forms import UserRegisterForm,LoginForm
from django.contrib.auth.views import LoginView
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from .models import Profile

# Create your views here.
def register(request):
    form=UserRegisterForm(request.POST or None)
    if request.method=='POST':
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            messages.success(request,f"Welcome {username}, your account has been successfully created")
            return redirect('login')
    context={
        'form':form
    }
    return render(request,"users/register.html",context)

def logout_view(request):
    logout(request)
    return render(request,"users/logout.html")


class CustomLoginView(LoginView):
    template_name = "login.html"
    form_class = LoginForm

class ProfileUpdateView(UpdateView):
    model = Profile
    fields = ['weight', 'height', 'daily_calorie_goal']
    template_name = "users/profile.html"
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        return self.request.user.profile