class Observer:
    def __init__(self, observable):
        observable.register_observer(self)

    def notify(self, message):
        pass


class Observable:
    def __init__(self):
        self.__observers = []
        self.__data = []

    def register_observer(self, observer):
        self.__observers.append(observer)

    def notify_observers(self):
        self.__data.clear()
        for observer in self.__observers:
            self.__data.append(observer.notify())
        print (self.__data)


    # def notify_observers(self, message):
    #     for observer in self.__observers:
    #         #rückgabe werte füllen in data[] liste
    #         #self.dataList[i] =
    #         observer.notify(self, message)
    #         pass
    #     #return self.dataList
