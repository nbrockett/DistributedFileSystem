import random
import dfs.api
import time


if __name__ == '__main__':

    # fs1
    print("---------\ntesting FS1\n---------")
    print("writing to file '/etc/aag'")
    f1 = dfs.api.open('/etc/aag', 'w')
    f1.write(str(random.randint(0, 100000)) * 5)
    f1.close()

    print("reading from file '/etc/aag'")
    f2 = dfs.api.open('/etc/aag', 'r')
    read_content = f2.read()
    print("read content = ", read_content)
    f2.close()

    # fs2
    print("---------\ntesting FS2\n---------")
    print("writing to file '/home/my_file'")
    f3 = dfs.api.open('/home/my_file', 'w')
    f3.write(str(random.randint(0, 100000)) * 5)
    f3.close()

    print("reading from file '/home/my_file'")
    f4 = dfs.api.open('/home/my_file', 'r')
    read_content = f4.read()
    print("read content = ", read_content)
    f4.close()


    # reading into same file
    print("reading from file '/home/my_file' first time")
    fa = dfs.api.open('/home/my_file', 'r')
    read_content = fa.read()

    print("reading from file '/home/my_file' second time")
    fb = dfs.api.open('/home/my_file', 'r')
    read_content = fb.read()

    fa.close()
    fb.close()

    # fs1
    print("---------\ntesting locking\n---------")
    print("writing to file '/etc/blub' without closing")
    f5 = dfs.api.open('/etc/blub', 'w')
    f5.write(str(random.randint(0, 100000)) * 5)
    # f1.close()

    print("Try to execute client2.py now, for simultaneous access")
    time.sleep(15)
    f5.close()

