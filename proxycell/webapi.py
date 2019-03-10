# -*- coding: utf-8 -*-
import sys
sys.path.append("D:\\workshop\\python\\proxycell")
from flask import Flask,g
from flask_restful import reqparse, abort, Api, Resource
from RedisOperator import RedisOperator
from flask import render_template
from tester import *

app = Flask(__name__)
api = Api(app)

# class HelloWorld(Resource):
#     def get(self):
#         return {'hello': 'world'}

# api.add_resource(HelloWorld, '/h')

ips = {}

class IpSimple(Resource):
    def get(self):
        conn = get_conn()
        return {'ip':conn.gets()[0]}

    # def put(self, todo_id):
        # todos[todo_id] = request.form['data']
        # return {todo_id: todos[todo_id]}

api.add_resource(IpSimple, '/')


def get_conn():
    """获取 Redis 连接
    :return: RedisOperator
    """
    if not hasattr(g, 'redis_connect'):
        g.redis_connect = RedisOperator()
    return g.redis_connect

@app.route('/raw')
def get_raw():
    conn=get_conn()
    #获取全部
    raw_inall=[]
    raw_inall=conn.get_all()
    #测试可用
    _tester=UsabilityTester()
    _tester.set_raw_proxies(raw_inall)
    _tester.test()
    proxies = _tester.usable_proxies
    conn.del_current()
    conn.puts(proxies)

    return str(proxies)

@app.route('/chm')
def get_chm():
    """
    """
    return render_template('Spells_CRB_A-D.htm')


@app.route('/get')
def get_proxy():
    """Web API IP获取页的 HTML 代码
    :return: HTML
    """
    conn = get_conn()
    return conn.pop()


@app.route('/count')
def get_counts():
    """Get the count of proxies
    :return: HTML
    """
    pool = get_conn()
    return str(pool.size)

@app.route('/fillpool')
def fill_pool():
    """手动补满代理池
    """
    #adder=PoolAdder()
    try:
        
        #adder.add_to_pool()
        return "ok"
    except Exception as e:
        print(e)
        #logging.exception(e)
        return "Exception"
    except:
        return "fail"

if __name__ == '__main__':
    app.run(debug=True)