class MyClass:
    __name="xxx"
    gender="male"
    def __init__(self):
        self.__name="Gary"

    def hisName(self, name):
        self.__name=name

    def printName(self):
        self.hisName("Harry")
        print("Name: %s" % self.__name)

def main():
    mc = MyClass()
    mc.printName()
    print(mc.gender)

if __name__=="__main__":
    main()

        
