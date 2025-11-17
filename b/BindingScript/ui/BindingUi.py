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
        is_method = hasattr(func, "im_func")
        real_func = func.im_func if is_method else func
        name_attr = "func_name" if is_method else "__name__"

        old_flag = hasattr(real_func, "old_func_name")
        in_bind = func in self.vaule_bind

        if in_bind or old_flag:
            self.unBinding(func)
            if func in self.vaule_bind:
                self.vaule_bind.remove(func)
        old_name = getattr(real_func, name_attr)
        setattr(real_func, "old_func_name", old_name)
        new_name = "{}_patch_{}".format(uid, old_name)
        setattr(real_func, name_attr, new_name)
        setattr(self, new_name, func)
        if hasattr(func, "collection_name"):
            self._process_collection(func, self.screen_name)
        if hasattr(func, "binding_flags"):
            self._process_default(func, self.screen_name)
        if func not in self.vaule_bind:
            self.vaule_bind.append(func)

    def unBinding(self, func):
        is_method = hasattr(func, "im_func")
        real_func = func.im_func if is_method else func
        name_attr = "func_name" if is_method else "__name__"
        name = getattr(real_func, name_attr, None)
        if not name:
            return
        if hasattr(func, "collection_name"):
            self._process_collection_unregister(func, self.screen_name)
        if hasattr(func, "binding_flags"):
            self._process_default_unregister(func, self.screen_name)
        if hasattr(self, name):
            delattr(self, name)
        if hasattr(real_func, "old_func_name"):
            setattr(real_func, name_attr, real_func.old_func_name)
            delattr(real_func, "old_func_name")
        if func in self.vaule_bind:
            self.vaule_bind.remove(func)

    def process_unbinding(self, screen_name):
        for key in dir(self):
            func = getattr(self, key)
            is_method = hasattr(func, "im_func")
            real_func = func.im_func if is_method else func
            name_attr = "func_name" if is_method else "__name__"
            if hasattr(real_func, "old_func_name"):
                setattr(real_func, name_attr, real_func.old_func_name)
                delattr(real_func, "old_func_name")
            if hasattr(func, "collection_name"):
                self._process_collection_unregister(func, screen_name)
                continue
            if hasattr(func, "binding_flags"):
                self._process_default_unregister(func, screen_name)
                continue

    def process_binding(self, screen_name):
        for key in dir(self):
            func = getattr(self, key)
            if func not in self.vaule_bind:
                self.vaule_bind.append(func)
            if hasattr(func, "collection_name"):
                self._process_collection(func, screen_name)
                continue
            if hasattr(func, "binding_flags"):
                self._process_default(func, screen_name)
                continue