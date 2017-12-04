import random
import dfs.api

if __name__ == '__main__':

    # fs1
    print("writing to file '/etc/blub'")
    f = dfs.api.open('/etc/blub', 'w')
    f.write(str(random.randint(0, 100000)) * 1)
    f.close()