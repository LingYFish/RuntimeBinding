# -*- coding: utf-8 -*-

from mod.common.mod import Mod


@Mod.Binding(name="Binding", version="0.0.1")
class Binding(object):

    def __init__(self):
        pass

    @Mod.InitServer()
    def BindingServerInit(self):
        import mod.server.extraServerApi as serverApi
        print "[SUB] BaseBindingLoadServer"
        serverApi.RegisterSystem('Binding','BindingServerSystem','BindingScript.system.serverSystem.BindingServerSystem')

    @Mod.DestroyServer()
    def BindingServerDestroy(self):
        pass

    @Mod.InitClient()
    def BindingClientInit(self):
        import mod.client.extraClientApi as clientApi
        print "[SUB] BaseBindingLoadClient"
        clientApi.RegisterSystem('Binding','BindingClientSystem','BindingScript.system.clientSystem.BindingClientSystem')
        

    @Mod.DestroyClient()
    def BindingClientDestroy(self):
        pass
