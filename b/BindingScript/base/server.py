import mod.server.extraServerApi as extraServerApi
lambda : "By:SliverX"
engineNameSpace = "Minecraft"
engineSystemName = "Engine"
serverSystem = extraServerApi.GetServerSystemCls()
compFactory = extraServerApi.GetEngineCompFactory()
levelId = extraServerApi.GetLevelId()
serverApi = extraServerApi

def funcListenEvent(func, namespace = engineNameSpace, systemName = engineSystemName, eventName = '', priority = 0):
    #type: (function,str,str,str,int) -> None
    _ts = type("TemporaryContainer",(object,),{})()
    setattr(_ts,func.__name__,func)
    serverSystem('Binding','______________').ListenForEvent(namespace, systemName, eventName, _ts, func, priority)

def funcUnListenEvent(func, namespace = engineNameSpace, systemName = engineSystemName, eventName = '', priority = 0):
    #type: (function,str,str,str,int) -> None
    _ts = type("TemporaryContainer",(object,),{})()
    setattr(_ts,func.__name__,func)
    serverSystem('Binding','______________').UnListenForEvent(namespace, systemName, eventName, _ts, func, priority)


class IServerSystem(serverSystem):

    def __init__(self, namespace, systemName):
        serverSystem.__init__(self,namespace, systemName)
        for method in dir(self):
            if hasattr(getattr(self,method),'event_list'):
                event_list = getattr(getattr(self,method),'event_list')
                for event in event_list:
                    _namespace = event[0]
                    _systemName = event[1]
                    eventName = event[2]
                    priority = event[3]
                    self.addListenEvent(func=getattr(self,method),systemName=_systemName,namespace=_namespace,eventName=eventName,priority=priority)

    @staticmethod
    def ListenEvent(namespace = engineNameSpace, systemName = engineSystemName, eventName = '',priority=0):
        def warp(func):
            if hasattr(func,'event_list'):
                func.event_list.append((namespace,systemName,eventName if eventName != '' else func.__name__,priority))
            else:
                func.event_list = [(namespace,systemName,eventName if eventName != '' else func.__name__,priority),]
            return func
        return warp
    
    def GetSystem(self):
        serverName = self.__name__
        return serverApi.GetSystem('Binding',serverName)

    def addListenEvent(self, func, namespace = engineNameSpace, systemName = engineSystemName, eventName = '', priority = 0):
        #type: (function,str,str,str,int) -> None
        self.ListenForEvent(namespace, systemName, eventName, self, func, priority)

    def addListenEventUi(self, screen, func, namespace = engineNameSpace, systemName = engineSystemName, eventName = '', priority = 0):
        #type: (object,function,str,str,str,int) -> None
        self.ListenForEvent(namespace, systemName, eventName, screen, func, priority)

    def removeListenEvent(self, func, namespace = engineNameSpace, systemName = engineSystemName, eventName = '', priority = 0):
        #type: (function,str,str,str,int) -> None
        self.UnListenForEvent(namespace, systemName, eventName, self, func, priority)

    def removeListenEventUi(self, screen, func, namespace = engineNameSpace, systemName = engineSystemName, eventName = '', priority = 0):
        #type: (object,function,str,str,str,int) -> None
        self.UnListenForEvent(namespace, systemName, eventName, screen, func, priority)
    
    def clientCaller(self, funcName, args):
        #type: (str,dict) -> None
        self.NotifyToClient(funcName, args)

    def clientCaller(self, clientId, funcName, args):
        #type: (str,str,dict) -> None
        self.NotifyToClient(clientId, funcName, args)
    
    def callAllclient(self, funcName, args):
        #type: (str,dict) -> None
        self.NotifyToMultiClients(extraServerApi.GetPlayerList(),funcName, args)