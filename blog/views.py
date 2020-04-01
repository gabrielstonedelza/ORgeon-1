from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView
from .models import Volunteer, Events, JoinTrip, Partnership, NewsLetter, Report, InstantMessage, Post, Comments, NewsUpdate, Usermsg, Gallery,LoginCode,Online_user,InstantReply
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from email.message import EmailMessage
import smtplib
from django.conf import settings
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
import pytz
from django.db.models import Q
from datetime import datetime, date, time, timedelta
from django.core.paginator import Paginator
from .forms import (VolunteerForm,
                    JoinTripForm,
                    PartnershipForm,
                    NewsLetterForm,
                    ReportForm,
                    PostForm, InstantMessageForm, CommentsForm,
                    NewsUpdateForm,InstantReplyForms
                    )
from django.contrib.auth.models import User
import random
from django.contrib import auth
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login
import threading
import time
import asyncio

# global time checker
CAN_STAY_LOGGED_IN1 = 30
CAN_STAY_LOGGED_IN2 = 45
CAN_STAY_LOGGED_IN3 = 55
CAN_STAY_LOGGED_IN4 = 15

@login_required()
def news_letter(request):
    msg = EmailMessage()
    suscribed_users = NewsLetter.objects.all()
    if request.method == "POST":
        form = NewsUpdateForm(request.POST)
        if form.is_valid():
            form.save()
            title = form.cleaned_data.get('title').upper()
            update_message = form.cleaned_data.get('message')
            msg["Subject"] = title
            msg["From"] = settings.EMAIL_HOST_USER
            msg["To"] = suscribed_users
            msg.set_content(update_message)
            hml = f"""
            <!Doctype html>
            <html>
            <body>
            <h1 style='font-style:italic;'>{ title }</h1>
            <p style='color:SlateGray;'>  { update_message } </p>
            </body>
            </html>
            </html>
            """
            msg.add_alternative(hml, subtype='html')
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(settings.EMAIL_HOST_USER,settings.EMAIL_HOST_PASSWORD)
                smtp.send_message(msg)
                messages.success(request, f"News update messages sent successfully.")
                return redirect('newsletter_create')
    else:
        form = NewsUpdateForm()

    context = {
        "form": form
    }

    return render(request, "blog/newsletter.html", context)


def home(request):
    if request.method == "POST":
        msg = EmailMessage()
        form = NewsLetterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if NewsLetter.objects.filter(email=email).exists():
                messages.info(request, "This email already exists.")
            else:
                form.save()
                msg["Subject"] = "Thank you for subcribing to our newsletter."
                msg["From"] = settings.EMAIL_HOST_USER
                msg["To"] = email
                msg.set_content("We will send you all the necessary updates.")
                hml = f"""
                <!Doctype html>
                <html>
                <body>
                <h1 style='font-style:italic;'>Thank you for subcribing to our newsletter.</h1>
                <p style='color:SlateGray;'> We will send you all the necessary updates.</p>
                <p style='color:SlateGray;'>Stay blessed.</p>
                <p style='color:SlateGray;'>ORgeonofstars</p>
                </body>
                </html>
                </html>
                """
                msg.add_alternative(hml, subtype='html')
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(settings.EMAIL_HOST_USER,
                               settings.EMAIL_HOST_PASSWORD)
                    smtp.send_message(msg)
                    messages.success(
                        request, f"Thank you,your email has been added to our newslist.")
                    return redirect('home')

    else:
        form = NewsLetterForm()

    context = {
        'form': form
    }
    return render(request, "blog/home.html", context)


def success_stories(request):
    return render(request, "blog/success-stories.html")


def needy_stories(request):
    return render(request, "blog/stories_of_need.html")


def inspirational_stories(request):
    return render(request, "blog/inspirational_stories.html")


def some_videos(request):
    return render(request, "blog/some_videos.html")


