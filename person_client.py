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
    