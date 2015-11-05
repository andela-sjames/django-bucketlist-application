from django.shortcuts import render
from django.views.generic import View
from django.core.context_processors import csrf
from bucketlist.forms import UserSignupForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.core.validators import validate_email, ValidationError
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
# Create your views here. 

class HomePageView(View):

    template_name = 'bucketlist/index.html'
    
    def get(self, request):
        return render(request, self.template_name)

class SignUpView(View):

    template_name = 'bucketlist/signup.html'

    def get(self, request, *args, **kwargs):
        args ={}
        args.update(csrf(request))
        return render(request, self.template_name, args)

    def post(self,request, *args, **kwargs):

        usersignupform = UserSignupForm(request.POST)
        #get the user email address
        email = request.POST.get('email')
        signup_new_user = User.objects.filter(email__exact=email)

        if signup_new_user:
            args = {}
            args.update(csrf(request))
            mssg = "Email already taken please signup with another email"
            messages.add_message(request, messages.INFO, mssg)
            return render(request, self.template_name, args)

        if usersignupform.is_valid():                      
            usersignupform.save()
            confirmation_msg = "You have sucessfully registered."
            messages.add_message(request, messages.INFO, confirmation_msg)
            return HttpResponseRedirect(reverse('signin'))

        else:
            login = "Seems like you didn't input a strong password."
            args = {}
            args.update(csrf(request))
            messages.add_message(request, messages.INFO,login )
            return render(request, self.template_name, args)


class SignOutView(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(
            reverse('homepage'))    

class SignInView(View):

    template_name = 'bucketlist/signin.html'

    def get(self, request, *args, **kwargs):
        args ={}
        args.update(csrf(request))
        return render(request, self.template_name, args)

    def post(self, request, *args, **kwargs):

        if self.request.user.is_authenticated():
            return HttpResponseRedirect(reverse('dashboard'))

        else:
            email = self.request.POST.get('email', '')
            password = self.request.POST.get('password', '')
            csrfmiddlewaretoken = self.request.POST.get('csrfmiddlewaretoken', '')
            try:
                validate_email(email)
            except ValidationError:
                pass
            try:
                theuser = User.objects.get(email=email)
                user = authenticate(username=theuser.username, password=password)
                if user is not None and user.is_active:
                    login(self.request, user)
                return HttpResponseRedirect(reverse('dashboard'))

            except ObjectDoesNotExist:
                new_user_msg = "Please Sign Up for a wonderful experience."
                messages.add_message(request, messages.INFO, new_user_msg)
                return HttpResponseRedirect(reverse('homepage'))


class DashboardView(View):
    template_name = 'bucketlist/dashboard.html'
    
    def get(self, request):
        return render(request, self.template_name)

class BucketItemsView(View):

    template_name ='bucketlist/item.html'

    def get(self, request, *args, **kwargs):
        args ={}
        args.update(csrf(request))
        return render(request, self.template_name, args)








        