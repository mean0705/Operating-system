import operator
import queue
import struct
import copy

class Process():
    def __init__(self, id, cpu_burst, arrival_time, priority, waiting_time, turnaround_time, cpu_leftTime, hasBeen ):
        self.id = int(id)
        self.cpu_burst = int(cpu_burst)
        self.arrival_time = int(arrival_time)
        self.priority = int(priority)
        self.waiting_time = int(waiting_time)
        self.turnaround_time = int(turnaround_time)
        self.cpu_leftTime = int(cpu_leftTime)
        self.hasBeen = int(hasBeen)

def SaveData(file):
    process_list = []

    line = file.readline()
    line_data = line.split()
    method = int(line_data[0])
    time_slice = int(line_data[1])
    
    line = file.readline()

    for line in file.readlines():
         line_data = line.split()
         process = Process( line_data[0], line_data[1], line_data[2], line_data[3], 0, 0, line_data[1], 0)
         process_list.append(process)

    return method, time_slice, process_list

def FCFS(time_slice, process_list):
    iid = []
    WaitingProcess = []
    final_list = []
    process_list.sort(key=operator.attrgetter('arrival_time', 'id'))
    current_time = 0
    i = 0
    while 1:
        if i < len(process_list) and process_list[i].arrival_time == current_time: 
            WaitingProcess.append(process_list[i])
            i+=1
            continue
        else:
            if len(WaitingProcess) != 0 :
                for j in range(0, WaitingProcess[0].cpu_burst):            
                  while i < len(process_list) and process_list[i].arrival_time == current_time:                              
                      WaitingProcess.append(process_list[i])
                      i+=1
                  current_time += 1
                  iid.append(WaitingProcess[0].id)

                WaitingProcess[0].turnaround_time = current_time - WaitingProcess[0].arrival_time
                WaitingProcess[0].waiting_time = WaitingProcess[0].turnaround_time - WaitingProcess[0].cpu_burst
                final_list.append(WaitingProcess[0])
                del WaitingProcess[0]
            else: 
                if i == len(process_list): break
                else: 
                    current_time += 1
                    iid.append(-1)

    final_list.sort(key=operator.attrgetter('id'))

    return final_list, iid
       
def RR(time_slice, process_list):
    final_list = []
    WaitingProcess = []
    saveProcess= []
    iid = []
    iid[:] = []

    process_list.sort(key=operator.attrgetter('arrival_time', 'id'))

    current_time = 0
    i = 0
    while 1:
        if i < len(process_list) and process_list[i].arrival_time == current_time: 
            while i < len(process_list) and process_list[i].arrival_time == current_time:
                WaitingProcess.append(process_list[i])
                i+=1 

            if saveProcess : 
                WaitingProcess.append(saveProcess[0])
                saveProcess [:] = []
            continue
        else:
            if saveProcess : 
                WaitingProcess.append(saveProcess[0])
                saveProcess [:] = []

            if len(WaitingProcess) != 0 :               
                for t in range(0, time_slice):
                  if WaitingProcess[0].cpu_leftTime == 0: break
                  if i < len(process_list) and process_list[i].arrival_time == current_time:
                      while i < len(process_list) and process_list[i].arrival_time == current_time:
                          WaitingProcess.append(process_list[i])
                          i+=1 

                  current_time += 1
                  iid.append(WaitingProcess[0].id)
                  WaitingProcess[0].cpu_leftTime -= 1

                if WaitingProcess[0].cpu_leftTime == 0:
                   WaitingProcess[0].turnaround_time = current_time - WaitingProcess[0].arrival_time
                   WaitingProcess[0].waiting_time = WaitingProcess[0].turnaround_time - WaitingProcess[0].cpu_burst
                   final_list.append(WaitingProcess[0])
                   del WaitingProcess[0]
                   saveProcess [:] = []
                else:
                    saveProcess.append(WaitingProcess[0])
                    del WaitingProcess[0]
            else: 
                if i == len(process_list): break              
                else: 
                    current_time += 1
                    iid.append(-1)
                           
    final_list.sort(key=operator.attrgetter('id'))

    return final_list, iid
  
