from typing import List,Iterable
class Elem(object):
    def __init__(self,Key:int,Val:object,NextNode):
        self.key=Key
        self.value=Val # value指向记录的行地址
        self.nextNode=NextNode # 指向下一个节点
    def __str__(self):
        print(self.key)
        if self.nextNode is None:
            next='None'
        else:
            next = str(self.nextNode.key)
        return "{key:"+str(self.key)+",value:"+self.value.__str__()+",nextNode:'"+next+"'}"
class Node(object):
    def __init__(self, elems: List[Elem]):
        self.elems = elems
        self.nextLeaf=None # 只有叶子节点指向下一个兄弟节点
    def __getitem__(self, item):
        return self.elems[item]
    def __str__(self):
        res="["
        i=0
        while i<len(self.elems)-1:
            res+=self.elems[i].__str__()+","
            i+=1
        res+=self.elems[i].__str__()
        res+="]"
    def put(self,elem:Elem):
        self.elems.append(elem)
    def max(self)->int:
        assert len(self.elems)>=1
        return self.elems[-1].key
    def Find(self,Key:int):
        i=0
        while i<len(self.elems):
            if self.elems[i].key==Key:
                return i
            i+=1
        return -1
class BPT(object):
    M=4 #定义B+树的阶数
    def __init__(self,eps:int=4):
        self.height=0
        self.root=Node([])
        self.eps=eps
        BPT.M=eps
    def __str__(self):
        return "{root:"+str(self.root.__dict__)+",height:"+str(self.height)+",eps:"+str(self.eps)+"}"

    def insert(self,Key:int,Val:object):
        res=self._insertElem(self.root, Key, Val, self.height)
        if res==None:
            return
        newRoot=Node([])
        newRoot.put(Elem(res.max(), None, res))
        newRoot.put(Elem(self.root.max(), None, self.root))
        self.root=newRoot
        self.height+=1 # 因为根节点进行了分裂，所以高度要增加

    def _insertElem(self, node:Node, Key:int, Val:object, High:int)->Node:
        newElem=Elem(Key,Val,None)
        j=0
        if High==0: # 如果当前节点是叶子节点，则直接在elems列表中查找插入位置
            while j<len(node.elems):
                if Key<node[j].key:
                    break
                j+=1
        else: # 如果当前节点不是叶子节点，则要进行递归调用，直到叶子节点，还要处理节点分裂
            if node.max() < Key: # 插入的值如果大于当前节点的最大索引值，则将当前节点的最大索引值改为Key的值
                node[-1].key=Key
            while j<len(node.elems):
                if Key<=node[j].key: #找到了插入位置，就是第j个关键字指向的节点
                    res=self._insertElem(node[j].nextNode, Key, Val, High - 1)
                    if res==None:
                        return None
                    newElem.key=res.max()
                    newElem.nextNode=res
                    break
                j+=1
        # 新增elem到节点中
        node.elems= node.elems[:j] + [newElem] + node.elems[j:]
        if len(node.elems) <BPT.M:
            return None
        else:
            splitNode=Node(node.elems[:BPT.M // 2])
            node.elems= node.elems[BPT.M // 2:]
            return splitNode

    def search(self,Key:int)->Elem:
        return self._search(self.root,Key,self.height)
    def _search(self,node:Node,Key:int,High:int)->Elem:
        if High==0: # 如果当前是叶子节点，直接顺序查找即可
            for elem in node.elems:
                if elem.key==Key:
                    return elem
        else:
            for i in range(0,len(node.elems)):
                if Key<=node[i].key:
                    return self._search(node[i].nextNode,Key,High-1)
        return None

    def delete(self,Key:int):
        self.root=self._delete(self.root,Key,self.height)
        if len(self.root.elems)!=0:
            if len(self.root.elems)<2 and self.root[0].nextNode!=None: # B+树的根节点最少要有两个节点，否则就要取消根节点，减少高度
                self.root=self.root[0].nextNode
                self.height-=1

    def _delete(self,node:Node,Key:int,High:int)->Node:
        if High==0:
            ind=node.Find(Key)
            if ind!=-1:
                node.elems=node.elems[:ind]+node.elems[ind+1:] # 删除对应的元素
            return node
        else: #如果不是叶子节点，要先找到在哪里删，然后递归调用
            ind=0
            while ind<len(node.elems):
                if Key<=node[ind].key: # 要删除的数据应该在node的子树中
                    res=self._delete(node[ind].nextNode,Key,High-1)
                    if Key==node.max():
                        node[-1].key=res.max()
                    if len(res.elems)< BPT.M//2:
                        From=node.Find(res.max())
                        # 下面两行是debug信息
                        if From==-1: #说明删除的是叶节点的最大值
                            From=node.Find(Key)
                        # debug 结束
                        if From==0:
                            node=self._merge(node,From,From+1)
                        else:
                            node=self._merge(node,From-1,From)
                    break
                ind+=1
            return node
    def _merge(self,node:Node,From:int,To:int)->Node:
        # From<To
        # 先采用合并方式
        leftarr = node[From].nextNode.elems
        rightarr = node[To].nextNode.elems
        node[To].nextNode.elems = leftarr + rightarr
        if len(node[To].nextNode.elems) >= BPT.M:  # 如果需要分裂
            newNode = Node(node[To].nextNode.elems[:BPT.M // 2])
            node[To].nextNode.elems = node[To].nextNode.elems[BPT.M // 2:]
            # 更新node节点中对应索引的值
            node[From].nextNode = newNode
            node[From].key = newNode.max()
        else:  # 不需要分裂，则应删除对应的索引
            node.elems = node.elems[0:From] + node.elems[To:]
        return node

"""
下面是可视化代码
"""
class Group(object):
    ID=0
    def __init__(self,elems:list):
        self.keys=[]
        for elem in elems:
            self.keys.append(elem.key)
        self.nodeids=[] # 用于存储ids
        self.id=Group.ID
        Group.ID+=1
    def addIds(self,id):
        self.nodeids.append(id)
    def todict(self):
        dic={}
        dic["name"]="group"+str(self.id)
        dic["key"]=self.keys
        dic["nodeids"]=self.nodeids
        return dic

def visual(bpt:BPT)->dict:
    nodeid=0
    groups=[] # 存储所有的群组
    nodeids=[] # 所有节点的编号
    edges=[] # 所有边的集合，形式为[[fromId,toId],[fromId,toId]]
    queue=[] #层次遍历使用的队列,存储类型为node类型
    node=bpt.root

    group=Group(node.elems)
    nodeids+=[k for k in range(nodeid,nodeid+len(node.elems))]
    group.nodeids=[k for k in range(nodeid,nodeid+len(node.elems))]
    nodeid+=len(node.elems)
    groups.append(group)
    for i in range(len(node.elems)):
        if node[i].nextNode==None:
            continue
        queue.append((node[i].nextNode,group.nodeids[i]))
    while len(queue) !=0:
        top=queue[0][0]
        startid=queue[0][1]
        temp=Group(top.elems)
        nodeids+=[k for k in range(nodeid,nodeid+len(top.elems))]
        temp.nodeids=[k for k in range(nodeid,nodeid+len(top.elems))]
        nodeid+=len(top.elems)
        groups.append(temp)
        for i in range(len(top.elems)):
            if top[i].nextNode==None:
                continue
            queue.append((top[i].nextNode,temp.nodeids[i]))
        edges.append([startid,temp.nodeids[-1]])
        queue=queue[1:]
    result={}
    result["groups"]=[g.todict() for g in groups]
    result["edges"]=edges
    return result

def build_tree(keys:list,values:list)->BPT:
    assert len(keys)==len(values)
    bpt=BPT(eps=4)
    for key,value in zip(keys,values):
        bpt.insert(key,value)
    return bpt
