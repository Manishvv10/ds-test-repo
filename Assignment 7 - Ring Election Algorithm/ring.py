# we define MAX as the maximum number of processes our program can simulate
# we declare pStatus to store the process status; 0 for dead and 1 for alive
# we declare n as the number of processes
# we declare coordinator to store the winner of election

MAX = 20
pStatus = [0 for _ in range(MAX)]
n = 0
coordinator = 0

def ring():
    " ring election implementation"
    global coordinator, n
    condition = True
    while condition:
        print('---------------------------------------------')
        print("1.CRASH\n2.ACTIVATE\n3.DISPLAY\n4.EXIT")
        print('---------------------------------------------\n')
        print("Enter your choice: \t")
        tchoice = int(input())
        if tchoice == 1:
            print("\nEnter process to crash : \t")
            crash = int(input())

            if pStatus[crash]:
                pStatus[crash] = 0
            else:
                print("Process", crash, "is already dead!\n")
            condition = True
            while condition:
                print("Enter election generator id: \t")
                gid = int(input())
                if gid == coordinator:
                    print("Please, enter a valid generator id!\n")
                condition = (gid == coordinator)

            if crash == coordinator:
                subcoordinator = 1
                i = 0
                while i < (n+1):
                    pid = (i + gid) % (n+1)
                    if pid != 0:     # since our process starts from 1 (to n)
                        if pStatus[pid] and subcoordinator < pid:
                            subcoordinator = pid
                        print("Election message passed from", pid, ": #Msg", subcoordinator, "\n")
                    i += 1

                coordinator = subcoordinator
            display()

        elif tchoice == 2:
            print("Enter Process ID to be activated: ")
            activate = int(input())
            if not pStatus[activate]:
                pStatus[activate] = 1
            else:
                print("Process", activate, "is already alive!\n")
                break

            subcoordinator = activate
            i = 0
            while i < (n+1):
                pid = (i + activate) % (n+1)
                if pid != 0:    # since our process starts from 1 (to n)
                    if pStatus[pid] and subcoordinator < pid:
                        subcoordinator = pid
                    print("Election message passed from", pid,
                          ": #Msg", subcoordinator, "\n")
                i += 1

            coordinator = subcoordinator
            display()

        elif tchoice == 3:
            display()

        condition = tchoice != 4


def display():
    """ displays the processes, their status and the coordinator """
    global coordinator
    print('---------------------------------------------')
    print("PROCESS:")
    for i in range(1, n+1):
        print(i, '\t')
    print('\nALIVE:',)
    for i in range(1, n+1):
        print(pStatus[i], "\t")
    print('\n---------------------------------------------')
    print('COORDINATOR IS', coordinator, "\n")
    # print('----------------------------------------------')


if __name__ == '__main__':

    # take_input()

    n = int(input("Enter number of processes: "))
    for i in range(1, n+1):
        print("Enter Process ", i, " is alive or not(0/1): ")
        x = int(input())
        pStatus[i] = x
        if pStatus[i]:
            coordinator = i

    display()
    ring()
