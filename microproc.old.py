import subprocess
import sys

permastart = int(sys.argv[1])
interval = 5
num_instances = 10

for batch in range(1, num_instances+1):
    processes = []
    for i in range(1, interval + 1):
        
        start = (permastart + (i-1)*interval*num_instances)
        end = start + interval
        print(f'{start}-{end}');
        # print(f"Batch {batch+1} of instances has finished.");
        continue
    
        # print(start)
        cmd = f"python pexurls.py {start} {end}"  # command to run the script with start and end arguments
        p = subprocess.Popen(cmd, shell=True)  # create a process object for the command
        processes.append(p)  # add the process object to the list of processes

    # wait for all the processes to finish
    for p in processes:
        p.wait()

    print(f"Batch {batch+1} of instances has finished.")
    if(batch == 6):
        break
