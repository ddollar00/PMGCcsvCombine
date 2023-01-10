import sys
import os
import pandas as pd


class csvCombine:
    
    def combine(self, argv: list):
        heapsize = 100000
        llist = []

        if self.isValidPath(argv):
            files = argv[1:]

            for path in files:
                for heap in pd.read_csv(path, chunksize=heapsize):
                    filename = os.path.basename(path)# this will give us the filename that we need, using the path
                    heap['filename'] = filename
                    llist.append(heap)   #were adding the filename column to this heap and appending the heap to the list
            
            header = True # lets us knw if we need to add another heaser

            
            for heap in llist:
                print(heap.to_csv(index=False, header=header, lineterminator='\n', chunksize=heapsize), end='')  # combining all the heaps
                header = False
        else:
            return

    @staticmethod
    def isValidPath(argv): # error cheching with the entered file paths
      
        if len(argv) <= 1:
            print("Enter a file path")
            return False

        files = argv[1:]

        for path in files:
            if not os.path.exists(path):
                print("couldn't find this File: " + path)
                return False
            if os.stat(path).st_size == 0:
                print("empty file: " + path)
                return False
        return True

    


def main():
    
    csvCombine().combine(sys.argv)

if __name__ == '__main__':
    main()
