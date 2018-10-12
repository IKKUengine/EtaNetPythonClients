import error

class Observer:
    def __init__(self, observable):
        observable.register_observer(self)

    def notify(self, message):
        pass

class Observable:
    def __init__(self):
        self.__observers = []
        self.__data = []
    
    def getDataList(self):
        message = self.__data
        return message

    def register_observer(self, observer):
        self.__observers.append(observer)

    def notify_observers(self):
        self.__data.clear()
        for observer in self.__observers:
            self.__data.append(observer.notify())
        self.sendAllData()

    def sendAllData(self):
        pass