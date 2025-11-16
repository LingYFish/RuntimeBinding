import mod.client.extraClientApi as clientApi
from mod.client.ui.screenNode import ScreenNode
import traceback, uuid
compFactory = clientApi.GetEngineCompFactory()
levelId = clientApi.GetLevelId()
gameComp = compFactory.CreateGame(levelId)

class uiNode(ScreenNode):

    def __init__(self, namespace, name, param=None):
        super(uiNode, self).__init__(namespace, name, param)
        self.bind_data =  {}

    def addBinding(self, func):
        uid = uuid.uuid4().hex
        self.bind_data[func.im_func.func_name] = '{}_patch_{}'.format(uid, func.im_func.func_name)
        func.im_func.func_name = '{}_patch_{}'.format(uid, func.im_func.func_name)
        setattr(self, func.im_func.func_name, func)
        if hasattr(func, 'collection_name'):
            self._process_collection(func, self.screen_name)
        if hasattr(func, 'binding_flags'):
            self._process_default(func, self.screen_name)

    def unBinding(self, func):
        name = self.bind_data.get(func.im_func.func_name)
        if name:
            if hasattr(func, 'collection_name'):
                self._process_collection_unregister(func, self.screen_name)
            if hasattr(func, 'binding_flags'):
                self._process_default_unregister(func, self.screen_name)
            if hasattr(self, name):
                delattr(self, name)