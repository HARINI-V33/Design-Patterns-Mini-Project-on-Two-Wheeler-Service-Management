from abc import *
from datetime import datetime
import time
import pickle
import re
import threading
from test_pricecheck import TestVerifyPrice as tvp

class TwoWheelerServiceManagementSystemAdmin:

    # singleton pattern for this admin system

    s_instance=None

    def __new__(cls):

        if cls.s_instance==None:
            cls.s_instance=super().__new__(cls)
        return cls.s_instance

    def __init__(self):

        # regex check for username and password

        username=input("Enter the admin username:")
        while (not re.match("Bike24/7",username)):
            username=input("Your username is incorrect!\nEnter the correct username:")
        password=input("Enter admin password:")
        while not re.match("Bk@7",password):
            password=input("Your password is incorrect!\nEnter the correct password:")

        self.pricedict={"oil":500,"maintenance":300,"brake":400}
        self.shopname="H Two Wheeler Services"
        self.employeelist=[]
        self.bookingslist=[]

        # serialisation using pickle
        try:
                file1=open("bookings.pickle","rb")
                while(1):
                    try:
                        job=pickle.load(file1)
                        if job not in self.bookingslist:
                            self.bookingslist.append(job)
                    except:
                        break
                file1.close()

        except:
            pass

    def addjob(self,job):
        self.bookingslist.append(job)
        tvp().test_verify(self,job.service.stype,job.service.price)
        self.assignworks()

    # to invoke the alert (command pattern)
    
    def invokealert(self,cust):
        Alert(cust).givealert()

    def addemployee(self,emp):
        self.employeelist.append(emp)
    
    def assignworks(self):
        try:
            if len(self.bookingslist)%2==0:
                self.employeelist[-1].addwork(self.bookingslist[-1])
            else:
                self.employeelist[-2].addwork(self.bookingslist[-1])
        except:
            pass

    def instructtowork(self):
        for i in self.employeelist:
            t1=threading.Thread(target=i.startwork())
            t1.start()
            t1.join()
        print("At the end of the day!\n----------------------")
        for i in self.employeelist:
            i.refinework()

class Command(ABC):
    def __init__(self,cust):
        self.receiver=cust
    @abstractmethod
    def givealert(self):
        pass
class Alert(Command):
    def givealert(self):
        self.receiver.getalert()

class State(ABC):
    @property
    def context(self):
        return self._context
    @context.setter
    def context(self,con):
        self._context=con
    @abstractmethod
    def changestate(self):
        pass

class NotCompleted(State):
    def changestate(self):
        print("The state changes to not completed state.")

class Completed(State):
    def changestate(self):
        print("The service is completed.")

class Customer:
    def __init__(self):
        self.name=input("Enter your name:")
        self.phone=input("Enter your phone number:")
        self.detailcard=Jobcard(self)
    def getalert(self):
        print("{} your two wheeler got ready after the finished service".format(self.name))
    def viewinfo(self):
        print(self.detailcard)

class Jobcard:
    def __init__(self,cust):
        self.cust=cust
        self.vnum=input("Enter the vehicle number:")
        self.vmodel=input("Enter the vehicle model:")
        self.expdate=datetime.strptime(input("Enter the expected delivery date:"),"%d/%m/%Y")
        self.service=Service()
        self.state=NotCompleted()
        self.state.context=self
        file2=open("bookings.pickle","ab")
        pickle.dump(self,file2)
        file2.close()
        admin.addjob(self)
    def __str__(self):
        return "Name:"+self.cust.name+"\nPhone:"+self.cust.phone+"\nVehicle number:"+self.vnum+"\nVehicle model:"+self.vmodel+"\nExpected delivery date:"+self.expdate.strftime("%d/%m/%Y")+"\n"+str(self.service)
    def changestate(self):
        self.state=Completed()
        self.state.changestate()

class Service:
    def __init__(self):
        self.stype=input("Enter the type of service:")
        self.price=int(input("Enter the price rate:"))
    def __str__(self):
        return "Service type:"+self.stype+"\nPrice:"+str(self.price)

class Employee:
    def __init__(self,name,id):
        self.name=name
        self.id=id
        self.jobslist=JobworkIterable()
    def addwork(self,work):
        self.jobslist.append(work)
    def refinework(self):
        finished=[]
        for i in self.jobslist:
            print(i)
            answer=input(self.name+"!,Have you finished this service?")
            if answer=="yes":
                admin.invokealert(i.cust)
                finished.append(i)
                i.changestate()
            elif answer=="no":
                print("You have to finsh this work first!")
                break
        filename=open("bookings.pickle","wb")

        for i in finished:
            pickle.dump(i,filename)
        filename.close()

    def startwork(self):
        print("{} has started the work.\nI have to keep it idle for sometime.".format(self.name))
        time.sleep(2)
        print("{} has finished the service.".format(self.name))

def priordate(obj):
    return obj.expdate

class JobworkIterable:
    def __init__(self):
        self.jobslist=[]
    def append(self,job):
        self.jobslist.append(job)
    def __iter__(self):
        return JobworkIterator(self.jobslist)

class JobworkIterator:
    def __init__(self,lst):
        lst.sort(key=priordate)
        self.sortjoblist=lst
        self.index=0
    def __next__(self):
        if self.index==len(self.sortjoblist):
            raise StopIteration
        x=self.sortjoblist[self.index]
        self.index+=1
        return x


admin=TwoWheelerServiceManagementSystemAdmin()
e1=Employee("Ram",888)
e2=Employee("Krish",787)
admin.addemployee(e1)
admin.addemployee(e2)
c1=Customer()
c2=Customer()
admin.instructtowork()
fil=open("bookings.pickle","wb")
fil.close()