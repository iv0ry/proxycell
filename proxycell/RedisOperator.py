# -*- coding: utf-8 -*-
import sys
sys.path.append("D:\\workshop\\python\\proxycell")
from proxycell.othersettings import REDIS_HOST, REDIS_PORT, REDIS_POOL_NAME
import redis

redis_pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, max_connections=20)


class RedisOperator(object):
    """Redis 操作类"""

    def __init__(self):
        """初始化 Redis 连接"""
        # self._conn = redis.Po(HOST, PORT)
        print('初始化 Redis 连接')
        self._conn = redis.Redis(connection_pool=redis_pool)

    def gets(self, total=1):
        """从池中返回给定数量的代理(取出但不删除)，当 total > pool.size
        时，将返回 pool.size 个代理。
        :param total: 返回的数量
        :return: proxies, size=total
        """
        tmp = self._conn.srandmember(REDIS_POOL_NAME, total)
        return [s.decode('utf-8') for s in tmp]

    def get_all(self):
        tmp = self._conn.smembers(REDIS_POOL_NAME)
        return [s.decode('utf-8') for s in tmp]

    def puts(self, proxies):
        """将一定量的代理压入 pool 中
        :param proxies:
        :return:
        """
        self._conn.sadd(REDIS_POOL_NAME, *proxies)

    def pop(self):
        """弹出一个代理(取出并删除)
        :return: proxy
        """
        # if self.size == 0:
        #     raise PoolEmptyError
        return self._conn.spop(REDIS_POOL_NAME).decode('utf-8')

    @property
    def size(self):
        """返回 pool 的 size
        :return: pool.size
        """
        return self._conn.scard(REDIS_POOL_NAME)

    def del_current(self):
        '''删除该 POOL_NAME key 下的全部内容
        :return: None
        '''
        self._conn.delete(REDIS_POOL_NAME)

    def _flush(self):
        """清空 Redis 中的全部内容
        :return: None
        """
        self._conn.flushall()

