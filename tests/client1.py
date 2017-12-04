import random
import dfs.api
import time


if __name__ == '__main__':

    # fs1
    print("---------\ntesting FS1\n---------")
    print("writing to file '/etc/blub'")
    f1 = dfs.api.open('/etc/blub', 'w')
    f1.write(str(random.randint(0, 100000)) * 5)
    f1.close()

    print("reading from file '/etc/blub'")
    f2 = dfs.api.open('/etc/blub', 'r')
    read_content = f2.read()
    print("read content = ", read_content)
    f2.close()

    # fs2
    print("---------\ntesting FS2\n---------")
    print("writing to file '/home/my_file2'")
    f3 = dfs.api.open('/home/my_file', 'w')
    f3.write(str(random.randint(0, 100000)) * 5)
    f3.close()

    print("reading from file '/home/my_file2'")
    f4 = dfs.api.open('/home/my_file', 'r')
    read_content = f4.read()
    print("read content = ", read_content)
    f4.close()

    # fs1
    print("---------\ntesting locking\n---------")
    print("writing to file '/etc/blub' without closing")
    f5 = dfs.api.open('/etc/blub', 'w')
    f5.write(str(random.randint(0, 100000)) * 5)
    # f1.close()

    time.sleep(15)
    print("run client 2 now. 15 seconds time to test")

    f5.close()





    # # fs2
    # f3 = dfs.api.open('/home/my_file2', 'w')
    # f3.write(str(random.randint(0, 100000)) * 5)
    # f3.close()
    #
    # f4 = dfs.api.open('/home/my_file2', 'r')
    # read_content = f4.read()
    # print("read content = ", read_content)
    # f4.close()

