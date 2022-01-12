import json
import time

import psutil
from flask import request, make_response, jsonify, current_app

from app.api import bp
from app.executor import executor


@bp.route('/execute', methods=['POST'])
def execute():
    req_json = request.get_json()
    uuid = req_json['uuid'] or {}
    env = req_json['env'] or {}
    data = req_json['notebook'] or {}
    current_app.logger.info('Получен запрос с параметрами: {uuid: %s, env: %s}', uuid, env)
    current_app.logger.info('RAM доступно до выполнения запроса с uuid {}: {} MB'.format(uuid, psutil.virtual_memory().available / 1048576))
    current_app.logger.info('Загрузка CPU до выполнения запроса с uuid {}: {} %'.format(uuid, psutil.cpu_percent()))

    data = json.dumps(data, ensure_ascii=False)
    script_start_time = time.time()
    result = executor.Executor(data, uuid, env).execute()
    script_evaluate_time = time.time() - script_start_time
    current_app.logger.info('Запрос с uuid: %s выполнен за %s секунд', uuid, round(script_evaluate_time, 3))

    return make_response(jsonify(result.serialize()))
