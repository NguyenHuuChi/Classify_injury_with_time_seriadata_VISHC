import pandas as pd
import matplotlib.pyplot as plt
import csv
from datetime import datetime
import linecache
import numpy as np
import seaborn as sns

# a="Hello.sdfg"
# print(a[:len(a)-5])

# Function read the file contain specific time
def read_file_time(path, start ,end) :
    if(path[-4:] == "xlsx"):
        new_path=path[:len(path)-4]+"csv"
        read_file=pd.read_excel(path)
        read_file.to_csv(new_path, index= None, header=True)
        with open(new_path) as file_obj :
            read_obj= csv.reader(file_obj)
            interestingrows=[row for idx, row in enumerate(read_obj) if idx in range(start,end)]
            return interestingrows
    elif (path[-3:]=='csv') :
        with open(path) as file_obj:
            read_obj=csv.reader(file_obj)
            interestingrows=[row for idx, row in enumerate(read_obj) if idx in range(start,end)]
            return interestingrows

data= read_file_time("2023-06-14-11-02_Treadmill_9-11kph.xlsx",1,11) # read from line 2 to line 11

# Find where contain time in file
def read_time(data):
    index=0
    while(index < len(data[0])-1) :
        if len(data[0][index])==0:
            index+=1
            continue
        elif data[0][index][-1]== "Z" and data[0][index][0]=="2" :
            break
        index +=1
    standard_time=[]
    for i in range(len(data)):
        standard_time.append(data[i][index])
    return standard_time
a=read_time(data)
# print(a)

# first_timestamp = datetime.fromisoformat(a[0])
# print(first_timestamp)
# from datetime import datetime


# calculate the time difference 
def calculate_time_differences(timestamps):
    first_timestamp = datetime.fromisoformat(timestamps[0].replace("Z", ""))
    time_diffs = []

    for timestamp in timestamps[2:]:
        if timestamp:
            current_timestamp = datetime.fromisoformat(timestamp.replace("Z", ""))
            time_diff = int((current_timestamp - first_timestamp).total_seconds()*100)
            time_diffs.append(time_diff)

    return time_diffs

different_time=calculate_time_differences(a)
# print(different_time)

#----------------Read data angle ------------------------------------------
# Check if it can transfer to interger
def check_number(string):
    try:
        number = float(string)
        return True
    except:
        return False
# ----Transfer elements of an array from string to float----------------
def change_to_number(arr):
    arr_number=[float(element) for element in arr]  
    return arr_number
#----------------scalse and interpolate --------------------------
def interp_sampling(arr, total_frames):
    return np.interp(
        np.linspace(0,1.0,total_frames), 
        np.linspace(0,1.0,len(arr)),
        arr
    )

#function read specific row in csv file
def read_specific_rows(filename, row_indices):

    with open(filename, 'r') as file:
        row = linecache.getline(filename, row_indices)
        row.strip()
        row=row.split(',')
    return row

class Read_data_runing:
    def __init__(self,file_path):
        self.Model_output=[] # ---------first element is index in column, second is start frame , third is the end frame---------------------
        self.Trajectory=[]
        self.file_path=file_path
        self.Name_of_angle=read_specific_rows(self.file_path,3)
        self.estimate_the_start_frame()


    #-------------------- Read the data and Find the frame where to start-------------------------
    def estimate_the_start_frame(self,skiprow=3):
        # print(self.file_path)
        self.data_frame = pd.read_csv(self.file_path,skiprows=skiprow)
        
        
        Frame=self.data_frame["Frame"]
        self.Model_output.append(1)
        self.Model_output.append(int(Frame[1]))
        i=1

        #-------------------Find where Model_output finish--------------------------------
        while  i<len(Frame) : 
            if not check_number(Frame[i]):
                break
            i+=1
        self.Model_output.append(int(Frame[i-1]))
        while i<len(Frame):
            if(Frame[i]=="Frame"):
                break
            i+=1
        self.Trajectory.append(i+2)
        self.Trajectory.append(int(Frame[i+2]))
        self.Trajectory.append(int(Frame[len(Frame)-1]))
        self.Column_name=self.data_frame.columns
        # print(self.Column_name)
        # print(self.Trajectory,self.Model_output)
    def read_specific_columns(self,name_column):
        a=0

        #------------find the angle-----------------------------
        for angle in self.Name_of_angle :

            if len(angle) >0:
                if "LKneeAngles" in angle :
                    a+=2
                    break
                else :
                    a+=1
        a-=8
        if a>0 :
            name_column="X."+str(a)
        else :
            name_column="X"
        # print(name_column)
        columna= self.data_frame[name_column]
        
        # ----------------------------Split part Model output and Trajectory------------------------
        Model_ouput_co=columna[self.Model_output[0]:self.Model_output[2]-self.Model_output[1]+self.Model_output[0]+1]
        Trajectory_co=columna[self.Trajectory[0]:self.Trajectory[2]-self.Trajectory[1]+self.Trajectory[0]+1]

        return Model_ouput_co, Trajectory_co

        