def PSJF(time_slice, process_list):
    final_list = []
    WaitingProcess = []
    iid = []

    final_list[:] = []
    WaitingProcess.clear()
    iid[:] = []
    hasMinCpuProcessIn = 0
    needToP = 0

    process_list.sort(key=operator.attrgetter('arrival_time', 'id'))
    current_time = 0
    i = 0
    while 1:
        if i < len(process_list) and process_list[i].arrival_time == current_time:           
            WaitingProcess.append(process_list[i])
            i+=1
            continue
        else:
            if len(WaitingProcess) != 0 :
                WaitingProcess.sort(key=operator.attrgetter('cpu_leftTime', 'hasBeen', 'arrival_time', 'id'))
                while 1:
                  if WaitingProcess[0].hasBeen == 0: WaitingProcess[0].hasBeen = 1
                  if WaitingProcess[0].cpu_leftTime == 0: break
                  if i < len(process_list) and process_list[i].arrival_time == current_time:
                      while i < len(process_list) and process_list[i].arrival_time == current_time:
                          if process_list[i].cpu_leftTime <= WaitingProcess[0].cpu_leftTime:  needToP = 1
                          WaitingProcess.append(process_list[i])
                          i+=1

                      if needToP == 1: 
                          needToP = 0
                          break

                  current_time += 1
                  iid.append(WaitingProcess[0].id)
                  WaitingProcess[0].cpu_leftTime -= 1
                  
                if WaitingProcess[0].cpu_leftTime == 0:
                   WaitingProcess[0].turnaround_time = current_time - WaitingProcess[0].arrival_time
                   WaitingProcess[0].waiting_time = WaitingProcess[0].turnaround_time - WaitingProcess[0].cpu_burst
                   final_list.append(WaitingProcess[0])
                   del WaitingProcess[0]
            else: 
                if i == len(process_list): break
                else: 
                    current_time += 1
                    iid.append(-1)

    final_list.sort(key=operator.attrgetter('id'))

    return final_list, iid
 
def NPSJF(time_slice, process_list):
    final_list = []
    WaitingProcess = []
    iid = []

    final_list[:] = []
    WaitingProcess.clear()
    iid[:] = []

    process_list.sort(key=operator.attrgetter('arrival_time', 'id'))
    current_time = 0
    i = 0
    while 1:
        if i < len(process_list) and process_list[i].arrival_time == current_time: 
            WaitingProcess.append(process_list[i])
            i+=1
            continue
        else:
            if len(WaitingProcess) != 0 :
                WaitingProcess.sort(key=operator.attrgetter('cpu_burst', 'arrival_time', 'id'))
                for j in range(0, WaitingProcess[0].cpu_burst):            
                  while i < len(process_list) and process_list[i].arrival_time == current_time:                              
                      WaitingProcess.append(process_list[i])
                      i+=1
                  current_time += 1
                  iid.append(WaitingProcess[0].id)

                WaitingProcess[0].turnaround_time = current_time - WaitingProcess[0].arrival_time
                WaitingProcess[0].waiting_time = WaitingProcess[0].turnaround_time - WaitingProcess[0].cpu_burst
                final_list.append(WaitingProcess[0])
                del WaitingProcess[0]
            else: 
                if i == len(process_list): break
                else: 
                    current_time += 1
                    iid.append(-1)
                
    final_list.sort(key=operator.attrgetter('id'))
    
    return final_list, iid

