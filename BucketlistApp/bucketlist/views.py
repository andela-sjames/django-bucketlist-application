from django.shortcuts import render
from django.views.generic import View
from django.views.generic.base import TemplateView
from django.core.context_processors import csrf
from bucketlist.forms import UserSignupForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.core.validators import validate_email, ValidationError
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from bucketlist.models import Bucketlist, BucketlistItems
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
            return HttpResponseRedirect(reverse_lazy('signin'))

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
            reverse_lazy('homepage'))    

class SignInView(View):

    template_name = 'bucketlist/signin.html'

    def get(self, request, *args, **kwargs):
        args ={}
        args.update(csrf(request))
        return render(request, self.template_name, args)

    def post(self, request, *args, **kwargs):

        if self.request.user.is_authenticated():
            return HttpResponseRedirect(reverse_lazy('board'))

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
                return HttpResponseRedirect(reverse_lazy('board'))

            except ObjectDoesNotExist:
                new_user_msg = "Please Sign Up for a wonderful experience."
                messages.add_message(request, messages.INFO, new_user_msg)
                return HttpResponseRedirect(reverse_lazy('homepage'))


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


    def post(self, request, **kwargs):

        username = self.kwargs.get('username')
        userid=self.kwargs.get('id')

        name = request.POST.get('name','')
        public = request.POST.get('public')
        public = True if public else False

        itemname = request.POST.get('itemname','')
        done = request.POST.get('done')
        done = True if done else False

        if name and itemname:
            bucketlist=Bucketlist(name=name, public=public, created_by=username, user_id=userid)
            bucketlist.save()
            items=BucketlistItems(name=itemname, done=done, bucketlist_id=bucketlist.id)
            items.save()

            msg = "Action succesfully performed."
            messages.add_message(request, messages.SUCCESS, msg)
            return HttpResponseRedirect(reverse_lazy('mylist', kwargs={
                'username': username,
                'id':userid
                }))

        else:
            args ={}
            args.update(csrf(request))
            msg = "It seems like you didn't add an item."
            messages.add_message(request, messages.INFO, msg)
            return render(request, self.template_name, args)

class BucketlistView(TemplateView):

    template_name = 'bucketlist/list.html'

    def get_context_data(self, **kwargs):
        context = super(BucketlistView, self).get_context_data(**kwargs)
        userid=self.kwargs.get('id')
        context['bucketlists'] = Bucketlist.objects.filter(user=userid)
        return context


class ViewBucketlistdetail(TemplateView):

    template_name='bucketlist/view.html'

    def get_context_data(self, **kwargs):
        context = super(ViewBucketlistdetail, self).get_context_data(**kwargs)
        bucketlistid=self.kwargs.get('id')
        context['items'] = BucketlistItems.objects.filter(bucketlist_id=bucketlistid)
        context['bucketlists']=Bucketlist.objects.filter(id=bucketlistid)
        return context

class AddItemsView(View):


    def post(self, request, **kwargs):

        bucketlistid=self.kwargs.get('id')
        
        itemname = request.POST.get('itemname','')
        done = request.POST.get('done')
        done = True if done else False

        if itemname:
            items=BucketlistItems(name=itemname, done=done, bucketlist_id=bucketlistid)
            items.save()

            msg = "Item succesfully added."
            messages.add_message(request, messages.SUCCESS, msg)
            return HttpResponseRedirect(reverse_lazy('view', kwargs={
                    'id':bucketlistid }))

        else:
            msg = "Item field should not be left empty."
            messages.add_message(request, messages.SUCCESS, msg)
            return HttpResponseRedirect(reverse_lazy('view', kwargs={
                'id':bucketlistid }))



class DeleteUpdateBucketlistView(View):

    def get(self, request, **kwargs):
        bucketlistid=self.kwargs.get('id')
        bucketlist=Bucketlist.objects.get(id=bucketlistid)
        bucketlist.delete()

        msg = "bucketlist succesfully deleted"
        messages.add_message(request, messages.SUCCESS, msg)
        return HttpResponseRedirect(reverse_lazy('view', kwargs={
                'id':bucketlistid }))

    def post(self, request, **kwargs):

        bucketlistid=self.kwargs.get('id')
        name = request.POST.get('name','')
        bucketlist=Bucketlist.objects.get(id=bucketlistid)
        bucketlist.name=name
        bucketlist.save()
        msg = "Bucketlist name succesfully edited."
        messages.add_message(request, messages.SUCCESS, msg)
        return HttpResponseRedirect(reverse_lazy('view', kwargs={
                'id':bucketlistid }))




class delUpdateItemView(View):

    def get(self, request, **kwargs):

        bucketlistid=self.kwargs.get('id')
        itemid = self.kwargs.get('item_id')
        item=BucketlistItems.objects.get(id=itemid)
        item.delete()

        msg = "Item sucessfully deleted."
        messages.add_message(request, messages.SUCCESS, msg)
        return HttpResponseRedirect(reverse_lazy('view', kwargs={
                'id':bucketlistid }))

    def post(self, request, **kwargs):

        bucketlistid=self.kwargs.get('id')
        itemid = self.kwargs.get('item_id')
        itemname = request.POST.get('itemname','')
        done = request.POST.get('done')
        done = True if done else False

        item=BucketlistItems.objects.get(id=itemid)
        item.name=itemname
        item.done=done
        item.save()

        msg = "Item sucessfully edited."
        messages.add_message(request, messages.SUCCESS, msg)
        return HttpResponseRedirect(reverse_lazy('view', kwargs={
                'id':bucketlistid }))





