class Test(object):
    def __init__(self, name):
        self.name = name

    def __or__(self, other):
        return MySequence(self, other)
    
    def __str__(self): #__str__ 方法会在 print(对象) 时被 Python 自动调用，用返回值替代默认的内存地址，所以 print(a) 实际输出 a，print(b) 输出 b。
        return self.name

class MySequence(object):
    def __init__(self, *args):
        self.sequence = []
        for arg in args:
            self.sequence.append(arg)
    
    def __or__(self, other):
        self.sequence.append(other)
        return self
    
    def run(self):
        for item in self.sequence:
            print(item, end=' ')
        

if __name__ == "__main__":
    a = Test('a')
    b = Test('b')
    c = Test('c')

    d = a|b|c 
    d.run()