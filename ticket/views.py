from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView, ListView, UpdateView
from .models import Ticket, Zones, Branches
from blog.models import Post, Comment
from django.contrib import messages
from django.contrib.auth.models import User
from ticket.models import Expert
import random
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail

class BookTicketView(LoginRequiredMixin, CreateView):
    model = Ticket
    fields = ['issue', 'phone', 'anydesk', 'image', 'description']

    def form_valid(self, form):
        expert = random.choice(random.shuffle(Expert.objects.all()))
        form.instance.assigned_to = expert
        form.instance.submitter = self.request.user
        form.instance.zone = self.request.user.account.zone
        form.instance.branch = self.request.user.account.branch
        send_mail(
            f'{form.instance.issue}',
            f'{form.instance.submitter.first_name} {form.instance.submitter.last_name} sent a support request.\n\nDESCRIPTION:\n\n{form.instance.description}', 
            'yonnatech.g@gmail.com',
            ['techsupport@yonnaforexbureau.com'],
            fail_silently=False,
        )

        send_mail(
            f'Ticket Assignation',
            f'You have been assigned a task to work on the request of {form.instance.submitter.first_name} {form.instance.submitter.last_name} about {form.instance.issue} ', 
            'yonnatech.g@gmail.com',
            [f'{expert.expert.email}'],
            fail_silently=False,
        )
        messages.success(self.request, "Your request have been submitted successfully. We will get back to you shortly. Thanks 😊")
        return super().form_valid(form)
    
    def get_context_data(self, *args, **kwargs):
        context = super(BookTicketView, self).get_context_data(*args, **kwargs)
        context['button'] = 'Request'
        return context
    

class TicketView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'ticket/my_tickets.html'
    context_object_name = 'tickets'
    ordering = ['-date_submitted']
    paginate_by = 8

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Ticket.objects.filter(submitter=user).order_by('-date_submitted')
    

class DashboardView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'ticket/dashboard.html'
    context_object_name = 'tickets'
    
    def get_context_data(self, *args, **kwargs):
        tickets_total = len(Ticket.objects.all())
        tickets_pending = len(Ticket.objects.filter(status=False))
        tickets_closed = len(Ticket.objects.filter(status=True))
        users = len(User.objects.all())
        zones = len(Zones.objects.all())
        branches = len(Branches.objects.all())
        posts = len(Post.objects.all())
        comments = len(Comment.objects.all())

        # likes
        likes = 0
        for post in Post.objects.all():
            likes += post.total_likes()

        context = super(DashboardView, self).get_context_data(*args, **kwargs)

        context["tickets_total"] = tickets_total
        context["tickets_pending"] = tickets_pending
        context["tickets_closed"] = tickets_closed
        context["users"] = users
        context["zones"] = zones
        context["branches"] = branches
        context["posts"] = posts
        context["comments"] = comments
        context["likes"] = likes
        return context


class UpdateTicketView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ticket
    fields = ['issue', 'phone', 'anydesk', 'image', 'description']

    def form_valid(self, form):
        messages.success(self.request, "Your ticket is updated successfully.")
        return super().form_valid(form)
    
    
    def test_func(self):
        ticket = self.get_object()
        return self.request.user == ticket.submitter and not ticket.status
    
    def get_context_data(self, *args, **kwargs):
        context = super(UpdateTicketView, self).get_context_data(*args, **kwargs)
        context['button'] = 'Update'
        return context