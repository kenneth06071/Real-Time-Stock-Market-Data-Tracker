import random


class id_Node:
    def __init__(self, id, price):
        self.id = id
        self.price=price
        self.volume=0
        
class price_Node:
    def __init__(self,id,price):
        self.left = None
        self.right = None
        self.height=1
        self.id = id
        self.price=price

class volume_Node:
    def __init__(self,id,volume):
        self.left = None
        self.right = None
        self.height=1
        self.id = id
        self.volume = volume

    
        
class id_hash_table:
    def __init__(self):
        self.m = 5000 #numebr of bucket hash table
        self.p = 1000019 #smallest prime larger than U
        self.a = 792481 #alpha between {1,2,...,p-1}
        self.b = 12839 #beta between {0,1,2,...,p-1}
        self.buckets = [[] for i in range (self.m)]
    
    def hash_index (self,id):
        key=id
        return (((self.a * key +self.b)%self.p)%self.m)
    
    #return 1 if duplicate
    def check_duplicate(self,id):
        hash_index = self.hash_index(id)
        n = len(self.buckets[hash_index]) #O(1) time
        for i in range (n): #O(1) expected  time
            if (self.buckets[hash_index][i].id==id):
                return 1
        return 0
    
    
        
    def insert_id(self,id,price):
        node= id_Node(id,price)
        hash_index = self.hash_index(node.id)
        self.buckets[hash_index].append(node)
    
    
    #get the old price from hash table and update the new price
    def get_and_update_price(self,id,new_price):
        hash_index= self.hash_index(id)
        n = len(self.buckets[hash_index])
        for i in range (n):
            if (self.buckets[hash_index][i].id==id):
                old_price = self.buckets[hash_index][i].price
                self.buckets[hash_index][i].price = new_price
                return old_price
    
    def get_volume(self,id):
        hash_index= self.hash_index(id)
        n = len(self.buckets[hash_index])
        for i in range (n):
            if (self.buckets[hash_index][i].id==id):
                old_volume = self.buckets[hash_index][i].volume
                return old_volume

    def update_volume(self,id,volume_inc):
        hash_index= self.hash_index(id)
        n = len(self.buckets[hash_index])
        for i in range (n):
            if (self.buckets[hash_index][i].id==id):
                self.buckets[hash_index][i].volume+=volume_inc
                return self.buckets[hash_index][i].volume
    
    def get_stock_info(self,id):
        hash_index= self.hash_index(id)
        n = len(self.buckets[hash_index])
        for i in range (n):
            if (self.buckets[hash_index][i].id==id):
                return [self.buckets[hash_index][i].id,self.buckets[hash_index][i].price,self.buckets[hash_index][i].volume]         
        return None    

        

class price_tree: #AVL tree for price
    def __init__(self):
        self.root = None
        
    def get_height(self,node):
        if node is None:
            return 0
        return node.height
    
    def get_balance(self,node):  #left-right
        return self.get_height(node.left)-self.get_height(node.right)
    
    def right_rotate (self,a):
        b =a.left
        T2 = b.right
        
        #Start rotation
        b.right = a
        a.left = T2
    
        a.height = 1 +max(self.get_height(a.left),self.get_height(a.right))
        b.height = 1+max(self.get_height(b.left),self.get_height(b.right))
        
        return b
    
    def left_rotate (self,a):
        b = a.right
        T2 = b.left
        
        #start rotation
        b.left = a
        a.right = T2
        
        a.height = 1 +max(self.get_height(a.left),self.get_height(a.right))
        b.height = 1+max(self.get_height(b.left),self.get_height(b.right))
        
        return b
    
    def insert_price(self,node,id,price): #Creating a BST using price as key
        if node is None:
            #Insert to the BST
            node=price_Node(id,price)            
        #smaller go left
        elif (node.price,node.id) > (price,id):
            node.left = self.insert_price(node.left,id,price)
        #larger or equal go right
        else:
            node.right = self.insert_price(node.right,id,price)

        #checking for balancy
        node.height = 1 + max(self.get_height(node.left),self.get_height(node.right))
            
        balance= self.get_balance(node)
        
            
        #Rebalancing
        #LL
        if balance >1 and self.get_balance(node.left)>=0:
            return self.right_rotate(node)
        #LR
        if balance >1 and self.get_balance(node.left)<0:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)
            
        #RR
        if balance < -1 and self.get_balance(node.right)<=0:
            return self.left_rotate(node)
            
        #RL
        if balance < -1 and self.get_balance(node.right)>0:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)
               
        return node
    
    def minValueNode(self,node):
        current = node
        while current.left is not None:
            current = current.left
        return current
    
    def delete_price(self,node,id,price):
        if not node:
            return node

        if  (price,id) < (node.price,node.id):
            node.left = self.delete_price(node.left, id, price)
        elif (price,id) > (node.price,node.id):
            node.right = self.delete_price(node.right,id,price)
        else:
            if node.left is None:
                temp = node.right
                node = None
                return temp
            elif node.right is None:
                temp = node.left
                node = None
                return temp

            temp = self.minValueNode(node.right)
            node.price = temp.price
            node.id = temp.id
            node.right = self.delete_price(node.right, temp.id, temp.price)

        if node is None:
            return node
        
        node.height = 1 + max(self.get_height(node.left),self.get_height(node.right))
            
        balance= self.get_balance(node)
        
            
        #Rebalancing
        #LL
        if balance >1 and self.get_balance(node.left)>=0:
            return self.right_rotate(node)
        #LR
        if balance >1 and self.get_balance(node.left)<0:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)
            
        #RR
        if balance < -1 and self.get_balance(node.right)<=0:
            return self.left_rotate(node)
            
        #RL
        if balance < -1 and self.get_balance(node.right)>0:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)
               
        return node
    
    def range_reporting(self,root,p1,p2,result):
        if root is None:
            return
        
        if p1<= root.price <= p2:
            self.range_reporting(root.left, p1, p2, result)
            result.append(root.id)
            self.range_reporting(root.right,p1, p2, result)
        
        elif root.price<p1:
            self.range_reporting(root.right,p1, p2, result)
            
        else:
            self.range_reporting(root.left, p1, p2, result)
            
            
        
    
