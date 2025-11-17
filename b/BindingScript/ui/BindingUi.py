import mod.client.extraClientApi as clientApi
import traceback, uuid, copy
from ..base.ui import UiSystemNode
from controls.binder import Binder
compFactory = clientApi.GetEngineCompFactory()
levelId = clientApi.GetLevelId()
gameComp = compFactory.CreateGame(levelId)

@UiSystemNode.registerScreenInfo(
    'push',
    'binding',
    'binding',
    'binding'
)
class Binding(UiSystemNode):

    def __init__(self, namespace, name, param=None):
        super(Binding, self).__init__(namespace, name, param)
        self.vaule_bind = []

        Binder.set_bind_collection_string('binding_condition_test','#title_name',self.title_has_collection)
        Binder.set_bind_string('#l_n',self.title_no_collection)

    def title_no_collection(self):
        return "title_no_collection"
    
    def title_has_collection(self,index):
        return "title_has_collection index:{}".format(index)

    @Binder.binding(Binder.BF_ButtonClick, '#screen.back')
    def back(self, args):
        self.Destroy()
        clientApi.PopScreen()

    def Create(self):
        super(Binding, self).Create()
        self.addBinding(self.title_has_collection)
        self.addBinding(self.title_no_collection)
        self.UpdateScreen(True)

    def addBinding(self, func):
        uid = uuid.uuid4().hex
        if func in self.vaule_bind or hasattr(func.im_func,'old_func_name'): #避免复滥用重复绑定
            """避免开头先绑定了 导致复绑定问题 我们这边处理一次取消绑定 基于网易原本实现"""
            if hasattr(func, 'collection_name'):
                self._process_collection_unregister(func, self.screen_name)
            if hasattr(func, 'binding_flags'):
                self._process_default_unregister(func, self.screen_name)
            if func in self.vaule_bind:
                self.vaule_bind.remove(func)
        func.im_func.old_func_name = func.im_func.func_name
        func.im_func.func_name = '{}_patch_{}'.format(uid, func.im_func_name)
        setattr(self, func.im_func.func_name, func)
        if hasattr(func, 'collection_name'):
            self._process_collection(func, self.screen_name)
        if hasattr(func, 'binding_flags'):
            self._process_default(func, self.screen_name)

    def unBinding(self, func):
        name = func.im_func.func_name
        if name:
            if hasattr(func, 'collection_name'):
                self._process_collection_unregister(func, self.screen_name)
            if hasattr(func, 'binding_flags'):
                self._process_default_unregister(func, self.screen_name)
            if hasattr(self, name):
                delattr(self, name)
        if hasattr(func.im_func,'old_func_name'):
            func.im_func.func_name = func.im_func.old_func_name

    def process_unbinding(self, screen_name):
        """处理 取消绑定"""
        for key in dir(self):
            func = getattr(self, key)
            if hasattr(func.im_func,'old_func_name'):
                func.im_func.func_name = func.im_func.old_func_name #销毁后还原
            if hasattr(func, 'collection_name'):
                self._process_collection_unregister(func, screen_name)
                continue
            if hasattr(func, 'binding_flags'):
                self._process_default_unregister(func, screen_name)
                continue

    def process_binding(self, screen_name):
        """处理 绑定"""
        for key in dir(self):
            func = getattr(self, key)
            self.vaule_bind.append(func)
            if hasattr(func, 'collection_name'):
                self._process_collection(func, screen_name)
                continue
            if hasattr(func, 'binding_flags'):
                self._process_default(func, screen_name)
                continue