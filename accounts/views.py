from django.shortcuts import render,redirect
from django.views.generic import FormView
from accounts.forms import SignUpForm,UserAccountForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib import messages
from django.contrib.auth import login,logout
from django.views import View

# Create your views here.

class UserSignUpView(FormView):
    template_name ='signup.html'
    form_class =SignUpForm
    success_url =reverse_lazy("home")

    def form_valid(self, form):
        messages.success(self.request,"Account create successfully")
        form.save()
        return super().form_valid(form)
    

class UserLoginView(LoginView):
    template_name ='login.html'
    def get_success_url(self):
        return reverse_lazy('home')
    def form_valid(self,form):
        messages.success(self.request,"Login successfully")
        return super().form_valid(form)


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('login')
    
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET':
            if request.user.is_authenticated:
                logout(self.request)
            return redirect(self.next_page)
        else:
            return super().dispatch(request, *args, **kwargs)
        


class UserAccountUpdateView(View):
    template_name = 'profile.html'

    def get(self, request):
        form =UserAccountForm(instance=request.user)
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = UserAccountForm(request.POST,request.FILES, instance=request.user)
        if form.is_valid():
            messages.success(self.request,"Account update successfully")
            form.save()
            return redirect('profile')
        return render(request, self.template_name, {'form': form})