def volunteer_register(request):
    msg = EmailMessage()
    msg1 = EmailMessage()
    if request.method == "POST":
        form = VolunteerForm(request.POST)
        if form.is_valid():
            v_email = form.cleaned_data.get('email')
            if Volunteer.objects.filter(email=v_email).exists():
                messages.info(
                    request, f"Volunteer with {v_email} already exist.")
            else:
                form.save()
                name = form.cleaned_data.get('name')
                msg["Subject"] = f"{name} has just volunteered."
                msg["From"] = settings.EMAIL_HOST_USER
                msg["To"] = settings.EMAIL_HOST_USER
                msg.set_content(f"{name} wishes to volunteer for Orgeon.")
                hml = f"""
                <!Doctype html>
                <html>
                <body>
                <h1 style='font-style:italic;'>{name} has just volunteered.</h1>
                <p style='color:SlateGray;'> {name} wishes to volunteer for Orgeon.</p>
                </body>
                </html>
                </html>
                """
                msg.add_alternative(hml, subtype='html')
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(settings.EMAIL_HOST_USER,
                               settings.EMAIL_HOST_PASSWORD)
                    smtp.send_message(msg)
                # to user volunteering email
                msg1["Subject"] = "Orgeon of Stars welcomes you."
                msg1["From"] = settings.EMAIL_HOST_USER
                msg1["To"] = v_email
                msg1.set_content(
                    "Thank you for volunteering with Orgeon of stars,in order to know more about  you we will contact you soon,stay blessed.")
                hml = f"""
                <!Doctype html>
                <html>
                <body>
                <h1 style='font-style:italic;'>Welcome to ORgeonofstars.</h1>
                <p style='color:SlateGray;'> Thank you for volunteering with Orgeon of stars,in order to know more about  you we will contact you soon.</p>
                <p style='color:SlateGray;'>Stay blessed.</p>
                <p style='color:SlateGray;'>ORgeonofstars</p>
                </body>
                </html>
                </html>
                """
                msg1.add_alternative(hml, subtype='html')
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(settings.EMAIL_HOST_USER,
                               settings.EMAIL_HOST_PASSWORD)
                    smtp.send_message(msg1)
                    messages.success(request, f"Thank you for joining.")
                    return redirect('volunteers')

    else:
        form = VolunteerForm()

    context = {
        'form': form
    }

    return render(request, "blog/volunteer_form.html", context)


class Volunteers(ListView):
    model = Volunteer
    template_name = 'blog/volunteers.html'
    context_object_name = 'volunteers'
    ordering = ['-date_volunteered']


def events(request):
    events = Events.objects.all().order_by('-date_posted')[:1]

    context = {
        'events': events
    }

    return render(request, "blog/events.html", context)


def join_trip(request):
    msg = EmailMessage()
    msg1 = EmailMessage()
    if request.method == "POST":
        form = JoinTripForm(request.POST)
        if form.is_valid():
            trip_email = form.cleaned_data.get('email')
            if JoinTrip.objects.filter(email=trip_email).exists():
                messages.info(request, f"Email already exitst.")
        else:
            form.save()
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            phone = form.cleaned_data.get('phone')

            # mail to personal email
            msg["Subject"] = f"{name} wants to join the trip."
            msg["From"] = settings.EMAIL_HOST_USER
            msg["To"] = settings.EMAIL_HOST_USER
            msg.set_content(
                f"More details below \n 1.Email: {email}\n2.Phone: {phone}")
            hml = f"""
            <!Doctype html>
            <html>
            <body>
            <h1 style='font-style:italic;'>{name} wants to join the trip.</h1>
            <p style='color:SlateGray;'> Name: {name} </p>
            <p style='color:SlateGray;'>Email: {email}</p>
            <p style='color:SlateGray;'>Email: {phone}</p>
            </body>
            </html>
            </html>
            """
            msg.add_alternative(hml, subtype='html')
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(settings.EMAIL_HOST_USER,
                           settings.EMAIL_HOST_PASSWORD)
                smtp.send_message(msg)

            msg1["Subject"] = "Thank you."
            msg1["From"] = settings.EMAIL_HOST_USER
            msg1["To"] = trip_email
            msg1.set_content(f"Orgeon of stars is so delighted that you have decided to join our trip, saving lives and helping the vulnerable children is our top priority and we are happy that you've made it yours too.We will let you know of any other information before we embark on this journey.Stay blessed.")
            hml = f"""
            <!Doctype html>
            <html>
            <body>
            <h1 style='font-style:italic;'>Thank you for joining our trip.</h1>
            <p style='color:SlateGray;'>Orgeon of stars is so delighted that you have decided to join our trip, saving lives and helping the vulnerable children is our top priority and we are happy that you've made it yours too.We will let you know of any other information before we embark on this journey.Stay blessed."</p>
            <p style='color:SlateGray;'>ORgeonofstars</p>
            </body>
            </html>
            </html>
            """
            msg1.add_alternative(hml, subtype='html')
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(settings.EMAIL_HOST_USER,
                           settings.EMAIL_HOST_PASSWORD)
                smtp.send_message(msg1)
                messages.success(
                    request, f"Thank you for joining us on this trip.")
                return redirect('events')

    else:
        form = JoinTripForm()

    context = {
        'form': form
    }

    return render(request, "blog/jointrip_form.html", context)


