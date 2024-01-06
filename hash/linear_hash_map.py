from random import randint
import uuid
from graphviz import Digraph

def color(value):
    digit = list(map(str, range(10))) + list("ABCDEF")
    if isinstance(value, tuple):
        string = '#'
        for i in value:
            a1 = i // 16
            a2 = i % 16
            string += digit[a1] + digit[a2]
        return string
    elif isinstance(value, str):
        a1 = digit.index(value[1]) * 16 + digit.index(value[2])
        a2 = digit.index(value[3]) * 16 + digit.index(value[4])
        a3 = digit.index(value[5]) * 16 + digit.index(value[6])
        return (a1, a2, a3)


import colorsys
import random


def get_n_hls_colors(num):
    hls_colors = []
    i = 0
    step = 360.0 / num
    while i < 360:
        h = i
        s = 90 + random.random() * 10
        l = 50 + random.random() * 10
        _hlsc = [h / 360.0, l / 100.0, s / 100.0]
        hls_colors.append(_hlsc)
        i += step

    return hls_colors


def ncolors(num):
    rgb_colors = []
    if num < 1:
        return rgb_colors
    hls_colors = get_n_hls_colors(num)
    for hlsc in hls_colors:
        _r, _g, _b = colorsys.hls_to_rgb(hlsc[0], hlsc[1], hlsc[2])
        r, g, b = [int(x * 255.0) for x in (_r, _g, _b)]
        rgb_colors.append([r, g, b])

    return rgb_colors


#定义一个键值对
class Pair:
    __slots__ = ("key", "value")

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.id=str(uuid.uuid4())

#线性哈希表
class Linear_Hash:
    def __init__(self) -> None:
        self.bucket_capacity = 4 #桶的容量
        self.overpoint = 0 #分裂点
        self.init_size = 2 #哈希表初始大小
        self.size = 2 #哈希表大小
        self.level = 1 #分裂轮数
        self.buckets = [{ } for _ in range(self.init_size)]  # 桶数组
        self.id=str(uuid.uuid4())
    def hash_fun(self, key, f1):
        return key % (2 * 2**(f1 - 1))
    
    #查询函数	
    def Search(self, key):
        index = self.hash_fun(key, self.level)
        idx=0
        if index < self.overpoint:
            index = self.hash_fun(key, self.level + 1)
        if self.buckets[index].get(key) == None:
            print(str(key)+"对应键值不存在")  
        else:
            print(str(key)+"对应键值在桶"+str(index)+"中") 
        return self.buckets[index].get(key)
    
    def Insert(self, key, value):
        def SplitHash():
            old_bucket = self.buckets[self.overpoint]
            new_bucket = {}
            for key in list(old_bucket.keys()):
                index = self.hash_fun(key, self.level + 1)
                if index >= self.size:
                    value = old_bucket[key]
                    old_bucket.pop(key)
                    new_bucket[key]=value
            
            self.buckets.append(new_bucket)
            self.size += 1
            self.overpoint += 1

            if self.overpoint >= self.init_size:
                self.level += 1
                self.init_size *= 2
                self.overpoint = 0

        index = self.hash_fun(key, self.level)
        if index < self.overpoint:
            index = self.hash_fun(key, self.level + 1)
        bucket = self.buckets[index]
        if len(bucket) < self.bucket_capacity:
            bucket[key] = value
        else:
            bucket[key] = value
            SplitHash()

    def Delete(self, key):
        def MergeHash():
            if self.overpoint == 0 :
                self.level -= 1
                self.overpoint = self.init_size / 2 
                self.init_size /= 2

            self.overpoint -= 1
            self.size -= 1 
            old_bucket = self.buckets[self.size]
            self.buckets = self.buckets[:-1]
            for key in list(old_bucket.keys()):
                index = self.hash_fun(key, self.level)
                value = old_bucket[key]
                self.buckets[index][key] = value

        if self.Search(key) != None:
            index = self.hash_fun(key, self.level)
            if index < self.overpoint:
                index = self.hash_fun(key, self.level + 1)
            bucket = self.buckets[index]
            bucket.pop(key)
            print("已从桶" + str(index) + "中删除键值" + str(key))
            if len(bucket) == 0 and self.size >4:
                MergeHash()
                print("一个桶中元素删除至零,触发合并操作")

        # 打印哈希表
    def print(self):
        for bucket in self.buckets:
            res = []
            for key, value in bucket.items():
                res.append(str(key) + " -> " + str(value))
            print(res)
        #graphviz可视化
    def visualize(self):
        dot = Digraph(comment='Linear Hash',node_attr={'shape': 'record', 'height': '.1'})
        dot.attr('node', shape='box')
        #dot.node('bucket', style='filled', fillcolor='#40e0d0')

        color_1 = list(map(lambda x: color(tuple(x)), ncolors(100)))

        for i in range(self.size):

            dot.node("node_"+str(i),str(i))
            dot.node('bucket'+str(i), style='filled', fillcolor=color_1[i+random.randint(0,90)])

        for i in range(self.size):
            print(self.buckets[i])

            for key, value in self.buckets[i].items():


                dot.edge("node_"+str(i), 'bucket'+str(i), label=str(key) + " -> " + str(value))

        dot.view()




def test():
    L = Linear_Hash()

    for i in range(1,30,1):
        k = randint(1, 100)
        L.Insert(i,i**2)
    L.print()
    L.visualize()
'''
    for i in range(20):
        k = randint(1, 100)
        L.Search(k)
    for i in range(30):
        k = randint(1, 100)
        L.Delete(i)
    
    
    L.print()

    for i in range(1):
        k = randint(1, 300)
        L.Insert(i, i**2)
    L.print()
    for i in range(100):
        k = randint(1, 80)
        L.Insert(i, i**2)
    L.print()
'''
#对输出结果进行可视化





if __name__ == "__main__":
    test()

