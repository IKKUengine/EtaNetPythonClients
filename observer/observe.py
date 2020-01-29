import parameter

class Observer:
    def __init__(self, observable):
        observable.register_observer(self)

    def notifyData(self, data):
        pass
    
    def notifyHeader(self, header):
        pass
    
    def notifyControl(self, parameter):
        pass

class Observable:
    def __init__(self):
        self.__observers = []
        self.__data = []
        self.__header = []
        self.__parameter = ""
    
    def getDataList(self):
        message = ','.join(self.__data)
        return message
    
    def getHeaderList(self):
        message = ','.join(self.__header)
        return message
    
    def getControlParameter(self):
        message = ','.join(self.__parameter)
        return message
    
    def setControlParameter(self, message):
        self.__parameter = message

    def register_observer(self, observer):
        self.__observers.append(observer)

    def notify_observersMonitoring(self):
        self.__data.clear()
        self.__header.clear()
        for observer in self.__observers:
            self.__data.append(observer.notifyData())
            self.__header.append(observer.notifyHeader())            