def become_partner(request):
    msg1 = EmailMessage()
    msg = EmailMessage()
    if request.method == "POST":
        form = PartnershipForm(request.POST)
        if form.is_valid():
            partner_email = form.cleaned_data.get('email')
            if Partnership.objects.filter(email=partner_email).exists():
                messages.info(
                    request, f"A partner with the same email already exits.")

            else:
                form.save()
                name = form.cleaned_data.get('name')
                email = form.cleaned_data.get('email')
                phone = form.cleaned_data.get('phone')

                msg1["Subject"] = "Thank you for your partnership"
                msg1["From"] = settings.EMAIL_HOST_USER
                msg1["To"] = partner_email
                msg1.set_content(
                    f"We are happy to see you and also work with you.We will contact you soon for additional information.Stay blessed.")
                hml = f"""
                <!Doctype html>
                <html>
                <body>
                <h1 style='font-style:italic;'>Thank you for your partnership.</h1>
                <p style='color:SlateGray;'>We are happy to see you and also work with you.We will contact you soon for additional information.Stay blessed.</p>
                <p style='color:SlateGray;'>ORgeonofstars</p>
                </body>
                </html>
                </html>
                """
                msg1.add_alternative(hml, subtype='html')
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(settings.EMAIL_HOST_USER,
                               settings.EMAIL_HOST_PASSWORD)
                    smtp.send_message(msg1)

                # mail to personal email

                msg["Subject"] = "Got new partner"
                msg["From"] = settings.EMAIL_HOST_USER
                msg["To"] = partner_email
                msg.set_content(
                    f"{name} wants to partner with Orgeon of stars.")
                hml = f"""
                <!Doctype html>
                <html>
                <body>
                <h1 style='font-style:italic;'>New Partnership.</h1>
                <p style='color:SlateGray;'>{name} wants to partner with Orgeon of stars.</p>
                <p style='color:SlateGray;'>Email: {email}</p>
                <p style='color:SlateGray;'>Email: {phone}</p>
                </body>
                </html>
                </html>
                """
                msg.add_alternative(hml, subtype='html')
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(settings.EMAIL_HOST_USER,
                               settings.EMAIL_HOST_PASSWORD)
                    smtp.send_message(msg)
                    messages.success(request, f"Thank you for joining us..")
                    return redirect('partners')
    else:
        form = PartnershipForm()

    context = {
        'form': form
    }

    return render(request, "blog/partnerform.html", context)


def partners(request):
    partners = Partnership.objects.all()

    context = {
        'partners': partners
    }

    return render(request, "blog/partners.html", context)


def donate(request):

    return render(request, "blog/donate.html")


class ReportListView(LoginRequiredMixin, ListView):
    model = Report
    template_name = "blog/reports.html"
    context_object_name = "reports"
    ordering = ['-date_posted']
    paginate_by = 5


@login_required()
def report_detail(request, id):
    if LoginCode.objects.filter(user=request.user).exists():
        report = get_object_or_404(Report, id=id)
        hasRead = False
        if report:
            if not report.has_read.filter(id=request.user.id).exists():
                report.has_read.add(request.user)
                hasRead = True
        reports = Report.objects.all().order_by('-date_posted')[:6]
        this_time = datetime.now()
        this_min = this_time.minute
        if this_min == CAN_STAY_LOGGED_IN1 or this_min == CAN_STAY_LOGGED_IN2 or this_min == CAN_STAY_LOGGED_IN3 or this_min == CAN_STAY_LOGGED_IN4:
            return redirect('logout')
    else:
        messages.info(request,f"You were logged out")
        return redirect('login')

    context = {
        'report': report,
        'hasread': hasRead,
        'reports': reports
    }

    return render(request, "blog/report_detail.html", context)


