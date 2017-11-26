import random
import dfs.api

if __name__ == '__main__':

    f = dfs.api.open('my_file', 'w')
    f.write(str(random.randint(0, 100000)) * 5)
    f.close()

