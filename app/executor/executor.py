import os
import shutil
import subprocess
from tempfile import gettempdir

from dotenv import set_key
from flask import current_app
from ipynb_py_convert import convert


class Executor(object):
    def __init__(self, data, uuid, env):
        self.uuid = uuid
        self.data = data
        self.env = env
        self.curr_share_path = os.path.join(os.path.normpath(os.getenv('WORKDIR_PATH')), uuid)
        self.run_path = os.path.join(gettempdir(), uuid)
        self.local_share_path = os.path.join(self.run_path, uuid)
        self.share_folder_is_empty = True if not os.path.exists(self.curr_share_path) else False

    def prepare_work_dir(self):
        os.makedirs(self.run_path, exist_ok=True)
        with open(os.path.join(self.run_path, 'notebook.ipynb'), 'w') as nb_file:
            nb_file.write(self.data)
        convert(os.path.join(self.run_path, 'notebook.ipynb'), os.path.join(self.run_path, 'notebook.py'))
        os.remove(os.path.join(self.run_path, 'notebook.ipynb'))
        if self.share_folder_is_empty: os.makedirs(self.curr_share_path)
        os.symlink(self.curr_share_path, self.local_share_path)

    def clear(self):
        os.unlink(self.local_share_path)
        shutil.rmtree(self.run_path, ignore_errors=True)
        if self.share_folder_is_empty: shutil.rmtree(self.curr_share_path)

    def create_env(self):
        open(os.path.join(self.run_path, '.env'), 'w').close()
        for key, value in self.env.items():
            set_key(dotenv_path=os.path.join(self.run_path, '.env'), key_to_set=key, value_to_set=value)

    def execute(self):
        try:
            self.prepare_work_dir()
            self.create_env()
            self.check_files_size()
        except Exception as e:
            current_app.logger.error(e)
            self.clear()
            return Result(error=str(e))

        p = subprocess.Popen('cd {} && python {}'.format(self.run_path, os.path.join(self.run_path, 'notebook.py')),
                             stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        output, errors = p.communicate()
        if p.returncode != 0:
            current_app.logger.error(errors.decode('utf-8'))
            self.clear()
            return Result(error=errors.decode('utf-8'))
        self.clear()
        return Result()

    def check_files_size(self):
        size_logs = {}
        for filename in os.listdir(self.local_share_path):
            size_logs.update(
                {filename: '{0} bytes'.format(os.path.getsize(os.path.join(self.local_share_path, filename)))})
        current_app.logger.info('Файлы, полученные с запросом с uuid=%s: %s', self.uuid, size_logs)


class Result(object):
    def __init__(self, error=None):
        self.error = error

    def serialize(self):
        return {'error': self.error}
