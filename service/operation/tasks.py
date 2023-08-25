import smtplib
from celery import shared_task
from django.contrib.auth.models import User

from operation.models import FileModel
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from operation.utils import pylint_code, has_data_json
from service import settings
from django.db.models import Q


@shared_task
def check_file():
    files = FileModel.objects.filter(verified=False)

    for file in files:
        user_id = file.user.id
        file_path = file.file.path
        file_id = file.id
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

        file_info = {"file_path": file_path, "user_id": user_id, "file_id": file_id}
        send_email.delay(results, file_info)


@shared_task
def send_email(results, file_info):
    user = User.objects.get(id=file_info.get("user_id"))
    user_email = user.email

    try:
        subject = 'Результат проверки файла'
        from_email = settings.EMAIL_HOST_USER
        to_email = [user_email]
        html_content = render_to_string('email.html', {'results': results})
        text_content = strip_tags(html_content)

        msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
        msg.attach_alternative(html_content, "text/html")

        connection = msg.get_connection()
        connection.open()
        msg.send()
        connection.close()

        path = file_info.get("file_path")
        has_data_json({path: results, "email": "Отчет отправлен на почту"})

        verified = FileModel.objects.get(id=file_info.get("file_id"))
        verified.verified = True
        verified.save()

    except smtplib.SMTPException as e:
        print(f"Ошибка при отправке письма: {e}")
