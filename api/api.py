


import logging
import sys
import argparse
from sanic import Sanic, Blueprint
from sanic.response import json as json_response
from sanic_openapi import openapi2_blueprint, doc
import json
from time import perf_counter
from distutils import util


from render_service import render



logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(filename)s %(lineno)d %(message)s"
)

app = Sanic("stitch_render_selenium")
app.blueprint(openapi2_blueprint)

# http://172.31.16.183:3001/swagger/
arg_parser = argparse.ArgumentParser(description='Api')
arg_parser.add_argument("--port", type=int, help='启动端口', default=3001)
args = arg_parser.parse_args()


@app.before_server_start
async def setup(app, loop) :
    app.ctx.render = render


@app.middleware('request')
def add_start_time(request):
    request.ctx.start_time = perf_counter()
    
@app.middleware('response')
def add_cost_time(request, response) :
    cost = (perf_counter() - request.ctx.start_time)*1000
    logging.info("response : {} {:.2f}ms ; {} {} {} {}".format(response.status, cost, request.method,
                                           request.path, request.args, json.dumps(request.json)))    


@app.get('selenium/render')
@doc.consumes(doc.String(name="url"), location="query", required=True)
@doc.consumes(doc.String(name="user_agent"), location="query", required=False)
@doc.consumes(doc.String(name="cookies"), location="query", required=False)
@doc.consumes(doc.String(name="proxy_url"), location="query", required=False)
@doc.consumes(doc.String(name="javascript"), location="query", required=False)
@doc.consumes(doc.Integer(name="loading_page_timeout"), location="query", required=False)
@doc.consumes(doc.Boolean(name="refresh"), location="query", required=False)
@doc.consumes(doc.Boolean(name="disable_proxy"), location="query", required=False)
@doc.consumes(doc.Integer(name="delay"), location="query", required=False)
@doc.consumes(doc.Integer(name="width"), location="query", required=False)
@doc.consumes(doc.Integer(name="height"), location="query", required=False)
def get_render(request):
    url = request.args.get('url')
    logging.info(f"[get_render] ===== url : {url} ; args : {json.dumps(request.args)}")
    try :
        user_agent = request.args.get('user_agent')
        cookies_str = request.args.get('cookies')
        cookies = None
        if cookies_str :
            cookies = {}
            info = [item.strip() for item in cookies_str.split(";")]
            for item in info :
                kv = item.split("=")
                cookies[kv[0]] = kv[1]
        proxy_url = request.args.get('proxy_url')
        javascript = request.args.get('javascript')
        loading_page_timeout = request.args.get('loading_page_timeout')
        refresh = bool(util.strtobool(request.args.get('refresh', 'false')))
        disable_proxy = bool(util.strtobool(request.args.get('disable_proxy', 'false')))
        delay = request.args.get('delay')
        width = request.args.get('width')
        height = request.args.get('height')
        return json_response(request.app.ctx.render(url=url, user_agent=user_agent, cookies=cookies, proxy_url=proxy_url, loading_page_timeout=loading_page_timeout, refresh=refresh, javascript=javascript, disable_proxy=disable_proxy, delay=delay, width=width, height=height))
    except Exception as e :
        logging.exception(e)
        return {'message': str(e)}, 500


app.run(host='0.0.0.0', port=args.port)





