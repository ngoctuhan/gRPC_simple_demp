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
        print(name)
        print(id_)
        if id_ / 2 == 0:
            print("True")
            return Person(name = name, id = id_, married = True)
        else:
            print("False")
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