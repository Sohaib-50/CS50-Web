import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Email


def index(request):

    # Authenticated users view their inbox
    if request.user.is_authenticated:
        return render(request, "mail/inbox.html")

    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("login"))


@csrf_exempt
@login_required
def compose(request):

    # Composing a new email must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Check recipient emails
    data = json.loads(request.body)
    emails = [email.strip() for email in data.get("recipients").split(",")]
    if emails == [""]:
        return JsonResponse({
            "error": "At least one recipient required."
        }, status=400)

    # Convert email addresses to users
    recipients = []
    for email in emails:
        try:
            user = User.objects.get(email__iexact=email)
            recipients.append(user)
        except User.DoesNotExist:
            return JsonResponse({
                "error": f"User with email {email} does not exist."
            }, status=400)

    # Get contents of email
    subject = data.get("subject", "")
    body = data.get("body", "")

    # Create one email for each recipient, plus sender
    users = set()
    users.add(request.user)
    users.update(recipients)
    for user in users:
        email = Email(
            user=user,
            sender=request.user,
            subject=subject,
            body=body,
            read=user == request.user
        )
        email.save()
        for recipient in recipients:
            email.recipients.add(recipient)
        email.save()

    return JsonResponse({"message": "Email sent successfully."}, status=201)


@login_required
def mailbox(request, mailbox):

    # Filter emails returned based on mailbox
    if mailbox == "inbox":
        emails = Email.objects.filter(
            user=request.user, recipients=request.user, archived=False
        )
    elif mailbox == "sent":
        emails = Email.objects.filter(
            user=request.user, sender=request.user
        )
    elif mailbox == "archive":
        emails = Email.objects.filter(
            user=request.user, recipients=request.user, archived=True
        )
    else:
        return JsonResponse({"error": "Invalid mailbox."}, status=400)

    # Return emails in reverse chronologial order
    emails = emails.order_by("-timestamp").all()
    return JsonResponse([email.serialize() for email in emails], safe=False)


@csrf_exempt
@login_required
def email(request, email_id):

    # Query for requested email
    try:
        email = Email.objects.get(user=request.user, pk=email_id)
    except Email.DoesNotExist:
        return JsonResponse({"error": "Email not found."}, status=404)

    # Return email contents
    if request.method == "GET":
        return JsonResponse(email.serialize())

    # Update whether email is read or should be archived
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("read") is not None:
            email.read = data["read"]
        if data.get("archived") is not None:
            email.archived = data["archived"]
        email.save()
        return HttpResponse(status=204)

    # Email must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "mail/login.html", {
                "message": "Invalid email and/or password."
            })
    else:
        return render(request, "mail/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "mail/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(email, email, password)
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "mail/register.html", {
                "message": "Email address already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "mail/register.html")


def send_random_emails(request):
    emails = [
        {
            'subject': 'Hello',
            'body': 'Hi there'
        },
        {
            'subject': 'Hello again',
            'body': 'Hi there again'
        },
        {
            'subject': 'Ameeting',
            'body': '''We need to discuss a few things. Here are the details:
            Date: 1st Jan 2021
            Time: 9:00 AM
            Venue: Conference Hall'''
        },
        {
            'subject': 'Meeting minutes',
            'body': '''Hi there
            The minutes of the last meeting are as follows:
            1. We discussed the budget.
            2. We discussed the timeline.
            3. We discussed the venue for the upcoming meeting.'''
        },
        {
            'subject': 'Venting',
            'body': '''Hi there
            I'm just sending this email to vent out my frustration.
            I'm not really looking for a response.

            My situation is as follows:
            1. I'm not getting enough sleep.
            2. I'm not getting enough exercise.
            3. I'm not eating healthy food.

            I need to change my lifestyle

            I feel like I'm going to explode.
            While I'm at it, I might as well add a few more lines to this email.
            I'm really frustrated.
            I'm really really frustrated.
            I'm really really really frustrated.
            Also, I'm really really really really frustrated.'''
        },
        {
            'subject': 'Holiday Greetings',
            'body': '''Dear friends and family,

            Wishing you a joyful holiday season and a Happy New Year! May this festive season bring you warmth, happiness, and memorable moments with your loved ones.

            Looking forward to catching up in the coming year.

            Warm regards,
            Blaah'''
        },
        {
            'subject': 'Project Update',
            'body': '''Hello team,
            I wanted to provide a quick update on the project.
            We've made significant progress in the last week, and I'm excited about the results.

            Key achievements:
            - Completed the design phase
            - Implemented critical features
            - Resolved several bugs

            Looking forward to our upcoming sprint planning meeting.

            Best regards,
            [Your Name]'''
        },
        {
            'subject': 'Happy Birthday!',
            'body': '''Dear blooh,

            Happy Birthday! I hope you have a wonderful day and get everything you want.

            Best wishes,
            Blaah'''
        }
    ]

    receivers = ["sohaibahmedabbasi2@gmail.com" if request.user.email.lower() != "sohaibahmedabbasi2@gmail.com" else "sohaibahmedabbasi0@gmail.com"]
    print(request.user.email)
    recipients = []
    for email in receivers:
        try:
            user = User.objects.get(email__iexact=email)
            recipients.append(user)
        except User.DoesNotExist:
            return JsonResponse({
                "error": f"User with email {email} does not exist."
            }, status=400)
        
    # create one email for each recipient, plus sender
    users = set()
    users.add(request.user)
    users.update(recipients)

    for user in users:
        for email in emails:
            email = Email(
                user=user,
                sender=request.user,
                subject=email['subject'],
                body=email['body'],
                read=user == request.user
            )
            email.save()
            for recipient in recipients:
                email.recipients.add(recipient)
            email.save()

    return JsonResponse({"message": "Emails sent successfully."}, status=201)

