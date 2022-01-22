from typing import List

'''
    Only inheritance and explanations left
    All optimal solutions are already here
    There is a sub-optimal TreeNode soln in comments
'''

class DirNode:
    def __init__(self): #, dirname):
        # self.name = dirname
        self.dirs = {}
        self.files = {}
        
    def getOrCreateSubDir(self, subdirname):
        if subdirname not in self.dirs:
            self.dirs[subdirname] = DirNode() #subdirname)
        return self.dirs[subdirname]
    
    def isFile(self, filename):
        return filename in self.files
    
    def appendToFile(self, filename, content):
        if not self.isFile(filename):
            self.files[filename] = ''
        self.files[filename] += content
        
    def readFile(self, filename):
        return self.files[filename]

class FileSystem_DirNode:

    def __init__(self):
        self.root = DirNode() #'root')

    def ls(self, path: str) -> List[str]:
        if path == '/':
            # dont forget to list the files here too - Mistake 2
            return sorted(list(self.root.dirs.keys()) + list(self.root.files.keys()))
        
        head = self.root
        dirnames = path.split('/')
        for i in range(1, len(dirnames)-1):
            head = head.dirs[dirnames[i]]
        
        if head.isFile(dirnames[-1]):
            return [dirnames[-1]]
        else:
            # dont forget to list the files here too - Mistake 1
            return sorted(list(head.dirs[dirnames[-1]].dirs.keys()) + list(head.dirs[dirnames[-1]].files.keys()))

    def mkdir(self, path: str) -> None:        
        if path == '/':
            return
        
        head = self.root
        for dirname in path.split('/')[1:]:
            head = head.getOrCreateSubDir(dirname)
    
    def addContentToFile(self, filePath: str, content: str) -> None:
        head: DirNode = self.root
        dirnames = filePath.split('/')
        for i in range(1, len(dirnames)-1):
            head = head.dirs[dirnames[i]]
        head.appendToFile(dirnames[-1], content)

    def readContentFromFile(self, filePath: str) -> str:
        head: DirNode = self.root
        dirnames = filePath.split('/')
        for i in range(1, len(dirnames)-1):
            head = head.dirs[dirnames[i]]
        return head.files[dirnames[-1]]

    
class FileSystemObject:
    def __init__(self, isFile, content):
        self.childObjects = {}
        self.isFile = isFile
        self.content = content
    
    def getOrCreateSubDir(self, subdirname):
        if subdirname not in self.childObjects:
            self.childObjects[subdirname] = FileSystemObject(False, None)
        return self.childObjects[subdirname]
        
    def appendToFile(self, filename, content):
        if filename not in self.childObjects:
            self.childObjects[filename] = FileSystemObject(True, '')
        self.childObjects[filename].content += content
        
    def readFile(self, filename):
        return self.childObjects[filename].content

class FileSystem:

    def __init__(self):
        self.root = FileSystemObject(False, None)

    def ls(self, path: str) -> List[str]:
        head = self.root
        if path != '/':
            pathSegments = path.split('/')
            for i in range(1, len(pathSegments)):
                head = head.childObjects[pathSegments[i]]
            if head.isFile:
                return [pathSegments[-1]]
        
        return sorted(head.childObjects.keys())
    
    def mkdir(self, path: str) -> None:        
        if path == '/':
            return
        
        head = self.root
        for dirname in path.split('/')[1:]:
            head = head.getOrCreateSubDir(dirname)
    
    def addContentToFile(self, filePath: str, content: str) -> None:
        head = self.root
        pathSegments = filePath.split('/')
        for i in range(1, len(pathSegments)-1):
            head = head.childObjects[pathSegments[i]]
        head.appendToFile(pathSegments[-1], content)

    def readContentFromFile(self, filePath: str) -> str:
        head = self.root
        pathSegments = filePath.split('/')
        for i in range(1, len(pathSegments)):
            head = head.childObjects[pathSegments[i]]
        return head.content



# Your FileSystem object will be instantiated and called as such:
# obj = FileSystem()
# param_1 = obj.ls(path)
# obj.mkdir(path)
# obj.addContentToFile(filePath,content)
# param_4 = obj.readContentFromFile(filePath)