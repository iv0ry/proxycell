import asyncio
import aiohttp
import time

class UsabilityTester(object):
    """检验器，负责检验给定代理的可用性。"""
    test_api = 'https://www.baidu.com'

    def __init__(self):
        self.raw_proxies = None
        self._usable_proxies = None

    def set_raw_proxies(self, raw_proxies):
        self.raw_proxies = raw_proxies

        self._usable_proxies = []


    async def test_single_proxy(self, proxy):
        async with aiohttp.ClientSession() as sess:
            try:
                real_proxy = 'http://' + proxy
                async with sess.get(self.test_api, proxy=real_proxy, timeout=10) as resp:
                    self._usable_proxies.append(proxy)
            except Exception:
                print("e",end=" ")

    def test(self):
        
        assert self.raw_proxies != None
        print('Usability tester is working....')
        
        try:
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            print('asyncio.get_event_loop() is working...')
            tasks = [self.test_single_proxy(proxy) for proxy in self.raw_proxies]
            print('tasks is working...')
            loop.run_until_complete(asyncio.wait(tasks, loop=loop))
            print('\nrun_until_complete is working...')
            print("done total:"+str(len(self.raw_proxies))+" exists:"+str(len(self._usable_proxies)))
        except Exception:
                print(Exception.__name__+str(time.clock()))
        else:
            print("no err")
        

    @property
    def usable_proxies(self):
        return self._usable_proxies
