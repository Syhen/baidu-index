# -*- coding: utf-8 -*-
"""
create on 2018-10-09 下午9:06

author @heyao
"""
import base64
import json

from flask import Flask, render_template, request, abort

app = Flask(__name__)


@app.route('/baidu/res2', methods=['GET', 'POST'])
def baidu_res2():
    if request.method == 'POST':
        js_code = request.json.get("js_code", None)
        js_code_str = '\n                '.join(js_code)
        if js_code is None:
            js_code = request.data.get("js_code", None)
            js_code_str = js_code
        if js_code is None:
            abort(400)
        return render_template('res2.html', js=js_code_str)
    js_code = request.args.get("js_code", None)
    if not js_code:
        abort(400)
    js_code_str = '\n                '.join(json.loads(base64.b64decode(js_code)))
    return render_template('res2.html', js=js_code_str)


if __name__ == '__main__':
    app.run('localhost', 8008, debug=True)
