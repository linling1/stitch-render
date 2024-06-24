


import logging
import sys
import argparse
from sanic import Sanic, Blueprint
from sanic.response import json as json_response
from sanic_openapi import openapi2_blueprint, doc
import json
from time import perf_counter
from distutils import util


from render_service import RenderService



logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(filename)s %(lineno)d %(message)s"
)

app = Sanic("stitch_render_drission_page")
app.blueprint(openapi2_blueprint)

# http://172.31.16.183:3001/swagger/
arg_parser = argparse.ArgumentParser(description='Api')
arg_parser.add_argument("--port", type=int, help='启动端口', default=3001)
arg_parser.add_argument("--workers", type=int, help='进程数', default=1)
arg_parser.add_argument("--env", type=str, help='启动环境', default="prod")
args = arg_parser.parse_args()


@app.before_server_start
async def setup(app, loop) :
    config = {}
    if args.env == "prod" :
        from config.prod_conf import config
    elif args.env == "linling" :
        from config.linling_conf import config
    app.ctx.render_service = RenderService(**config)


@app.middleware('request')
def add_start_time(request):
    request.ctx.start_time = perf_counter()
    
@app.middleware('response')
def add_cost_time(request, response) :
    cost = (perf_counter() - request.ctx.start_time)*1000
    if isinstance(response, tuple) :
        err_data, status_code = response
        logging.info("response : {} {:.2f}ms ; {} {}".format(status_code, cost, json.dumps(err_data)))    
    else :
        logging.info("response : {} {:.2f}ms ; {} {} {} {}".format(response.status, cost, request.method,
                                           request.path, request.args, json.dumps(request.json)))    


@app.get('drission_page/render')
@doc.consumes(doc.String(name="url"), location="query", required=True)
@doc.consumes(doc.String(name="user_agent"), location="query", required=False)
@doc.consumes(doc.String(name="headers"), location="query", required=False)
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
        headers_str = request.args.get('headers')
        headers = None
        if headers_str :
            headers = {}
            info = [item.strip() for item in headers_str.split(";")]
            for item in info :
                kv = item.split("=", 1)
                headers[kv[0]] = kv[1]
        proxy_url = request.args.get('proxy_url')
        javascript = request.args.get('javascript')
        loading_page_timeout = request.args.get('loading_page_timeout')
        refresh = bool(util.strtobool(request.args.get('refresh', 'false')))
        disable_proxy = bool(util.strtobool(request.args.get('disable_proxy', 'false')))
        delay = request.args.get('delay')
        width = request.args.get('width')
        height = request.args.get('height')
        return json_response(request.app.ctx.render_service.render(url=url, user_agent=user_agent, headers=headers, proxy_url=proxy_url, loading_page_timeout=loading_page_timeout, refresh=refresh, javascript=javascript, disable_proxy=disable_proxy, delay=delay, width=width, height=height))
    except Exception as e :
        logging.exception(e)
        return {'message': str(e)}, 500


@app.post('drission_page/render')
@doc.consumes(doc.JsonBody(), location="body", required=True)
def post_render(request):
    body = request.json
    url = body.get('url')
    logging.info(f"[post_render] ===== url : {url} ; args : {json.dumps(request.args)}")
    try :
        user_agent = body.get('user_agent')
        headers = body.get('headers')
        cookies = body.get('cookies')
        proxy_url = body.get('proxy_url')
        javascript = body.get('javascript')
        loading_page_timeout = body.get('loading_page_timeout')
        refresh = body.get('refresh', False)
        if isinstance(refresh, str) :
            refresh = bool(util.strtobool(refresh))
        disable_proxy = body.get('disable_proxy', False)
        delay = body.get('delay')
        width = body.get('width')
        height = body.get('height')
        return json_response(request.app.ctx.render_service.render(url=url, user_agent=user_agent, headers=headers, cookies=cookies, proxy_url=proxy_url, loading_page_timeout=loading_page_timeout, refresh=refresh, javascript=javascript, disable_proxy=disable_proxy, delay=delay, width=width, height=height))
    except Exception as e :
        logging.exception(e)
        return {'message': str(e)}, 500    


app.run(host='0.0.0.0', port=args.port, workers=args.workers)





