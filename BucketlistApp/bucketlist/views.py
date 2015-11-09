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
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.views.generic.list import ListView

# Create your views here. 

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
            reverse_lazy('signin'))    

class SignInView(View):

    template_name = 'bucketlist/signin.html'

    def get(self, request, *args, **kwargs):
        args ={}
        args.update(csrf(request))
        return render(request, self.template_name, args)

    def post(self, request, *args, **kwargs):

        email = self.request.POST.get('email', '')
        password = self.request.POST.get('password', '')
        csrfmiddlewaretoken = self.request.POST.get('csrfmiddlewaretoken', '')

        if self.request.user.is_authenticated():
            username=request.user.username
            userid=request.user.id
            return HttpResponseRedirect(reverse_lazy('mylist', kwargs={
                'username': username,
                'id':userid
                }))

        else:
            try:
                validate_email(email)
            except ValidationError:
                pass
            try:
                theuser = User.objects.get(email=email)
                user = authenticate(username=theuser.username, password=password)
                if user is not None and user.is_active:
                    username=user.username
                    userid=user.id
                    login(self.request, user)
                return HttpResponseRedirect(reverse_lazy('mylist', kwargs={
                'username': username,
                'id':userid
                }))

            except ObjectDoesNotExist:
                new_user_msg = "Please Sign Up for a wonderful experience."
                messages.add_message(request, messages.INFO, new_user_msg)
                return HttpResponseRedirect(reverse_lazy('signin'))


class BucketItemsView(View):

    def post(self, request, **kwargs):

        username = self.kwargs.get('username')
        userid=self.kwargs.get('id')

        name = request.POST.get('name','')

        itemname = request.POST.get('itemname','')
        done = request.POST.get('done')
        done = True if done else False

        if name and itemname:
            bucketlist=Bucketlist(name=name, created_by=username, user_id=userid)
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
            msg = "It seems like you didn't add an item."
            messages.add_message(request, messages.INFO, msg)
            return HttpResponseRedirect(reverse_lazy('mylist', kwargs={
                'username': username,
                'id':userid
                }))

class BucketlistView(View):

    
    template_name = 'bucketlist/list.html'

    def get(self, request, *args, **kwargs):
        args ={}
        userid=self.kwargs.get('id')
        user_bucketlists= Bucketlist.objects.filter(user=userid).order_by('-date_created')
        paginator = Paginator(user_bucketlists, 10, 2)

        try:
            page = int(request.GET.get('page',1))
        except:
            page = 1

        try:
            bucketlists = paginator.page(page)
        except(EmptyPage, InvalidPage):
            bucketlists = paginator.page(paginator.num_pages)

        args['bucketlists'] = bucketlists
        args.update(csrf(request))
        return render(request, self.template_name, args)


class ViewBucketlistdetail(TemplateView):

    template_name='bucketlist/view.html'

    def get(self, request, *args, **kwargs):
        args ={}
        bucketlistid=self.kwargs.get('id')
        
        myitems_list = BucketlistItems.objects.filter(bucketlist_id=bucketlistid)
        paginator = Paginator(myitems_list, 8, 2)

        try:
            page = int(request.GET.get('page',1))
        except:
            page = 1

        try:
            items = paginator.page(page)
        except(EmptyPage, InvalidPage):
            items = paginator.page(paginator.num_pages)
        
        args.update(csrf(request))
        args['items'] = items
        args['bucketlists']=Bucketlist.objects.filter(id=bucketlistid)
        return render(request, self.template_name, args)


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

class SearchListView(TemplateView):

    template_name='bucketlist/ajax_search.html'

    def get(self, request, *args, **kwargs):

        userid = self.kwargs.get('id')
        text =  request.GET.get('q', '')
        result = Bucketlist.objects.filter(name__icontains=text).filter(user_id=userid)


        return render(request, self.template_name, {'search':result})



