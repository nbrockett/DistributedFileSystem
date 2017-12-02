import random
import dfs.api
import time


if __name__ == '__main__':

    # fs1
    f = dfs.api.open('/etc/blub', 'w')
    f.write(str(random.randint(0, 100000)) * 1000)
    f.close()

    t1 = time.clock()
    f2 = dfs.api.open('/etc/blub', 'r')
    read_content = f2.read()
    # print("read content = ", read_content)
    f2.close()
    t2 = time.clock()

    f = dfs.api.open('/etc/blub', 'w')
    f.write(str(random.randint(0, 100000)) * 1000)
    f.close(cached=True)

    # dfs.api.clear_cache()

    t3 = time.clock()
    f2 = dfs.api.open('/etc/blub', 'r')
    read_content = f2.read()
    # print("read content = ", read_content)
    f2.close()
    t4 = time.clock()

    print("first read required {0} s".format(t2-t1))
    print("cached read required {0} s".format(t4-t3))