# gRPC Simple  
## A high performance, open source universal RPC framework


[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://grpc.io/)

gRPC is a modern open source high performance Remote Procedure Call (RPC) framework that can run in any environment. It can efficiently connect services in and across data centers with pluggable support for load balancing, tracing, health checking and authentication. It is also applicable in last mile of distributed computing to connect devices, mobile applications and browsers to backend services.

## Why need use gRPC?
- Simple service definition
- Works across languages and platforms
- Start quickly and scale
- Bi-directional streaming and integrated auth

## How to implement in Python?

To can implement gRPC in Python need somethings:

### Prerequisites

* Python 3.5 or higher
* pip version 9.0.1 or higher
If necessary, upgrade your version of pip:

#### Windown
```sh
python -m pip install --upgrade pip
```
#### Linux or Mac OS
```
python3 -m pip install --upgrade pip
```

Notes: 
- Syntax can change depend on OS.
- If you are using env in Linux, pls active env before upgrade pip. To can active and using env in Linux run command:
```
source {your_env}/bin/activate
```

### Install gRPC and gRPC-tool for Python

#### Install gRPC

gRPC can install throught [pip](https://pypi.org/project/grpc/):
```
pip3 install grpcio
```
#### Install gRPC-tools

Python’s gRPC tools include the protocol buffer compiler protoc and the special plugin for generating server and client code from .proto service definitions. 

To install gRPC tools, run:

```
pip3 install grpcio-tools
```
### Development
By default, gRPC uses Protocol Buffers, Google’s mature open source mechanism for serializing structured data (although it can be used with other data formats such as JSON).

So need create a file .proto. In a file .proto need define schema of service include: input and ouput and methods.

```protobuf
syntax = "proto3";

message Person {
  string name = 1;
  int32 id = 2;
  bool married = 3;
}
// The request message containing the user's name.
message RequestInforPerson {
  string name = 1;
}
// The request message containing the user's name.
message RequestCheckMaritalStatus {
  string name = 1;
}
// The response message containing the information of person with name from input
message RespondGetMaritalStatus {
  bool married = 1;
}
service AsillaService {
    rpc getInfor (RequestInforPerson) returns (Person) {}
    rpc checkMarried (RequestCheckMaritalStatus) returns (RespondGetMaritalStatus) {}
}
```
A above example define a service with 2 functions:

- Get fully information of person from a name. 
- Check marital status of person with name 

In .proto to can define a object data structure start by message. Start a service with name "AsillaService" you can change anyname you like. 

To define each function in a service start with structure:

``` 
rpc {option name} (Input format is defined by "message") returns (Format will be respond, it also is defined by message) {}
```

#### Generate gRPC code

```sh
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./person.proto
```
Explain:
* python -m grpc_tools.protoc:  runs the protobuf compiler
* -I ../protobufs: tells the compiler where to find files that your protobuf code imports. 
* --python_out=. --grpc_python_out=.: tells the compiler where to output the Python files.
* ../protobufs/person.proto: is the path to the protobuf file.

You also run throught python code:

```python
from grpc_tools import protoc

protoc.main((
    '',
    '-I.',
    '--python_out=.',
    '--grpc_python_out=.',
    './person.proto',
))
```
Run file python by command:

```
python3 filename.py 
```
If everything is OK, we can see new 2 file person_pb2_grpc.py and person_pb2.py

Tools help us define interfaces in Python. Now we need custom to fit with purpose.  
#### Define Logical Serve

```python
from person_pb2 import Person, RespondGetMaritalStatus
import person_pb2_grpc
import grpc 
from concurrent import futures
import random 

class PersonServer(person_pb2_grpc.AsillaServiceServicer):
    def __init__(self):
        super(person_pb2_grpc.AsillaServiceServicer, self).__init__()
    def getInfor(self, request, context):
        name = request.name    
        id_ = random.randint(1, 1000)
        if id_ / 2 == 0:
            return Person(name = name, id = id_, married = True)
        else:
            return Person(name = name, id = id_, married = False)
    def checkMarried(self, request, context):
        id_ = random.randint(1, 1000)
        if id_ / 2 == 0:
            return RespondGetMaritalStatus(married = False)
        else:
            return RespondGetMaritalStatus(married = True)
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    person_pb2_grpc.add_AsillaServiceServicer_to_server(
        PersonServer(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()
    
if __name__ == "__main__":
    serve()
```
Some attention:
+ gRPC only generate interface of request. So we need implement interface *Servicer 
+ Define logical processs of all methods in a Interface. 
+ When start serverice need care: port, ip and number workers fefault value of max_workers is changed to min(32, os.cpu_count() + 4)

Run in background: to can run service in background os using command:

```
nohup python3 person_server.py >> log.log & 
```
log.log is a file is written all output while service is running. 
#### Define Client

After create a server need define a client to can connect to server:

```python
from person_pb2_grpc import AsillaServiceStub
from person_pb2 import RequestInforPerson, RequestCheckMaritalStatus
import grpc

class PersonGrpcClient:
    def __init__(self, ip, port, client_id="app"):
        self.channel = grpc.insecure_channel("{}:{}".format(ip, port))
        self.person_service_stub = AsillaServiceStub(self.channel)
        self.client_id = client_id
        print("Connect oke")

    def checkMarried(self,_name):
        request = RequestCheckMaritalStatus(name = _name)
        response = self.person_service_stub.checkMarried(request)
        print(response)
    
    def getInfor(self, _name):
        request = RequestInforPerson(name = _name)
        response = self.person_service_stub.getInfor(request)
        print(response.married)

if __name__ == '__main__':
    
    import argparse
    parser = argparse.ArgumentParser(description='AsillaPose Client')
    parser.add_argument('--ip', default="localhost", type=str,
                      help='Ip address of the server')
    parser.add_argument('--port', default=50051, type=int,
                      help='expose port of gRPC server')
    args = parser.parse_args()
    client = PersonGrpcClient(args.ip, args.port)
    client.checkMarried('trung')
    client.getInfor("trung")
```
To can create connect to service need init a object ServiceTub with a parameters include port & ip 

Run client:
```
python3 client.py --ip 127.0.0.1 --port 50051 
```
IP and Port depend define of serice. In a above example, we run in localhost.  


## Issues 

When implement about gRPC has exist some issues

- Install wrong libraries: Can you installed grpc, Correct library is grpcio 
- Meet a exception look like: "Exception calling application: No positional arguments allowed","grpc_status":2}". Check paramters name and type data.
- If you have see log: details = "failed to connect to all addresses". Check port is runing and port is called from client is one. 
- If gRPC server is deloyed in a server. If you can not connect, pls check public IP and port is ready for call from out network. 


## License


****

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [dill]: <https://github.com/joemccann/dillinger>
   [git-repo-url]: <https://github.com/joemccann/dillinger.git>
   [john gruber]: <http://daringfireball.net>
   [df1]: <http://daringfireball.net/projects/markdown/>
   [markdown-it]: <https://github.com/markdown-it/markdown-it>
   [Ace Editor]: <http://ace.ajax.org>
   [node.js]: <http://nodejs.org>
   [Twitter Bootstrap]: <http://twitter.github.com/bootstrap/>
   [jQuery]: <http://jquery.com>
   [@tjholowaychuk]: <http://twitter.com/tjholowaychuk>
   [express]: <http://expressjs.com>
   [AngularJS]: <http://angularjs.org>
   [Gulp]: <http://gulpjs.com>

   [PlDb]: <https://github.com/joemccann/dillinger/tree/master/plugins/dropbox/README.md>
   [PlGh]: <https://github.com/joemccann/dillinger/tree/master/plugins/github/README.md>
   [PlGd]: <https://github.com/joemccann/dillinger/tree/master/plugins/googledrive/README.md>
   [PlOd]: <https://github.com/joemccann/dillinger/tree/master/plugins/onedrive/README.md>
   [PlMe]: <https://github.com/joemccann/dillinger/tree/master/plugins/medium/README.md>
   [PlGa]: <https://github.com/RahulHP/dillinger/blob/master/plugins/googleanalytics/README.md>
