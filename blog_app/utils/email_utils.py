from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_dynamic_email(req,username,email,task):
    context={
        'user_name':username,
        'user_email':email,
        'site_name':'vandhanaSite'
    }
    if task=='welcome_email':
        html_content=render_to_string('email/welcome_email.html',context)
    elif task=='comment_added':
        html_content=render_to_string('email/comment_added.html',context)

    text_content=strip_tags(html_content)

    email=EmailMultiAlternatives(
        subject="welcome to Vandhana's django practice session🎉✔️",
        body=text_content,
        from_email='vandhanamulguri@gmail.com',
        to=[email]
    )
    email.attach_alternative(html_content,"text/html")
    email.send()