class volume_tree:
    def __init__(self):
        self.root = None
        
    def get_height(self,node):
        if node is None:
            return 0
        return node.height
    
    def get_balance(self,node):  #left-right
        return self.get_height(node.left)-self.get_height(node.right)
    
    def right_rotate (self,a):
        b =a.left
        T2 = b.right
        
        #Start rotation
        b.right = a
        a.left = T2
    
        a.height = 1 +max(self.get_height(a.left),self.get_height(a.right))
        b.height = 1+max(self.get_height(b.left),self.get_height(b.right))
        
        return b
    
    def left_rotate (self,a):
        b = a.right
        T2 = b.left
        
        #start rotation
        b.left = a
        a.right = T2
        
        a.height = 1 +max(self.get_height(a.left),self.get_height(a.right))
        b.height = 1+max(self.get_height(b.left),self.get_height(b.right))
        
        return b
    
    def insert_volume(self,node,id,volume):
        if node is None:
            #Insert to the BST
            node=volume_Node(id,volume)            
        #smaller go left
        elif (node.volume,node.id) > (volume,id):
            node.left = self.insert_volume(node.left,id,volume)
        #larger or equal go right
        else:
            node.right = self.insert_volume(node.right,id,volume)
            

        #checking for balancy
        node.height = 1 + max(self.get_height(node.left),self.get_height(node.right))
            
        balance= self.get_balance(node)
        
            
        #Rebalancing
        #LL
        if balance >1 and self.get_balance(node.left)>=0:
            return self.right_rotate(node)
        #LR
        if balance >1 and self.get_balance(node.left)<0:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)
            
        #RR
        if balance < -1 and self.get_balance(node.right)<=0:
            return self.left_rotate(node)
            
        #RL
        if balance < -1 and self.get_balance(node.right)>0:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)
               
        return node
    
    def minValueNode(self,node):
        current = node
        while current.left is not None:
            current = current.left
        return current
    
    def delete_volume(self,node,id,volume):
        if not node:
            return node

        if  (volume,id) < (node.volume,node.id):
            node.left = self.delete_volume(node.left, id, volume)
        elif (volume,id) > (node.volume,node.id):
            node.right = self.delete_volume(node.right,id,volume)
        else:
            if node.left is None:
                temp = node.right
                node = None
                return temp
            elif node.right is None:
                temp = node.left
                node = None
                return temp

            temp = self.minValueNode(node.right)
            node.id = temp.id
            node.volume = temp.volume
            node.right = self.delete_volume(node.right, temp.id, temp.volume)

        if node is None:
            return node
        
        node.height = 1 + max(self.get_height(node.left),self.get_height(node.right))
            
        balance= self.get_balance(node)
        
            
        #Rebalancing
        #LL
        if balance >1 and self.get_balance(node.left)>=0:
            return self.right_rotate(node)
        #LR
        if balance >1 and self.get_balance(node.left)<0:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)
            
        #RR
        if balance < -1 and self.get_balance(node.right)<=0:
            return self.left_rotate(node)
            
        #RL
        if balance < -1 and self.get_balance(node.right)>0:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)
               
        return node
    
    def get_max_volume(self,root):
        if root is None:
            return 
        
        curr = root
        
        while curr.right is not None:
            curr = curr.right
        
        return [curr.id,curr.volume]
    

        

class stock_tracker:
    def __init__(self):
        self.id = id_hash_table()
        self.price = price_tree()
        self.volume= volume_tree()
        
    def insert_new_stock(self,id,price):
        #check whether id exist in the hash table first
        if self.id.check_duplicate(id) ==0 :
            self.id.insert_id(id,price) #O(1) expected
            self.price.root = self.price.insert_price(self.price.root,id,price) #O(logn)
            self.volume.root = self.volume.insert_volume(self.volume.root,id,0) #O(logn)


    def update_price(self,id,new_price):
        #finsih update in the hash_table
        if self.id.check_duplicate(id) ==1 :
            old_price = self.id.get_and_update_price(id,new_price)
        
            self.price.root = self.price.delete_price(self.price.root, id,old_price)
        
            self.price.root = self.price.insert_price(self.price.root,id,new_price)

    def increase_volume(self,id,volume_inc):
        if self.id.check_duplicate(id) ==1 :
            #finsih update in the hash_table
            old_volume = self.id.get_volume(id)
            #new volume = old volume + volue_inc
            new_volume = self.id.update_volume(id, volume_inc)
            self.volume.root = self.volume.delete_volume(self.volume.root,id,old_volume)
            self.volume.root = self.volume.insert_volume(self.volume.root,id,new_volume)
 
    def lookup_by_id (self, id):
        info = self.id.get_stock_info(id)
        if info is None:
           return
        else:
            return (info[0],info[1],info[2])
    
    def price_range (self,p1,p2):
        result=[]
        self.price.range_reporting(self.price.root,p1,p2,result)
        return result
    
    def max_vol (self):
        return self.volume.get_max_volume(self.volume.root)







    


    



