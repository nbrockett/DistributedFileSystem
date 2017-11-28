import random
import dfs.api

if __name__ == '__main__':

    # fs1
    f = dfs.api.open('/etc/blub', 'w')
    f.write(str(random.randint(0, 100000)) * 5)
    f.close()

    f2 = dfs.api.open('/etc/blub', 'r')
    read_content = f2.read()
    print("read content = ", read_content)
    f2.close()


    # fs1
    f = dfs.api.open('/home/my_file2', 'w')
    f.write(str(random.randint(0, 100000)) * 5)
    f.close()

    f2 = dfs.api.open('/home/my_file2', 'r')
    read_content = f2.read()
    print("read content = ", read_content)
    f2.close()