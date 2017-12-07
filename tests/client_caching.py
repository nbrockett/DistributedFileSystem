import random
import dfs.api
import time


if __name__ == '__main__':

    # fs1
    f = dfs.api.open('/etc/blub', 'w')
    f.write(str(random.randint(0, 100000)) * 1000)
    f.write(str(random.randint(0, 100000)) * 1000)
    f.write(str(random.randint(0, 100000)) * 1000)
    f.close()

    t1 = time.clock()
    f2 = dfs.api.open('/etc/blub', 'r')
    read_content = f2.read()
    # print("read content = ", read_content)
    f2.close()
    t2 = time.clock()

    print("caching '/etc/blub2'")
    f = dfs.api.open('/etc/blub2', 'w')
    f.write(str(random.randint(0, 100000)) * 1000)
    f.write(str(random.randint(0, 100000)) * 1000)
    f.write(str(random.randint(0, 100000)) * 1000)
    f.close(cached=True)

    # dfs.api.clear_cache()

    print("Current Cache after close: ", dfs.api._cached_files)

    t3 = time.clock()
    f3 = dfs.api.open('/etc/blub2', 'r')
    read_content = f2.read()
    # print("read content = ", read_content)
    f3.close()
    t4 = time.clock()

    print("first read required {0} s".format(t2-t1))
    print("cached read required {0} s".format(t4-t3))