@login_required()
def create_report(request):
    if LoginCode.objects.filter(user=request.user).exists():
        if request.method == "POST":
            form = ReportForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data.get('title')
                report = form.cleaned_data.get('report')
                Report.objects.create(
                    user=request.user, title=title, report=report)
                reporter = request.user

                subject = f"New report from {reporter}"
                message = f"Login to orgeon of stars in order to read message"
                from_email = settings.EMAIL_HOST_USER
                to_list = [settings.EMAIL_HOST_USER]
                send_mail(subject, message, from_email,
                        to_list, fail_silently=True)
                messages.success(
                    request, f"Report '{title}' successfullly created.")
                return redirect('reports')

        else:
            form = ReportForm()
    else:
        messages.info(request,f"You were logged out")
        return redirect('login')

    context = {
        'form': form
    }

    return render(request, "blog/create_report.html", context)


@login_required()
def employees(request):
    if LoginCode.objects.filter(user=request.user).exists():
        employees = User.objects.all()
        this_time = datetime.now()
        this_min = this_time.minute
        if this_min == CAN_STAY_LOGGED_IN1 or this_min == CAN_STAY_LOGGED_IN2 or this_min == CAN_STAY_LOGGED_IN3 or this_min == CAN_STAY_LOGGED_IN4:
            return redirect('logout')
    else:
        messages.info(request,f"You were logged out")
        return redirect('login')
    context = {
        'employees': employees
    }

    return render(request, "blog/employees.html", context)


class InstantMessgeCreateView(LoginRequiredMixin, CreateView):
    model = InstantMessage
    fields = ['title', 'recipient', 'message_content']
    success_url = '/main'

    def form_valid(self, form):
        form.instance.sender = self.request.user
        
        return super().form_valid(form)

@login_required
def instantmessage_create(request):
    msg = EmailMessage()
    if request.method == "POST":
        form  = InstantMessageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            recipient = form.cleaned_data.get('recipient')
            content = form.cleaned_data.get('message_content')
            InstantMessage.objects.create(title=title,sender=request.user,recipient=recipient,message_content=content)
            theuser = User.objects.get(username=recipient)
            receiver_email = theuser.email

            msg["Subject"] = f"Got a new Message from {request.user.username}"
            msg["From"] = settings.EMAIL_HOST_USER
            msg["To"] = receiver_email
            msg.set_content(
                f"{request.user.username} just sent a private message to your inbox.Login to read it.")
            hml = f"""
                <!Doctype html>
                <html>
                <body>
                <h1 style='font-style:italic;'>Got a new Message from {request.user.username}</h1>
                <p style='color:SlateGray;'>{request.user.username} just sent a private message to your inbox.Login to read it.</p>
                </body>
                </html>
                </html>
                """
            msg.add_alternative(hml, subtype='html')
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(settings.EMAIL_HOST_USER,settings.EMAIL_HOST_PASSWORD)
                smtp.send_message(msg)
                messages.success(request,f'Your message to {recipient} was successful.')
                return redirect('main')

    else:
        form = InstantMessageForm()

    context = {
        'form': form
    }

    return render(request,"blog/instantmessage_form.html",context)

@login_required()
def user_messages(request):
    if LoginCode.objects.filter(user=request.user).exists():
        user_messages = InstantMessage.objects.filter(recipient=request.user).order_by('-date_posted')
        unread_count = InstantMessage.objects.filter(recipient=request.user, read=False).count
        paginator = Paginator(user_messages, 4)
        page = request.GET.get('page')
        user_messages = paginator.get_page(page)
        this_time = datetime.now()
        this_min = this_time.minute
        if this_min == CAN_STAY_LOGGED_IN1 or this_min == CAN_STAY_LOGGED_IN2 or this_min == CAN_STAY_LOGGED_IN3 or this_min == CAN_STAY_LOGGED_IN4:
            return redirect('logout')
    else:
        messages.info(request,f"You were logged out")
        return redirect('login')

    context = {
        'user_messages': user_messages,
        'notification_count': unread_count,
    }

    return render(request, "blog/messages.html", context)

