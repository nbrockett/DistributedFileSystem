# DistributedFileSystem

The distributed file system uses an AFS approach, where a temporary file is created on the client side. 
Once manipulations are finished on the client side the file is sent back to the distributed file system.
Multiple directories can be served by multiple file server. The directory server is responsible for mapping
the file directories to the respective file server. A locking server assures that no two client can gain write 
access to the same file at the same time. 

Follow features have been implemented:

- Distributed File System
- Directory Server
- Locking Server
- Caching


## Setup 

This Project was built using Python 3.6 and Flask

Setting up the servers can be done by running the following commands:

```
python directory_server.py --host=[HOST_IP] --port=[PORT]
python file_server.py --host=[HOST_IP] --port=[PORT] --config=[.json config]
python locking_server.py --host=[HOST_IP] --port=[PORT]      
```
The servers need to be started in that given order


The file server requires a config file which needs to have the same directory server address
as given above.

The client requires a servers.json config file which contains both directory server
and locking server address.

## Testing

Testing is done using three client files: client1.py, client2.py, client_caching.py

client1.py:

- Opens the dsf API, and creates a temporary file with the open command
- writes and reads into a file with directory '/etc'
- writes and reads into a file hosted by a different file server with directory '/home'
- These serving directories are specified in the config file of each file server
- Reads into the same file without any problems.
- writes again into '/etc' but does not close. If a second client from client2.py writes into the same file
  access will be denied and the locking server will be polled until it is freed. After 15 seconds client1 closes
  the file and client2 has write access again
  
client2.py
 
- used to test multiple write access. See last point in client1.py

client_caching.py

- reads a file once from cache and once not. Display the cache saved in the api. Takes the time required for operation.