def PP(time_slice, process_list):
    final_list = []
    WaitingProcess = []
    iid = []
    saveProcess = []

    final_list[:] = []
    WaitingProcess[:] = []
    iid[:] = []
    saveProcess[:] = []
    hasMinCpuProcessIn = 0
    needToP = 0

    process_list.sort(key=operator.attrgetter('arrival_time', 'id'))

    current_time = 0
    i = 0
    while 1:
        if i < len(process_list) and process_list[i].arrival_time == current_time: 
            while i < len(process_list) and process_list[i].arrival_time == current_time:
                  WaitingProcess.append(process_list[i])
                  i+=1
            if saveProcess : 
                WaitingProcess.append(saveProcess[0])
                saveProcess [:] = []
            continue
        else:
            if saveProcess : 
                WaitingProcess.append(saveProcess[0])
                saveProcess [:] = []
            if len(WaitingProcess) != 0 :
                WaitingProcess.sort(key=operator.attrgetter('priority', 'hasBeen','arrival_time', 'id'))
                runningProcess = WaitingProcess[0]
                while 1:
                  if runningProcess.hasBeen == 0: runningProcess.hasBeen = 1
                  if runningProcess.cpu_leftTime == 0: break
                  if i < len(process_list) and process_list[i].arrival_time == current_time:   
                      while i < len(process_list) and process_list[i].arrival_time == current_time:
                          if process_list[i].priority < WaitingProcess[0].priority:  needToP = 1
                          WaitingProcess.append(process_list[i])
                          i+=1
                 
                      if needToP == 1: 
                          needToP = 0
                          break
                      
                  current_time += 1
                  iid.append(WaitingProcess[0].id)
                  runningProcess.cpu_leftTime -= 1

                if runningProcess.cpu_leftTime == 0:
                   runningProcess.turnaround_time = current_time - runningProcess.arrival_time
                   runningProcess.waiting_time = runningProcess.turnaround_time - runningProcess.cpu_burst
                   final_list.append(WaitingProcess[0])
                   del WaitingProcess[0]

                else:
                    saveProcess.append(WaitingProcess[0])
                    del WaitingProcess[0]

            else: 
                if i == len(process_list): break
                else: 
                    current_time += 1
                    iid.append(-1)

    final_list.sort(key=operator.attrgetter('id'))

    return final_list, iid

def Output1File(fileName, out_list, gantt_chart, missionName):
    file = open(fileName + '_' + missionName + '_output.txt', "w")  
    file.write('==  ')
    file.write(missionName)
    file.write('==\n')
    for i in gantt_chart:
         if i == -1:
            file.write('-')
         elif i < 10:
            file.write(str(i))
         else:
            file.write(chr(i-10+ord('A')))

    file.write('\n=================================================\n\n')
    file.write('Waiting Time\n')
    file.write('ID  ')
    file.write(missionName)
    file.write('\n=================================================\n')
    for j in out_list:
        file.write(str(j.id))
        if j.id < 10: file.write(' ')
        file.write('  ')
        file.write(str(j.waiting_time))
        file.write('\n')

    file.write('=================================================\n\n')

    file.write('Turnaround Time\n')
    file.write('ID  ')
    file.write(missionName)
    file.write('\n=================================================\n')
    for k in out_list:
        file.write(str(k.id))
        if k.id < 10: file.write(' ')
        file.write('  ')
        file.write(str(k.turnaround_time))
        file.write('\n')

    file.write('=================================================')
    file.close()

