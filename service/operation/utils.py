import os
import json
from io import StringIO
from pylint.lint import Run
from pylint.reporters.text import TextReporter


def pylint_code(file):
    output = StringIO()
    reporter = TextReporter(output)
    Run([file], reporter=reporter, do_exit=False)

    logs = output.getvalue()
    lines = logs.splitlines()
    return lines


def has_data_json(data):
    with open('logs.json', encoding='utf8') as f:
        if not os.path.getsize('logs.json') > 0:
            save_data_json([data])

        else:
            datas = json.load(f)
            datas.append(data)
            save_data_json(datas)


def save_data_json(data):
    with open("logs.json", "w", encoding='utf8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)


