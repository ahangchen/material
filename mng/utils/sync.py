import threading
import time

__author__ = 'cwh'


# 类的方式, 传递可变参数
def run_in_background(func, *args):
    class ThreadDemo(threading.Thread):
        def __init__(self):  # 线程构造函数
            threading.Thread.__init__(self)

        def run(self):  # 具体的线程运行代码
            func(*args)

    ThreadDemo().start()


# 过程的方式
def new_thread(func, thread_name):
    t = threading.Thread(target=func, name=thread_name)
    t.start()
    # t.join()  # this will wait


if __name__ == '__main__':

    def sleep_print():
        time.sleep(1)
        print(1)
        time.sleep(1)
        print(2)

    new_thread(sleep_print, 'sleep')
    print('this end')