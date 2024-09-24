# -*- coding: utf-8 -*-
# import pickle
#
#
# class Person:
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
#
#     def __getstate__(self):
#         # 只返回需要序列化的状态
#         return self.name
#
#     def __setstate__(self, state):
#         # 从序列化状态恢复对象
#         self.name = state
#         self.age = 1  # 设置age的默认值
#
#
# # 创建一个Person对象并序列化
# p = Person("Alice", 30)
# serialized_p = pickle.dumps(p)
#
# # 反序列化并打印结果
# p_restored = pickle.loads(serialized_p)
# print(p_restored.name)  # 输出: Alice
# print(p_restored.age)  # 输出: 1，因为我们在__setstate__中设置了默认值


import pickle


def create_person(name):
    return Person(name, 0)  # 创建一个新的Person对象，age默认为0


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __reduce__(self):
        # 返回一个元组，包含可调用对象和该对象需要的参数
        return create_person, (self.name,)

    # 创建一个Person对象并序列化（使用__reduce__）


p = Person("Bob", 25)
serialized_p = pickle.dumps(p)

# 反序列化并打印结果
p_restored = pickle.loads(serialized_p)
print(p_restored.name)  # 输出: Bob
print(p_restored.age)  # 输出: 0，因为create_person函数设置了age的默认值