@login_required()
def replied_detail(request,id):
    replied = get_object_or_404(InstantReply,id=id)

    context = {
        'replied' : replied
    }

    return render(request,"blog/replied.html",context)


@login_required()
def user_sent_messages(request):
    if LoginCode.objects.filter(user=request.user).exists():
        # sent messages
        sent_messages = InstantMessage.objects.filter(sender=request.user).order_by('-date_posted')
        ireplies = InstantReply.objects.all().order_by('-date_post')
        paginator = Paginator(sent_messages, 4)
        page = request.GET.get('page')
        sent_messages = paginator.get_page(page)
        this_time = datetime.now()
        this_min = this_time.minute
        if this_min == CAN_STAY_LOGGED_IN1 or this_min == CAN_STAY_LOGGED_IN2 or this_min == CAN_STAY_LOGGED_IN3 or this_min == CAN_STAY_LOGGED_IN4:
            return redirect('logout')
    else:
        messages.info(request,f"You were logged out")
        return redirect('login')

    context = {
        'user_messages': sent_messages,
    }

    return render(request, "blog/user_sent_messages.html", context)



@login_required()
def instantmessage_detail(request, id):
    if LoginCode.objects.filter(user=request.user).exists():
        user = get_object_or_404(User, username=request.user)
        instant_message = get_object_or_404(InstantMessage, recipient=user, id=id)

        has_read = False
        if instant_message:
            instant_message.read = True
            has_read = True
            instant_message.save()
        ireplies = InstantReply.objects.filter(imessage=instant_message).order_by('-date_posted')
        if request.method == "POST":
            form = InstantReplyForms(request.POST)
            if form.is_valid():
                rcontent = request.POST.get('reply_content')
                repmessage = InstantReply.objects.create(imessage=instant_message,user=request.user,reply_content=rcontent)
                back_to_sender = InstantMessage.objects.create(title=instant_message.title,sender=request.user,recipient=instant_message.sender)
                back_to_sender.save()
                repmessage.save()
        else:
            form = InstantReplyForms()
        this_time = datetime.now()
        this_min = this_time.minute
        if this_min == CAN_STAY_LOGGED_IN1 or this_min == CAN_STAY_LOGGED_IN2 or this_min == CAN_STAY_LOGGED_IN3 or this_min == CAN_STAY_LOGGED_IN4:
            return redirect('logout')
    else:
        messages.info(request,f"You were logged out")
        return redirect('login')

    context = {
        "instant_message": instant_message,
        'has_read': has_read,
        'form': form,
        'ireplies': ireplies
    }

    if request.is_ajax():
        html = render_to_string("blog/inreply.html",context,request=request)
        return JsonResponse({"form":html})

    return render(request, "blog/instant_message_detail.html", context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'message', 'poster', 'need_replies']
    success_url = '/main'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = 'posts'
    ordering = ['-date_posted']


@login_required()
def post_detail(request, id):
    if LoginCode.objects.filter(user=request.user).exists():
        hasRead = False
        post = get_object_or_404(Post, id=id)

        if post:
            post.views += 1
            post.save()
            if not post.has_read.filter(id=request.user.id).exists():
                post.has_read.add(request.user)
                hasRead = True

        comments = Comments.objects.filter(post=post).order_by('-date_posted')

        if request.method == "POST":
            form = CommentsForm(request.POST)
            if form.is_valid():
                comment_content = request.POST.get('reply')
                comment = Comments.objects.create(post=post, user=request.user, reply=comment_content)
                comment.save()

        this_time = datetime.now()
        this_min = this_time.minute
        if this_min == CAN_STAY_LOGGED_IN1 or this_min == CAN_STAY_LOGGED_IN2 or this_min == CAN_STAY_LOGGED_IN3 or this_min == CAN_STAY_LOGGED_IN4:
            return redirect('logout')

        else:
            form = CommentsForm()
    else:
        messages.info(request,f"You were logged out")
        return redirect('login')

    context = {
        "post": post,
        'form': form,
        'comments': comments,
        'hasRead': hasRead
    }

    if request.is_ajax():
        html = render_to_string("blog/comment_form.html",
                                context, request=request)
        return JsonResponse({"form": html})
    return render(request, "blog/post_detail.html", context)


