from django.shortcuts import render
from django.views.generic import View
from django.views.generic.base import TemplateView
from django.core.context_processors import csrf
from bucketlist.forms import UserSignupForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from bucketlist.models import Bucketlist, BucketlistItem
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404


class LoginRequiredMixin(object):

    '''View mixin which requires that the user is authenticated.'''

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(
            request, *args, **kwargs)


class SignUpView(TemplateView):

    '''View defined for user signup.'''

    template_name = 'bucketlist/signup.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(
                reverse_lazy('mylist',
                             kwargs={'username': request.user.username, }))
        return super(SignUpView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        usersignupform = UserSignupForm(request.POST)
        # get the user email address
        email = request.POST.get('email')
        new_user_signup = User.objects.filter(email__exact=email)

        # run if user already exist
        if new_user_signup:
            args = {}
            args.update(csrf(request))
            mssg = "Email already taken please signup with another email"
            messages.add_message(request, messages.INFO, mssg)
            return render(request, self.template_name, args)

        # run if user doesn't exist
        if usersignupform.is_valid():
            usersignupform.save()
            confirmation_msg = """You have sucessfully registered,
             please sign in."""
            messages.add_message(request, messages.INFO, confirmation_msg)
            return HttpResponseRedirect(reverse_lazy('signup'))

        # run if the first two conditions are not met.
        else:
            args = {}
            args.update(csrf(request))
            return render(request, self.template_name, args)


class SignOutView(View, LoginRequiredMixin):

    '''Logout User from session.'''

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(
            reverse_lazy('signup'))


class SignInView(TemplateView):

    '''Sign in existing user. '''

    def post(self, request, *args, **kwargs):

        email = self.request.POST.get('email', '')
        password = self.request.POST.get('password', '')
        csrfmiddlewaretoken = self.request.POST.get('csrfmiddlewaretoken', '')

        if self.request.user.is_authenticated():
            username = request.user.username
            return HttpResponseRedirect(reverse_lazy('mylist', kwargs={
                'username': username,
            }))

        else:
            try:
                singin_user = User.objects.get(email=email)
                user = authenticate(username=singin_user.username,
                                    password=password)

                if user is None:
                    new_user_msg = """Invalid password,
                     please confirm your password."""
                    messages.add_message(request, messages.INFO, new_user_msg)
                    return HttpResponseRedirect(reverse_lazy('signup'))

                if user is not None and user.is_active:

                    username = user.username
                    login(self.request, user)
                return HttpResponseRedirect(
                    reverse_lazy('mylist',
                                 kwargs={'username': username, }))

            except ObjectDoesNotExist:
                new_user_msg = "Please Sign Up for a wonderful experience."
                messages.add_message(request, messages.INFO, new_user_msg)
                return HttpResponseRedirect(reverse_lazy('signup'))


class CreateBucketlistView(View, LoginRequiredMixin):

    ''' View to create a new bucketlist.'''

    def post(self, request, **kwargs):

        name = request.POST.get('name', '')

        if name:
            bucketlist = Bucketlist(
                name=name, created_by=request.user.username,
                user_id=request.user.id)
            bucketlist.save()
            msg = "Action succesfully performed."
            messages.add_message(request, messages.SUCCESS, msg)
            return HttpResponseRedirect(reverse_lazy('mylist', kwargs={
                'username': request.user.username, }))

        else:
            msg = "It seems like you didn't add an item."
            messages.add_message(request, messages.INFO, msg)
            return HttpResponseRedirect(reverse_lazy('mylist', kwargs={
                'username': request.user.username, }))


class BucketlistView(View, LoginRequiredMixin):

    '''View to display specified bucketlist '''

    template_name = 'bucketlist/list.html'

    def get(self, request, *args, **kwargs):

        args = {}
        userid = self.request.user.id
        username = self.request.user.username
        if username:

            user_bucketlists = Bucketlist.objects.filter(
                user=userid).order_by('-date_created')
            paginator = Paginator(user_bucketlists, 9, 2)

            try:
                page = int(request.GET.get('page', 1))
            except:
                page = 1

            try:
                bucketlists = paginator.page(page)
            except(EmptyPage, InvalidPage):
                bucketlists = paginator.page(paginator.num_pages)

            args['bucketlists'] = bucketlists
            args.update(csrf(request))
            return render(request, self.template_name, args)
        else:
            return HttpResponseRedirect(reverse_lazy('signin'))


class ViewBucketlistdetail(TemplateView, LoginRequiredMixin):

    '''View bucketlist detail and associated items'''

    template_name = 'bucketlist/view.html'

    def get(self, request, *args, **kwargs):

        args = {}
        bucketlistid = self.kwargs.get('id')

        bucketlist = Bucketlist.objects.filter(
            id=bucketlistid).filter(
            user_id=self.request.user.id)
        if not bucketlist:
            raise Http404

        myitems_list = BucketlistItem.objects.filter(
            bucketlist_id=bucketlistid)
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
        args['bucketlists'] = bucketlist
        return render(request, self.template_name, args)


class AddItemsView(View, LoginRequiredMixin):

    '''View to  add item to a specific bucketlist '''

    def post(self, request, **kwargs):

        bucketlistid = self.kwargs.get('id')
        itemname = request.POST.get('itemname', '')
        done = request.POST.get('done')
        done = True if done else False

        if itemname:
            items = BucketlistItem(
                name=itemname,
                done=done,
                bucketlist_id=bucketlistid)
            items.save()

            msg = "Item succesfully added."
            messages.add_message(request, messages.SUCCESS, msg)
            return HttpResponseRedirect(
                reverse_lazy('view',
                             kwargs={'id': bucketlistid}))

        else:
            msg = "Item field should not be left empty."
            messages.add_message(request, messages.SUCCESS, msg)
            return HttpResponseRedirect(reverse_lazy('view', kwargs={
                'id': bucketlistid}))


class DeleteUpdateBucketlistView(View, LoginRequiredMixin):

    '''View to delete and update a specified bucketlist.'''

    def get(self, request, **kwargs):
        bucketlistid = self.kwargs.get('id')
        bucketlist = Bucketlist.objects.get(id=bucketlistid)
        bucketlist.delete()

        msg = "bucketlist succesfully deleted"
        messages.add_message(request, messages.SUCCESS, msg)
        return HttpResponseRedirect(
            reverse_lazy('mylist', kwargs={
                'username': request.user.username, }))

    def post(self, request, **kwargs):

        bucketlistid = self.kwargs.get('id')
        name = request.POST.get('name', '')
        bucketlist = Bucketlist.objects.get(id=bucketlistid)
        bucketlist.name = name
        bucketlist.save()
        msg = "Bucketlist name succesfully edited."
        messages.add_message(request, messages.SUCCESS, msg)
        return HttpResponseRedirect(
            reverse_lazy('mylist',
                         kwargs={'username': request.user.username, }))


class DelUpdateItemView(View, LoginRequiredMixin):

    '''View to delete and update a specified bucketlistitem.'''

    def get(self, request, **kwargs):

        bucketlistid = self.kwargs.get('id')
        itemid = self.kwargs.get('item_id')
        item = BucketlistItem.objects.get(id=itemid)
        item.delete()

        msg = "Item sucessfully deleted."
        messages.add_message(request, messages.SUCCESS, msg)
        return HttpResponseRedirect(
            reverse_lazy('view', kwargs={'id': bucketlistid}))

    def post(self, request, **kwargs):

        bucketlistid = self.kwargs.get('id')
        itemid = self.kwargs.get('item_id')
        itemname = request.POST.get('itemname', '')
        done = request.POST.get('done')
        done = True if done else False

        item = BucketlistItem.objects.get(id=itemid)
        item.name = itemname
        item.done = done
        item.save()

        msg = "Item sucessfully edited."
        messages.add_message(request, messages.SUCCESS, msg)
        return HttpResponseRedirect(
            reverse_lazy('view', kwargs={'id': bucketlistid}))


class SearchListView(TemplateView, LoginRequiredMixin):

    ''' View to search for bucketlists if there exists. '''

    template_name = 'bucketlist/ajax_search.html'

    def get(self, request, *args, **kwargs):

        userid = self.kwargs.get('id')
        text = request.GET.get('q', '')
        result = Bucketlist.objects.filter(
            name__icontains=text).filter(user_id=userid)

        paginator = Paginator(result, 8, 2)

        try:
            page = int(request.GET.get('page', 1))
        except:
            page = 1
        try:
            search_result = paginator.page(page)
        except(EmptyPage, InvalidPage):
            search_result = paginator.page(paginator.num_pages)

        return render(request, self.template_name, {'search': search_result})


class ItemDone(View):

    '''Class defined to toggle done field. '''

    def get(self, request, *args, **kwargs):

        bucketlistid = self.kwargs.get('id')
        itemid = self.kwargs.get('item_id')
        item = BucketlistItem.objects.get(id=itemid)
        if item.done is True:
            item.done = False
            item.save()
        else:
            item.done = True
            item.save()

        return HttpResponseRedirect(
            reverse_lazy('view', kwargs={'id': bucketlistid}))


def custom_404(request):
    return render(request, 'bucketlist/404.html')


def custom_500(request):
    return render(request, 'bucketlist/500.html')
