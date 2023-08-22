import os

from celery import shared_task
import json
from io import StringIO
from pylint.lint import Run
from pylint.reporters.text import TextReporter
from operation.models import FileModel


@shared_task
def log_handler(file_id):
    file_object = FileModel.objects.get(pk=file_id)
    file_name = file_object.file_name
    file_to_analyze = file_object.file_path.path


    captured_output = StringIO()
    reporter = TextReporter(captured_output)
    Run([file_to_analyze], reporter=reporter, do_exit=False)

    logs = captured_output.getvalue()
    lines = logs.splitlines()

    results = []

    for line in lines:
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

    data = {file_to_analyze: results}

    with open('logs.json', encoding='utf8') as f:
        if not os.path.getsize('logs.json') > 0:
            json_logs([data])
        else:
            datas = json.load(f)
            datas.append(data)
            json_logs(datas)


def json_logs(data):
    with open("logs.json", "w", encoding='utf8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)
