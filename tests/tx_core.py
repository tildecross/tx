#!/usr/bin/env python3

import os
import sys

# Include library directory
SCRIPT_PATH = "/".join(os.path.realpath(__file__).split("/")[:-1])
sys.path.insert(0, SCRIPT_PATH + "/../lib")

from tx import tx

class Test1:
    def __init__(self, sandbox):
        self.sandbox = sandbox
        
    def create(self):
        print("Test 1")
    
    def remove(self):
        print("Removed Test 1")

class Test2:
    def __init__(self, sandbox):
        self.sandbox = sandbox
        
    def create(self, x, y, z):
        print("Test 2")
        self.sum([x, y, z])
        
    def sum(self, arr):
        self.sandbox.notify({
            "name": "sum-and-remove",
            "data": {
                "arr": arr,
                "ctx": self
            }
        })
    
    def remove(self):
        print("Removed Test 2")

class Test3:
    def __init__(self, sandbox):
        self.sandbox = sandbox
        
    def create(self):
        print("Test 3")
        self.sandbox.listen("sum-and-remove", self.sum_and_remove)
        
    def sum_and_remove(self, data):
        x, y, z = data["arr"]
        print("Sum: %s" % (x + y + z))
        self.sandbox.silence("sum-message")
        data["ctx"].remove()
    
    def remove(self):
        print("Removed Test 3")

tx.core.register("test1", Test1)
tx.core.register("test2", Test2)
tx.core.register("test3", Test3)


tx.core.start("test1", deps=[
    lambda: tx.core.start("test2", args=[1, 2, 3], deps=[
        lambda: tx.core.start("test3")
    ])
])

# Expected:
# =========
# Test 3
# Test 2
# Sum: 6
# Removed Test 2
# Test 1
