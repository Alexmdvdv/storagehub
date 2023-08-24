import smtplib
from celery import shared_task

from operation.models import FileModel
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from operation.utils import pylint_code, has_data_json
from service import settings


@shared_task
def read_logs(file_id):
    file_object = FileModel.objects.get(pk=file_id)
    lines = pylint_code(file_object.file_path.path)
    results = []

    for line in lines:
        parts = line.strip().split(": ")
        if len(parts) >= 3:
            location, code, message = parts
            file, line, column = location.split(":")
            results.append({
                "file": file_object.file_name,
                "line_number": line,
                "col_number": column,
                "code": code,
                "message": message
            })

    has_data_json({file_object.file_path.path: results})
    send_email.delay(results)


@shared_task
def send_email(results):
    try:
        subject = 'Результат проверки файла'
        from_email = settings.EMAIL_HOST_USER
        to_email = ['recipient@example.com']

        html_content = render_to_string('email.html', {'results': results})
        text_content = strip_tags(html_content)

        msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
        msg.attach_alternative(html_content, "text/html")

        connection = msg.get_connection()
        connection.open()
        msg.send()
        connection.close()

    except smtplib.SMTPException as e:

        print(f"Ошибка при отправке письма: {e}")
