from ..base.server import *

class BindingServerSystem(IServerSystem):

    def __init__(self, namespace, systemName):
        super(BindingServerSystem, self).__init__(namespace, systemName)

    @IServerSystem.ListenEvent(eventName='ServerChatEvent')
    def ServerChatEvent(self, args):
        playerId = args['playerId']
        message = args['message']
        if message == 'open':
            self.clientCaller(playerId,'open_Binding',{})

    @IServerSystem.ListenEvent(eventName='ServerItemTryUseEvent')
    def ServerItemTryUseEvent(self, args):
        playerId = args['playerId']
        itemDict = args['itemDict'] or {'newItemName':'114514'}
        if itemDict['newItemName'] == 'minecraft:netherite_sword':
            self.clientCaller(playerId,'open_Binding',{})
