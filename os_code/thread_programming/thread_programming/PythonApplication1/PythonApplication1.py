import threading
import multiprocessing 
import time
import queue

def AllList(fileName, file):
    readData = file.read()
    x = readData.split()
    data = list(map(int, x))
    return data

def SeperatedList(fileName, numOfSep, file):
    data = AllList(fileName, file)
    length_data = len(data)
    n = len(data) // numOfSep
    sepList = []

    for i in range(0, n*numOfSep, n):
        sepList.append(data[i:i+n])

    sepList[numOfSep-1].extend(data[n*numOfSep:length_data])
    return sepList

def BubbleSortForList(list):
    length_list = len(list)
    for i in range(length_list):
        for j in range(length_list-1-i):
            if list[j] > list[j+1]:
                list[j], list[j+1] = list[j+1], list[j] 
    return list

def BubbleSort(list, result):
    length_list = len(list)
    for i in range(length_list):
        for j in range(length_list-1-i):
            if list[j] > list[j+1]:
                list[j], list[j+1] = list[j+1], list[j] 
    result.put(list)

def MergeSort(_leftList, _rightList, result): 
    index_l = 0 
    index_r = 0
    length_l = len(_leftList)
    length_r = len(_rightList)
    items = []
    
    while index_l < length_l and index_r < length_r:
        if _leftList[index_l] < _rightList[index_r]:
            items.append(_leftList[index_l])
            index_l = index_l + 1
        else : 
            items.append(_rightList[index_r])
            index_r = index_r + 1

    if index_l == length_l:
        items.extend(_rightList[index_r:length_r])
    else:
        items.extend(_leftList[index_l:length_l])

    result.put(items)

def Process_BubbleAndMerge(list, result):
    for l in list:
        BubbleSort(l, result)

    while result.qsize() != 1:
        _leftlist = result.get()
        _rightlist = result.get()
        MergeSort(_leftlist, _rightlist, result)
    
def OutputFile(fileName, list, cpu_time):
    file = open(fileName + '_output.txt', "w")  
    for i in list:
        file.write(str(i) + ' ')
    file.write('\nCPU time : ')
    file.write(str(cpu_time))
    file.write(' secs')
    file.close()

def mission1(fileName,file):
    list = AllList(fileName,file)
    start = time.time() 

    bubble_list = [len(list)]
    bubble_list = BubbleSortForList(list)

    cpu_time = time.time() - start
    print('\nCPU Time: ' + str(cpu_time))
    OutputFile(fileName, bubble_list, cpu_time)

def mission2(fileName,file):
    numOfCopy = input('How many copies of this document do you want?: ')
    while not numOfCopy.isdigit():
         print('this is not integer...please enter again')
         numOfCopy = input('value k: ')
    numOfCopy = int(numOfCopy)

    start = time.time() 

    sepList = SeperatedList(fileName, numOfCopy, file)  
    q = queue.Queue(numOfCopy) 
    threads = []
    merge_threads = []

    for i in range(numOfCopy):
        thread = threading.Thread(target=BubbleSort, args=(sepList[i], q))
        threads.append(thread)

    for t in range(numOfCopy):
        threads[t].start()

    ##for tt in threads: 
    ##    tt.join() 

    mt = 0
    while mt < numOfCopy - 1:
        if q.qsize() > 1:
            _leftlist = q.get()
            _rightlist = q.get()
            mergeThread = threading.Thread(target=MergeSort, args=(_leftlist, _rightlist, q))
            mergeThread.start()
            merge_threads.append(mergeThread)
            mt = mt + 1

    for m in merge_threads: 
        m.join() 
    
    cpu_time = time.time() - start 
    print('\nCPU Time: ' + str(cpu_time))
    OutputFile(fileName, q.get(), cpu_time)

def mission3(fileName, file):
    numOfCopy = input('How many copies of this document do you want?: ')
    while not numOfCopy.isdigit():
         print('this is not integer...please enter again')
         numOfCopy = input('value k: ')
    numOfCopy = int(numOfCopy)

    start = time.time() 

    sepList = SeperatedList(fileName, numOfCopy, file) 
    manager = multiprocessing.Manager()
    q = manager.Queue(numOfCopy) 
    processes = []
    merge_processes = []
    
    for i in range(numOfCopy):
        processes.append(multiprocessing.Process(target=BubbleSort, args=(sepList[i], q)))

    for p in range(numOfCopy):
        processes[p].start()

    ##for pp in processes: 
    ##    pp.join() 

    mp = 0
    while mp < numOfCopy - 1:
        if q.qsize() > 1: 
            _leftlist = q.get()
            _rightlist = q.get()
            mergeProcesses = multiprocessing.Process(target=MergeSort, args=(_leftlist, _rightlist, q))
            mergeProcesses.start()
            merge_processes.append(mergeProcesses)
            mp = mp + 1

    for m in merge_processes: 
        m.join() 
        

    cpu_time = time.time() - start 

    print('\nCPU Time: ' + str(cpu_time))
    OutputFile(fileName, q.get(), cpu_time)


def mission4(fileName, file):
    numOfCopy = input('How many copies of this document do you want?: ')
    while not numOfCopy.isdigit():
         print('this is not integer...please enter again')
         numOfCopy = input('value k: ')
    numOfCopy = int(numOfCopy)

    start = time.time() 

    sepList = SeperatedList(fileName, numOfCopy, file) 
    manager = multiprocessing.Manager()
    q = manager.Queue(numOfCopy)
    process_BubbleAndMerge = multiprocessing.Process(target = Process_BubbleAndMerge, args = (sepList, q))

    process_BubbleAndMerge.start()
    process_BubbleAndMerge.join()



    cpu_time = time.time() - start # clock end

    print('\nCPU Time: ' + str(cpu_time))
    OutputFile(fileName, q.get(), cpu_time)

if __name__ == '__main__':

    while (1):
        fileName = input('Give your file name(if your file is A.txt, input A ) \n or input 0 to terminate the program: ')
        if fileName == "0" : break
        f = open(fileName + ".txt" , "r")
        command = f.read(1)
    
        if command == '1':   mission1(fileName, f)          
        elif command == '2': mission2(fileName, f)           
        elif command == '3': mission3(fileName, f)           
        elif command == '4': mission4(fileName, f)            
        else : print('error')
            
        print('end\n\n')