path_03="TuanAnhRunning04.csv"
path3=Read_data_runing(path_03)
Model03,Trajec03=path3.read_specific_columns("X.1")
Dif_model_out=path3.Model_output

#------------------determine the start and finish points of running file in the  force file---------------
start_frame03=different_time[4]+Dif_model_out[1]
end_frame03=different_time[4]+Dif_model_out[2]
# print(start_frame03,end_frame03)

data_run_left=pd.read_csv("data_run__left_leg_processed__.csv")
left_start=data_run_left["Left start"]
left_end=data_run_left["Left end"]
percent_stance_left=data_run_left['percent_stance_left']
Percent_initial_left=data_run_left["Percent initial left"]
Percent_Mid_swing_left =data_run_left["Percent mid swing left "]
Percent_Termial_left =data_run_left["Percent termial left"]

cycle=0
while(cycle < len(left_start)):
    if (left_start[cycle] > start_frame03):
        begin_cycle=cycle-1
        break
    cycle+=1
while (cycle < len(left_end)):
    if(left_end[cycle]> end_frame03):
        final_cycle=cycle-1
        break
    cycle+=1


# ------------------split cycle in Model--------------
# print(begin_cycle,"begin")
# print(final_cycle)
information_cycle=[]
phase_split_line=[]
for cycle in range(begin_cycle,final_cycle):
    split_line=[]
    information=[]
    information.append(left_start[cycle]-start_frame03)
    information.append(left_end[cycle]-start_frame03)

    split_line.append(percent_stance_left[cycle]*100)
    split_line.append(Percent_initial_left[cycle]*100+split_line[-1]) # the index of the phase must add with the previous point
    split_line.append(Percent_Mid_swing_left[cycle]*100+split_line[-1])
    # split_line.append(Percent_Termial_left[cycle]*100+split_line[-1])
    
    information_cycle.append(information)
    phase_split_line.append(split_line)
# print(information_cycle)

data_cycle=[]
for cycle in information_cycle:
    data=Model03[cycle[0]:cycle[1]+1]
    data_cycle.append(data)

#-----------------------interpolate data--> 100% :-----------------------
print(data_cycle, len(data_cycle))
def inter_shampe_many_data(data_cycle):
    inter_data_cycle=[]
    for cycle in data_cycle :
        number_cy= change_to_number(cycle)
        inter_sham=interp_sampling(number_cy,100)
        inter_data_cycle.append(inter_sham)
    return inter_data_cycle

inter_data_cycle=inter_shampe_many_data(data_cycle)

def plot_average_with_error(inter_data_cycle,information_cycle):

    average_split_cycle = np.mean(information_cycle, axis=0)
    std_error_split_cycle = np.std(information_cycle, axis=0)    

    # print(average_split_cycle)
    # print(std_error_split_cycle)

    # Calculate the average and standard error
    average = np.mean(inter_data_cycle, axis=0)
    std_devi = np.std(inter_data_cycle, axis=0) 
    # Create x-axis values
    x = np.arange(len(average))

    # Plot the average with shaded standard error using Seaborn
    plt.figure(figsize=(8, 6))
    for i, a in enumerate(average_split_cycle):
        plt.axvline(x=a , color='red', linestyle='-')
        plt.text(a , average_split_cycle[i ] + std_error_split_cycle[i ], f'{average_split_cycle[i ]:.1f} ± {std_error_split_cycle[i ]:.1f}', color='red', ha='center')
        plt.fill_between([average_split_cycle[i] - std_error_split_cycle[i ], average_split_cycle[i ] + std_error_split_cycle[i ]], [a, a], color='red', alpha=0.4)
    sns.lineplot(x=x, y=average, color='blue', label='Average')
    plt.fill_between(x, average - std_devi, average + std_devi, color='red', alpha=0.4, label='Standard deviation')
    plt.xlabel('Percent cycle')
    plt.ylabel('Angle (degree)')
    plt.title('Average with Standard Error')
    plt.legend()
    plt.show()

plot_average_with_error(inter_data_cycle,phase_split_line)

