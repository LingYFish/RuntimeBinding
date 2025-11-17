from client import *

class UiSystemNode(ScreenNode):
    createType = 'push'
    namespace = None
    name = None
    uiName = ''
    param = {}
    listenEvents = [] #type: list[tuple[str,str,str,int,function]]

    def __init__(self, namespace, name, param = {}):
        ScreenNode.__init__(self, namespace, name, param)
        self.hoverText = ''

    def uiListenEvent(self, func, namespace = engineNameSpace, systemName = engineSystemName, eventName = '', priority = 0):
        #type: (function,str,str,str,int) -> None
        clientSystem('Binding','______________').ListenForEvent(namespace, systemName, eventName, self, func, priority)

    def uiUnListenEvent(self, func, namespace = engineNameSpace, systemName = engineSystemName, eventName = '', priority = 0):
        #type: (function,str,str,str,int) -> None
        clientSystem('Binding','______________').UnListenForEvent(namespace, systemName, eventName, self, func, priority)

    @staticmethod
    def registerScreenInfo(createType='push',namespace=None,name=None,uiName=''):
        #type: (str,str,str,str) -> UiSystemNode
        def _setInfo(cls):
            #type: (object|UiSystemNode) -> UiSystemNode
            cls.createType = createType
            cls.namespace = namespace
            cls.name = name
            cls.uiName = uiName
            def register(args={}):
                ScreenNodeClsPath = "{}.{}".format(cls.__module__,cls.__name__)
                clientApi.RegisterUI('Binding', cls.uiName, ScreenNodeClsPath, "{}.{}".format(cls.namespace,cls.name))
            funcListenEvent(register,eventName='UiInitFinished')
            return cls
        return _setInfo
    
    @classmethod
    def removeUi(cls):
        UiNode = cls.getUi() # type: UiSystemNode
        if UiNode:
            UiNode.SetRemove()

    @classmethod
    def getUi(cls, uiName=None):
        # type: (object|UiSystemNode) -> UiSystemNode | None
        if isinstance(uiName,str):
            return clientApi.GetUI('Binding', uiName)
        elif uiName == None:
            return cls.getUi(cls)
        elif issubclass(uiName,UiSystemNode):
            return clientApi.GetUI('Binding', uiName.name)
    
    @staticmethod
    def ListenEvent(namespace = engineNameSpace, systemName = engineSystemName, eventName = '',priority=0):
        def warp(func):
            if hasattr(func,'event_list'):
                func.event_list.append((namespace,systemName,eventName if eventName != '' else func.__name__,priority))
            else:
                func.event_list = [(namespace,systemName,eventName if eventName != '' else func.__name__,priority),]
            return func
        return warp

    @staticmethod
    def onButtonClick(path):
        def wrap(func):
            return func
        return wrap
    
    @classmethod
    def CreateScreen(cls,params=None):
        uiNode = cls.getUi(cls)
        if cls.namespace is None or cls.name is None:
            raise TypeError("哈基米那没撸多")
        if uiNode:
            return uiNode
        if cls.createType == 'push':
            return clientApi.PushScreen('Binding', cls.uiName, params)
        else:
            return clientApi.CreateUI('Binding', cls.uiName, params)

    def OnActive(self):
        pass

    def OnDeactive(self):
        pass

    def Create(self):
        """ 自动监听事件监听 """
        for method in dir(self):
            if hasattr(getattr(self,method),'event_list'):
                event_list = getattr(getattr(self,method),'event_list')
                for event in event_list:
                    _namespace = event[0]
                    _systemName = event[1]
                    _eventName = event[2]
                    _priority = event[3]
                    self.listenEvents.append(
                        (_namespace,
                        _systemName,
                        _eventName,
                        _priority,
                        getattr(self,method))
                    )
                    self.uiListenEvent(func=getattr(self,method),systemName=_systemName,namespace=_namespace,eventName=_eventName,priority=_priority)

    def Destroy(self):
        """ 自动摧毁所有事件监听 """
        for event in self.listenEvents:
            _namespace = event[0]
            _systemName = event[1]
            _eventName = event[2]
            _priority = event[3]
            _func = event[4]
            self.uiUnListenEvent(_func,_namespace,_systemName,_eventName,_priority)
    
    def Update(self):
        pass

    def registerToggleButton(self):
        pass