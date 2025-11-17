from ..base.client import *
from ..ui.BindingUi import Binding
from collections import OrderedDict

class BindingClientSystem(IClientSystem):

    def __init__(self, namespace, systemName):
        super(BindingClientSystem, self).__init__(namespace, systemName)
        self.data =  {}

    @IClientSystem.ListenEvent('Binding','BindingServerSystem','open_Binding')
    def OpenBinding(self, args):
        Binding.CreateScreen()