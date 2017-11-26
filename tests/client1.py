import random
import dfs.api

if __name__ == '__main__':

    # f = dfs.api.open('etc/my_file', 'w') # handle later
    f = dfs.api.open('my_file', 'w')
    f.write(str(random.randint(0, 100000)) * 5)
    f.close()

    f2 = dfs.api.open('my_file', 'r')
    read_content = f2.read()
    print("read content = ", read_content)
    f2.close()