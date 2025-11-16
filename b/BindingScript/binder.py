class Binder(object):
    ButtonFilter = 268435456
    BF_ButtonClickUp = 0 | ButtonFilter
    BF_ButtonClickDown = 1 | ButtonFilter
    BF_ButtonClick = 2 | ButtonFilter
    BF_ButtonClickCancel = 3
    BF_InteractButtonClick = 4

    BindFilter = 16777216
    BF_BindBool = 5 | BindFilter
    BF_BindInt = 6 | BindFilter
    BF_BindFloat = 7 | BindFilter
    BF_BindString = 8 | BindFilter
    BF_BindGridSize = 9 | BindFilter
    BF_BindColor = 10 | BindFilter

    EditFilter = 1048576
    BF_EditChanged = 11 | EditFilter
    BF_EditFinished = 12 | EditFilter

    ToggleFilter = 65536
    BF_ToggleChanged = 13 | ToggleFilter

    SliderFilter = 4096
    BF_SliderChanged = 1 | SliderFilter
    BF_SliderFinished = 16 | SliderFilter

    bindings = {}
    collections = {}

    @staticmethod
    def _real_func(func):
        #type: (function) -> function
        """

        :param func: 函数对象
        :rtype: function
        """
        return getattr(func, "im_func", func)

    @staticmethod
    def _reg(name, func, flag):
        #type: (str, function, int) -> None
        """
        注册单个绑定函数，根据 flag 设置函数属性

        :param name: 绑定名称
        :param func: 回调函数
        :param flag: 绑定标志
        :rtype: None
        """
        func_obj = Binder._real_func(func)
        func_obj.binding_flags = flag
        func_obj.binding_name = name
        Binder.bindings[name] = func_obj

    @staticmethod
    def _reg_col(collection, name, func, flag):
        #type: (str, str, function, int) -> None
        """
        注册集合绑定函数，根据 flag 设置函数属性

        :param collection: 集合名称
        :param name: 绑定名称
        :param func: 回调函数
        :param flag: 绑定标志
        :rtype: None
        """
        func_obj = Binder._real_func(func)
        func_obj.binding_flags = flag
        func_obj.binding_name = name
        func_obj.collection_name = collection
        if collection not in Binder.collections:
            Binder.collections[collection] = []
        Binder.collections[collection].append(func_obj)

    @staticmethod
    def binding(bind_flag, binding_name=None):
        #type: (int, str) -> function
        """
        创建单个绑定装饰器

        :param bind_flag: 绑定标志
        :param binding_name: 绑定名称
        :rtype: function
        """
        def _binding(func):
            func.binding_flags = bind_flag
            func.binding_name = binding_name
            return func
        return _binding

    @staticmethod
    def binding_collection(bind_flag, collection_name, binding_name=None):
        #type: (int, str, str) -> function
        """
        创建集合绑定装饰器

        :param bind_flag: 绑定标志
        :param collection_name: 集合名称
        :param binding_name: 绑定名称
        :rtype: function
        """
        def _binding(func):
            func.binding_flags = bind_flag
            func.collection_name = collection_name
            func.binding_name = binding_name
            return func
        return _binding

    @staticmethod
    def set_binding_flags(func, flags):
        #type: (function, int) -> None
        """
        设置绑定标志

        :param func: 函数对象
        :param flags: 绑定标志
        :rtype: None
        """
        func.binding_flags = flags

    @staticmethod
    def set_binding_name(func, name):
        #type: (function, str) -> None
        """
        设置绑定名称

        :param func: 函数对象
        :param name: 绑定名称
        :rtype: None
        """
        func.binding_name = name

    @staticmethod
    def set_binding_collection(func, collection):
        #type: (function, str) -> None
        """
        设置集合绑定名称

        :param func: 函数对象
        :param collection: 集合名称
        :rtype: None
        """
        func.collection_name = collection

    @staticmethod
    def bind_bool(name):
        #type: (str) -> function
        """
        装饰器: bool 绑定

        :param name: 绑定名称
        :rtype: function
        """
        return Binder.binding(Binder.BF_BindBool, name)

    @staticmethod
    def bind_int(name):
        #type: (str) -> function
        """
        装饰器: int 绑定

        :param name: 绑定名称
        :rtype: function
        """
        return Binder.binding(Binder.BF_BindInt, name)

    @staticmethod
    def bind_float(name):
        #type: (str) -> function
        """
        装饰器: float 绑定

        :param name: 绑定名称
        :rtype: function
        """
        return Binder.binding(Binder.BF_BindFloat, name)

    @staticmethod
    def bind_string(name):
        #type: (str) -> function
        """
        装饰器: string 绑定

        :param name: 绑定名称
        :rtype: function
        """
        return Binder.binding(Binder.BF_BindString, name)

    @staticmethod
    def bind_grid_size(name):
        #type: (str) -> function
        """
        装饰器: grid size 绑定

        :param name: 绑定名称
        :rtype: function
        """
        return Binder.binding(Binder.BF_BindGridSize, name)

    @staticmethod
    def bind_color(name):
        #type: (str) -> function
        """
        装饰器: color 绑定

        :param name: 绑定名称
        :rtype: function
        """
        return Binder.binding(Binder.BF_BindColor, name)

    @staticmethod
    def bind_collection_bool(collection, name):
        #type: (str, str) -> function
        """
        装饰器: bool 集合绑定

        :param collection: 集合名称
        :param name: 绑定名称
        :rtype: function
        """
        return Binder.binding_collection(Binder.BF_BindBool, collection, name)

    @staticmethod
    def bind_collection_int(collection, name):
        #type: (str, str) -> function
        """
        装饰器: int 集合绑定

        :param collection: 集合名称
        :param name: 绑定名称
        :rtype: function
        """
        return Binder.binding_collection(Binder.BF_BindInt, collection, name)

    @staticmethod
    def bind_collection_float(collection, name):
        #type: (str, str) -> function
        """
        装饰器: float 集合绑定

        :param collection: 集合名称
        :param name: 绑定名称
        :rtype: function
        """
        return Binder.binding_collection(Binder.BF_BindFloat, collection, name)

    @staticmethod
    def bind_collection_string(collection, name):
        #type: (str, str) -> function
        """
        装饰器: string 集合绑定

        :param collection: 集合名称
        :param name: 绑定名称
        :rtype: function
        """
        return Binder.binding_collection(Binder.BF_BindString, collection, name)

    @staticmethod
    def bind_collection_grid_size(collection, name):
        #type: (str, str) -> function
        """
        装饰器: grid size 集合绑定

        :param collection: 集合名称
        :param name: 绑定名称
        :rtype: function
        """
        return Binder.binding_collection(Binder.BF_BindGridSize, collection, name)

    @staticmethod
    def bind_collection_color(collection, name):
        #type: (str, str) -> function
        """
        装饰器: color 集合绑定

        :param collection: 集合名称
        :param name: 绑定名称
        :rtype: function
        """
        return Binder.binding_collection(Binder.BF_BindColor, collection, name)

    @staticmethod
    def set_bind_bool(name, func):
        #type: (str, function) -> None
        """
        动态注册 bool 绑定

        :param name: 绑定名称
        :param func: 回调函数
        :rtype: None
        """
        Binder._reg(name, func, Binder.BF_BindBool)

    @staticmethod
    def set_bind_int(name, func):
        #type: (str, function) -> None
        """
        动态注册 int 绑定

        :param name: 绑定名称
        :param func: 回调函数
        :rtype: None
        """
        Binder._reg(name, func, Binder.BF_BindInt)

    @staticmethod
    def set_bind_float(name, func):
        #type: (str, function) -> None
        """
        动态注册 float 绑定

        :param name: 绑定名称
        :param func: 回调函数
        :rtype: None
        """
        Binder._reg(name, func, Binder.BF_BindFloat)

    @staticmethod
    def set_bind_string(name, func):
        #type: (str, function) -> None
        """
        动态注册 string 绑定

        :param name: 绑定名称
        :param func: 回调函数
        :rtype: None
        """
        Binder._reg(name, func, Binder.BF_BindString)

    @staticmethod
    def set_bind_grid_size(name, func):
        #type: (str, function) -> None
        """
        动态注册 grid size 绑定

        :param name: 绑定名称
        :param func: 回调函数
        :rtype: None
        """
        Binder._reg(name, func, Binder.BF_BindGridSize)

    @staticmethod
    def set_bind_color(name, func):
        #type: (str, function) -> None
        """
        动态注册 color 绑定

        :param name: 绑定名称
        :param func: 回调函数
        :rtype: None
        """
        Binder._reg(name, func, Binder.BF_BindColor)

    @staticmethod
    def set_bind_collection_bool(collection, name, func):
        #type: (str, str, function) -> None
        """
        动态注册 bool 集合绑定

        :param collection: 集合名称
        :param name: 绑定名称
        :param func: 回调函数
        :rtype: None
        """
        Binder._reg_col(collection, name, func, Binder.BF_BindBool)

    @staticmethod
    def set_bind_collection_int(collection, name, func):
        #type: (str, str, function) -> None
        """
        动态注册 int 集合绑定

        :param collection: 集合名称
        :param name: 绑定名称
        :param func: 回调函数
        :rtype: None
        """
        Binder._reg_col(collection, name, func, Binder.BF_BindInt)

    @staticmethod
    def set_bind_collection_float(collection, name, func):
        #type: (str, str, function) -> None
        """
        动态注册 float 集合绑定

        :param collection: 集合名称
        :param name: 绑定名称
        :param func: 回调函数
        :rtype: None
        """
        Binder._reg_col(collection, name, func, Binder.BF_BindFloat)

    @staticmethod
    def set_bind_collection_string(collection, name, func):
        #type: (str, str, function) -> None
        """
        动态注册 string 集合绑定

        :param collection: 集合名称
        :param name: 绑定名称
        :param func: 回调函数
        :rtype: None
        """
        Binder._reg_col(collection, name, func, Binder.BF_BindString)

    @staticmethod
    def set_bind_collection_grid_size(collection, name, func):
        #type: (str, str, function) -> None
        """
        动态注册 grid size 集合绑定

        :param collection: 集合名称
        :param name: 绑定名称
        :param func: 回调函数
        :rtype: None
        """
        Binder._reg_col(collection, name, func, Binder.BF_BindGridSize)

    @staticmethod
    def set_bind_collection_color(collection, name, func):
        #type: (str, str, function) -> None
        """
        动态注册 color 集合绑定

        :param collection: 集合名称
        :param name: 绑定名称
        :param func: 回调函数
        :rtype: None
        """
        Binder._reg_col(collection, name, func, Binder.BF_BindColor)
