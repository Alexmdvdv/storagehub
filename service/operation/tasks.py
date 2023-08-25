import smtplib
from celery import shared_task

from operation.models import FileModel
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from operation.utils import pylint_code, has_data_json


@shared_task
def check_file():
    files_for_review = FileModel.objects.filter(is_new=True)
    for file in files_for_review:
        file_path = file.file.path
        file_name = file.name
        lines_log = pylint_code(file_path)

        results = []

        for line in lines_log:
            parts = line.strip().split(": ")
            if len(parts) >= 3:
                location, code, message = parts
                file, line, column = location.split(":")

                results.append({
                    "file": file_name,
                    "line_number": line,
                    "col_number": column,
                    "code": code,
                    "message": message
                })

        send_email.delay(results, file_path)


@shared_task
def send_email(results, file_path):
    try:
        subject = 'Результат проверки файла'
        from_email = '63065523a0174b'
        to_email = ['recipient@example.com']
        html_content = render_to_string('email.html', {'results': results})
        text_content = strip_tags(html_content)

        msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
        msg.attach_alternative(html_content, "text/html")

        connection = msg.get_connection()
        connection.open()
        msg.send()
        connection.close()

        has_data_json({file_path: results, "email": "Отчет отправлен на почту"})

    except smtplib.SMTPException as e:

        print(f"Ошибка при отправке письма: {e}")
