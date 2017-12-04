import random
import dfs.api
import time



if __name__ == '__main__':

    # fs1
    print("writing to file '/etc/blub'")
    f = dfs.api.open('/etc/blub', 'w')
    f.write(str(random.randint(0, 100000)) * 5)
    # f.close()

    # f2 = dfs.api.open('/etc/blub', 'r')
    # read_content = f2.read()
    # print("read content = ", read_content)
    # f2.close()


    # # fs2
    # f3 = dfs.api.open('/home/my_file2', 'w')
    # f3.write(str(random.randint(0, 100000)) * 5)
    # f3.close()
    #
    # f4 = dfs.api.open('/home/my_file2', 'r')
    # read_content = f4.read()
    # print("read content = ", read_content)
    # f4.close()

    time.sleep(7)
    f.close()