def Output5File(fileName, out_list1, out_list2, out_list3, out_list4, out_list5, gantt_chart1, gantt_chart2, gantt_chart3, gantt_chart4, gantt_chart5):
    file = open(fileName + '_ALL_output.txt', "w")  

    file.write('==  FCFS==\n')
    for i in gantt_chart1:
         if i == -1: file.write('-')
         elif i < 10: file.write(str(i))           
         else:      file.write(chr(i-10+ord('A')))
        
    file.write('\n==  RR==\n')
    for i in gantt_chart2:
         if i == -1: file.write('-')
         elif i < 10: file.write(str(i))           
         else:      file.write(chr(i-10+ord('A')))

    file.write('\n==  PSJF==\n')
    for i in gantt_chart3:
         if i == -1: file.write('-')
         elif i < 10: file.write(str(i))          
         else:      file.write(chr(i-10+ord('A')))

    file.write('\n==  NON-PSJF==\n')
    for i in gantt_chart4:
         if i == -1: file.write('-')
         elif i < 10: file.write(str(i))            
         else:      file.write(chr(i-10+ord('A')))

    file.write('\n==  Priority==\n')
    for i in gantt_chart5:
         if i == -1: file.write('-')
         elif i < 10: file.write(str(i))            
         else:      file.write(chr(i-10+ord('A')))

    file.write('\n=================================================\n\n')
    file.write('Waiting Time\n')
    file.write('ID      FCFS    RR      PSJF    NPSJF   Priority')
    file.write('\n=================================================\n')
    for j in range(len(out_list1)):
        file.write(str(out_list1[j].id))
        if out_list1[j].id < 10: file.write(' ')
        file.write('  ')
        file.write(str(out_list1[j].waiting_time))
        if out_list1[j].waiting_time < 10: file.write(' ')
        file.write('    ')
        file.write(str(out_list2[j].waiting_time))
        if out_list2[j].waiting_time < 10: file.write(' ')
        file.write('    ')
        file.write(str(out_list3[j].waiting_time))
        if out_list3[j].waiting_time < 10: file.write(' ')
        file.write('    ')
        file.write(str(out_list4[j].waiting_time))
        if out_list4[j].waiting_time < 10: file.write(' ')
        file.write('    ')
        file.write(str(out_list5[j].waiting_time))
        if out_list5[j].waiting_time < 10: file.write(' ')
        file.write('    ')
        file.write('\n')

    file.write('=================================================\n\n')

    file.write('Turnaround Time\n')
    file.write('ID      FCFS    RR      PSJF    NPSJF   Priority')
    file.write('\n=================================================\n')

    for k in range(len(out_list1)):
        file.write(str(out_list1[k].id))
        if out_list1[k].id < 10: file.write(' ')
        file.write('  ')
        file.write(str(out_list1[k].turnaround_time))
        if out_list1[k].turnaround_time < 10: file.write(' ')
        file.write('    ')
        file.write(str(out_list2[k].turnaround_time))
        if out_list2[k].turnaround_time < 10: file.write(' ')
        file.write('    ')
        file.write(str(out_list3[k].turnaround_time))
        if out_list3[k].turnaround_time < 10: file.write(' ')
        file.write('    ')
        file.write(str(out_list4[k].turnaround_time))
        if out_list4[k].turnaround_time < 10: file.write(' ')
        file.write('    ')
        file.write(str(out_list5[k].turnaround_time))
        if out_list5[k].turnaround_time < 10: file.write(' ')
        file.write('    ')
        file.write('\n')

    file.write('=================================================')
    file.close()

if __name__ == '__main__':
    
    while (1):
        fileName = input('Give your file name(if your file is A.txt, input A ) \n or input 0 to terminate the program: ')
        if fileName == "0" : break
        file = open(fileName + ".txt" , "r")

        method, time_slice, process_list = SaveData(file)
        process1 = copy.deepcopy(process_list)
        process2 = copy.deepcopy(process_list)
        process3 = copy.deepcopy(process_list)
        process4 = copy.deepcopy(process_list)
        process5 = copy.deepcopy(process_list)
        gantt_chart1 = []
        gantt_chart2 = []
        gantt_chart3 = []
        gantt_chart4 = []
        gantt_chart5 = []

        if method == 1:
            process1, gantt_chart1 = FCFS(time_slice, process1)
            Output1File(fileName, process1, gantt_chart1, 'FCFS')
        elif method == 2:
            process2, gantt_chart2 = RR(time_slice, process2)
            Output1File(fileName, process2, gantt_chart2, 'RR')
        elif method == 3:
            process3, gantt_chart3 = PSJF(time_slice, process3)
            Output1File(fileName, process3, gantt_chart3, 'PSJF')
        elif method == 4:
            process4, gantt_chart4 = NPSJF(time_slice, process4)
            Output1File(fileName, process4, gantt_chart4, 'NPSJF')
        elif method == 5:
            process5, gantt_chart5 = PP(time_slice, process5)
            Output1File(fileName, process5, gantt_chart5, 'PP')
        elif method == 6:
            process1, gantt_chart1 = FCFS(time_slice, process1)
            process2, gantt_chart2 = RR(time_slice, process2)
            process3, gantt_chart3 = PSJF(time_slice, process3)
            process4, gantt_chart4 = NPSJF(time_slice, process4)
            process5, gantt_chart5 = PP(time_slice, process5)
            Output5File(fileName, process1, process2, process3, process4, process5, gantt_chart1, gantt_chart2, gantt_chart3, gantt_chart4, gantt_chart5 )

            
        print('end\n\n')