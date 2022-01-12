import datetime as dt
import os
import re

import psutil
from flask import render_template

from app.main import bp


@bp.route('/', methods=['GET'])
def credit_dict():
    sys_info = [wrap('CPU count', psutil.cpu_count()),
                wrap('CPU percent', psutil.cpu_percent(interval=1, percpu=True)),
                wrap('Memory', psutil.virtual_memory()),
                wrap('Swap', psutil.swap_memory()),
                wrap('Disk part', psutil.disk_partitions()),
                wrap('Disk usage', psutil.disk_usage('/')),
                wrap('Environ', psutil.Process().environ())]

    return render_template('index.html', sys_info=sys_info, version=get_version())


def wrap(title, value):
    return title, str(value)


basedir = os.path.abspath(os.path.dirname(__file__))
git_path = os.path.join(basedir, '../../git.properties')


def get_version():
    with open(git_path, 'r') as file:
        lines = []
        for line in file:
            lines.append(line)
        commit = get_commit(lines)
        commit = commit if commit else ''
        date = get_date(lines)
        date = ' от ' + date if date else ''
        return commit + date


commit_patter = 'commit'
date_patter = 'date'
commit_re = re.compile(commit_patter + ' .......')


def get_commit(lines):
    for line in lines:
        match = commit_re.match(line)
        if match:
            return match.group(0).replace(commit_patter, '')
    return None


def get_date(lines):
    for line in lines:
        if line.__contains__(date_patter):
            date_str = line.replace(date_patter, '').strip()
            date = dt.datetime.strptime(date_str, '%a %b %d %H:%M:%S %Z %Y')
            return date.strftime('%d.%m.%Y %H:%M:%S')
    return None