@login_required()
def main(request):
    
    if LoginCode.objects.filter(user=request.user).exists():
        on_line_users = Online_user.objects.all()
        unread_count = InstantMessage.objects.filter(recipient=request.user.id).order_by('-date_posted')[:6]
        unread_counts = InstantMessage.objects.filter(recipient=request.user.id, read=False).count

        reports = Report.objects.all().order_by('-date_posted')[:6]
        posts = Post.objects.all().order_by('-date_posted')[:6]
        td = date.today()
        tt = timezone.now()
        ntt = tt.time
        current_events = Events.objects.filter(date_of_event=td)
        this_time = datetime.now()
        this_min = this_time.minute
        if this_min == CAN_STAY_LOGGED_IN1 or this_min == CAN_STAY_LOGGED_IN2 or this_min == CAN_STAY_LOGGED_IN3 or this_min == CAN_STAY_LOGGED_IN4:
            return redirect('logout')
    else:
        messages.info(request,f"You were logged out")
        return redirect('login')
    context = {
        'users': on_line_users,
        'reports': reports,
        'posts': posts,
        'current_events': current_events,
        'unread_count': unread_count,
        'unread_counts': unread_counts
    }

    return render(request, "blog/main.html", context)


class EventCreateView(LoginRequiredMixin, CreateView):
    model = Events
    fields = ['theme', 'venue', 'date_of_event',
              'event_poster', 'description_of_event']
    success_url = '/events'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class EventDetailView(LoginRequiredMixin, DetailView):
    model = Events


@login_required()
def user_activities(request):
    if LoginCode.objects.filter(user=request.user).exists():
        users = User.objects.all().count()
        volunteers = Volunteer.objects.all().count()
        partners = Partnership.objects.all().count()
        # reports = Report.objects.all().order_by('-date_posted').count()
        subscribers = NewsLetter.objects.all().count()
        msg_system = InstantMessage.objects.all().count()

        this_time = datetime.now()
        this_min = this_time.minute
        if this_min == CAN_STAY_LOGGED_IN1 or this_min == CAN_STAY_LOGGED_IN2 or this_min == CAN_STAY_LOGGED_IN3 or this_min == CAN_STAY_LOGGED_IN4:
            return redirect('logout')
    else:
        messages.info(request,f"You were logged out")
        return redirect('login')

    context = {
        "users": users,
        "volunteers": volunteers,
        "partners": partners,
        # "report": reports,
        "subscribers": subscribers,
        "msg_system": msg_system
    }

    if request.is_ajax():
        return HttpResponse(context)

    return render(request, "blog/activities.html", context)


def gallery(request):
    gallery = Gallery.objects.all().order_by('-date_posted')
    context = {
        "gallery": gallery
    }
    return render(request, "blog/gallery.html", context)




def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request,request.POST)
        if form.is_valid():
            uname = request.POST['username']
            upassword = request.POST['password']
            user = authenticate(username=uname, password=upassword)
            if user is not None:
                login(request,user)
                if not LoginCode.objects.filter(user=user).exists():
                    LoginCode.objects.create(user=user)
                if not Online_user.objects.filter(user=user).exists():
                    Online_user.objects.create(user=user)
                # messages.success(request, f"login success")
                return redirect('main')
                # Redirect to a success page.
            else:
                messages.info(request,f"invalid username or password")
        else:
                messages.info(request,f"invalid information given")
    else:
        form = AuthenticationForm()

    context = {
        "form": form
    }

    return render(request,"users/login.html",context)


@login_required()
def logout(request):
    try:

        ul = LoginCode.objects.filter(user=request.user)
        on_user = Online_user.objects.filter(user=request.user)
        
        if ul:
            ul.delete()
        if on_user:
            on_user.delete()
        del request.session['username']

    except:
      pass

    return render(request,"blog/logout.html")


   
   
