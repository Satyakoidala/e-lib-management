from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def mailTemplateOne(student, book):
    html_message = render_to_string('librarian/mailtemp1.html', {
        'student': student,
        'book': book,
    })
    plain_message = strip_tags(html_message)
    send_mail(
        "Due date is Near!!",
        plain_message,
        'koidalasai21@gmail.com',
        [student.email],
        html_message=html_message
    )


def mailTemplateTwo(student, book):
    html_message = render_to_string('librarian/mailtemp2.html', {
        'student': student,
        'book': book,
    })
    plain_message = strip_tags(html_message)
    send_mail(
        "Attention!!",
        plain_message,
        'koidalasai21@gmail.com',
        [student.email],
        html_message=html_message
    )
