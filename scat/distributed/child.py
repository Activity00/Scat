# coding: utf-8

"""
@author: 武明辉 
@time: 2018/1/27 13:18
"""


class Child:
    """
    子节点对象
    """
    def __init__(self, id, name, transport=None):
        self.id = id
        self.name = name
        self.transport = transport

    def callback_child(self, *args, **kwargs):
        """
        回调子节点接口
        :return:
        """
        self.transport.call_remote(*args, **kwargs)


class ChildManager:
    """子节点管理器"""
    def __init__(self):
        self._childs = {}

    def get_child_by_id(self, child_id):
        """根据节点的ID获取节点实例"""
        return self._childs.get(child_id)

    def get_child_by_name(self, child_name):
        """根据节点的名称获取节点实例"""
        for key, child in self._childs.items():
            if child.getName() == child_name:
                return self._childs[key]
        return None

    def add_child(self, child):
        """添加一个child节点
        @param child: Child object
        """
        key = child.id
        if self._childs.get(key):
            raise "child node %s exists" % key
        self._childs[key] = child

    def drop_child(self, child):
        """删除一个child 节点
        @param child: Child Object 
        """
        key = child.id
        try:
            del self._childs[key]
        except Exception as e:
            print(str(e))

    def drop_child_by_id(self, child_id):
        """ 删除一个child 节点
        @param childId: Child ID 
        """
        try:
            del self._childs[child_id]
        except Exception as e:
            print(str(e))

    def call_child(self, child_id, *args, **kw):
        """调用子节点的接口
        """
        child = self._childs.get(child_id, None)
        if not child:
            print("child %s doesn't exists" % child_id)
            return
        return child.callbackChild(*args, **kw)

    def call_child_by_name(self, child_name, *args, **kw):
        """调用子节点的接口
        """
        child = self.get_child_by_name(child_name)
        if not child:
            print("child %s doesn't exists" % child_name)
            return
        return child.callbackChild(*args, **kw)

    def generate_child_id(self):
        return max(self._childs) + 1 if self._childs else 0

    def get_child_by_session_id(self, session_id):
        """根据sessionID获取child节点信息"""
        for child in self._childs.values():
            if child.transport.broker.transport.sessionno == session_id:
                return child
        return None

if __name__ == '__main__':
    pass
