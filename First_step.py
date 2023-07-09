import numpy as np
import pandas as pd
import os

# path = input(" file :")
path="data_run.csv"
processed_data_path=path[:-4]+"__processed__.csv"
mass=60

# while os.path.exists(processed_data_path) :
#     print("The %d file already exists.",processed_data_path)
#     print("continue ? \n 1: yes \n 2: no \n")
#     a =int(input())
#     if a == 1:
#         break
#     elif a==2:
#         path = input(" file :")
#         processed_data_path=path[:-4]+"processed__.csv"

#-----------read information from line 4
data = pd.read_csv(path,skiprows=3)
left_force=data['LT Force (N)']
right_force=data['RT Force (N)']


left_circle=[]
left_start=[]
left_end=[]
stance_left=[]
percent_stance_left=[]
Initial_swing_left=[]
percent_Initial_swing_left=[]
Mid_swing_left=[]
percent_mid_swing_left=[]
Termial_swing_left=[]
percent_termial_swing_left=[]

right_circle=[]
right_start=[]
right_end=[]
stance_right=[]
percent_stance_right=[]
Initial_swing_right=[]
percent_Initial_swing_right=[]
Mid_swing_right=[]
percent_mid_swing_right=[]
Termial_swing_right=[]
percent_termial_swing_right=[]

left_number_cycle=0
right_number_cycle =0

def find_zero(ind_start,arr) :
    i=ind_start
    while arr[i+5]!= 0 :
        if (arr[i+5] >= mass *2 *10):
            while arr[i+5] >= mass *2 *10 :
                i+=5
            range= i -ind_start
            i =ind_start+ range*2
            if (arr[i] ==0):
                while arr[i]==0 :
                    i-=1
                return i+1
        else :
            i+=5
    while arr[i]!=0 :
        i+=1
    return i


# -----------return the index where the force of one of two leg is not equal to 0
def find_not_zero(ind_start, arr):
    i=ind_start
    while(arr[i+4] ==0):
        i+=4
    while arr [i]==0 :
        i+=1
    return i
    # if check_left_right == 0 : # left
    #     i=ind_start
    #     while left_force[i+4] ==0 :
    #         i+=5
    #     while left_force[i]==0 :
    #         i+=1
    #     return i 
    # if check_left_right == 1 : # left
    #     i=ind_start
    #     while right_force[i+4] ==0 :
    #         i+=5
    #     while right_force[i]==0 :
    #         i+=1
    #     return i

#---------------- Find the frame that start the circle----------------

number_frame =1
check_start_left_right =-1 # left 0 ;  right 1
while left_force[number_frame] == 0 and right_force[number_frame] ==0 :
    number_frame +=1
    if left_force[number_frame]!=0 :
        check_start_left_right=0
    elif right_force[number_frame]!= 0 :
        check_start_left_right =1

#------------------------ split part of data ---------------------

# Left

if check_start_left_right ==0 :
    while number_frame<= len(left_force)-100 : #each while  loop will be a cycle of both right and left leg
        left_start.append(number_frame)
        stance_left.append(number_frame)
        left_number_cycle+=1
        left_circle.append(left_number_cycle)                            # add number of cycle        
        

        # finish stance phase and start initial swing in left leg - termial swing right
        zero_left=find_zero(number_frame, left_force)
        Initial_swing_left.append(zero_left)
        if(right_number_cycle!=0):
            Termial_swing_right.append(zero_left)                       # Initial left = terminal right
        number_frame =zero_left                                     # change the number of frame                               

        # Finish initial swing (left) start mid swing left - stance right
        start_right= find_not_zero(number_frame, right_force)       # move to find on right side
        number_frame=start_right
        Mid_swing_left.append(number_frame)
        stance_right.append(number_frame)
        right_start.append(number_frame)
        if(right_number_cycle !=0 ):
            right_end.append (number_frame-1)
        right_number_cycle+=1
        right_circle.append(right_number_cycle)

        #Finish the Midswing (left)- finish the stance (right) -start the  termial swing  (left)  and initial swing (right)
        start_terminal_swing = find_zero(number_frame, right_force)
        number_frame= start_terminal_swing
        Termial_swing_left.append(start_terminal_swing)                 
        Initial_swing_right.append(start_terminal_swing)            # Termial left = Initial right

        #Finish the terminal swing (left) - start the stance left and mid swing right
        start_new_circle= find_not_zero(number_frame,left_force)
        number_frame=  start_new_circle
        Mid_swing_right.append(start_new_circle)
        left_end.append(number_frame-1)
    right_circle.pop()
    right_start.pop()
    stance_right.pop()
    Initial_swing_right.pop()
    Mid_swing_right.pop()
    for i in range(len(left_circle)):
        total_frame=left_end[i]-left_start[i]
        percent_stance_left.append((Initial_swing_left[i]-stance_left[i])/total_frame)
        percent_Initial_swing_left.append((Mid_swing_left[i]-Initial_swing_left[i])/total_frame)
        percent_mid_swing_left.append((Termial_swing_left[i]-Mid_swing_left[i])/total_frame)
        percent_termial_swing_left.append((left_end[i]-Termial_swing_left[i])/total_frame)
    for i in range(len(right_circle)):
        total_frame=right_end[i]-right_start[i]
        percent_stance_right.append((Initial_swing_right[i]-stance_right[i])/total_frame)
        percent_Initial_swing_right.append((Mid_swing_right[i]-Initial_swing_right[i])/total_frame)
        percent_mid_swing_right.append((Termial_swing_right[i]-Mid_swing_right[i])/total_frame)
        percent_termial_swing_right.append((right_end[i]-Termial_swing_right[i])/total_frame)
elif check_start_left_right==1 : # right
    while number_frame<= len(left_force)-100 : #each while  loop will be a cycle of both right and left leg
        right_start.append(number_frame)
        stance_right.append(number_frame)
        right_number_cycle+=1
        right_circle.append(right_number_cycle)                            # add number of cycle        
        

        # finish stance phase and start initial swing in left leg - termial swing right
        zero_right=find_zero(number_frame, right_force)
        Initial_swing_right.append(zero_right)
        if (left_number_cycle !=0 ):
            Termial_swing_left.append(zero_right)                       # Initial left = terminal right
        number_frame =zero_right                                     # change the number of frame                               

        # Finish initial swing (left) start mid swing left - stance right
        start_left= find_not_zero(number_frame, left_force)       # move to find on right side
        number_frame=start_left
        Mid_swing_right.append(number_frame)
        stance_left.append(number_frame)
        left_start.append(number_frame)
        if(left_number_cycle !=0 ):
            left_end.append (number_frame-1)
        left_number_cycle+=1
        left_circle.append(left_number_cycle)
        

        #Finish the Midswing (left)- finish the stance (right) -start the  termial swing  (left)  and initial swing (right)
        start_terminal_swing = find_zero(number_frame, left_force)
        number_frame= start_terminal_swing
        Termial_swing_right.append(start_terminal_swing)                 
        Initial_swing_left.append(start_terminal_swing)            # Termial left = Initial right

        #Finish the terminal swing (left) - start the stance left and mid swing right
        start_new_circle= find_not_zero(number_frame,right_force)
        number_frame=  start_new_circle
        Mid_swing_left.append(start_new_circle)
        right_end.append(number_frame-1)    
        # print(right_circle[-1],right_start[-1], right_end[-1], stance_right[-1], Initial_swing_right[-1], Mid_swing_right[-1],Termial_swing_right[-1])
        # print(len(left_circle),len(left_start),len(left_end),len(stance_left),len(Initial_swing_left),len(Mid_swing_left),len  (Termial_swing_left))
        # print(right_circle[-1],right_start[-1], right_end[-1], stance_right[-1], Initial_swing_right[-1], Mid_swing_right[-1],Termial_swing_right[-1])
        # if len(left_end) >0 :
        #     print(left_circle[-1],left_start[-1], left_end[-1], stance_left[-1], Initial_swing_left[-1], Mid_swing_left[-1],Termial_swing_left[-1])
    # print(len(right_circle),len(right_start),len(right_end),len(stance_right),len(Initial_swing_right),len(Mid_swing_right),len  (Termial_swing_right))
    left_circle.pop()
    left_start.pop()
    stance_left.pop()
    Initial_swing_left.pop()
    Mid_swing_left.pop()


    for i in range(len(left_circle)):
        total_frame=left_end[i]-left_start[i]
        percent_stance_left.append((Initial_swing_left[i]-stance_left[i])/total_frame)
        percent_Initial_swing_left.append((Mid_swing_left[i]-Initial_swing_left[i])/total_frame)
        percent_mid_swing_left.append((Termial_swing_left[i]-Mid_swing_left[i])/total_frame)
        percent_termial_swing_left.append((left_end[i]-Termial_swing_left[i])/total_frame)
    for i in range(len(right_circle)):
        total_frame=right_end[i]-right_start[i]
        percent_stance_right.append((Initial_swing_right[i]-stance_right[i])/total_frame)
        percent_Initial_swing_right.append((Mid_swing_right[i]-Initial_swing_right[i])/total_frame)
        percent_mid_swing_right.append((Termial_swing_right[i]-Mid_swing_right[i])/total_frame)
        percent_termial_swing_right.append((right_end[i]-Termial_swing_right[i])/total_frame)
    
data_out_right={"Right cycle":right_circle, "Right start":right_start , "Right end" : right_end, 
          "Stance right " :stance_right,"percent_stance_right":percent_stance_right  ,
          "Initial swing right" : Initial_swing_right,"Percent initial right" :percent_Initial_swing_right ,
          "Mid swing right": Mid_swing_right, "Percent mid swing right ":percent_mid_swing_right,
          "Terminal right" : Termial_swing_right , "Percent termial right": percent_termial_swing_right,}
data_out_left={
          "Left cycle" : left_circle , "Left start" : left_start , "Left end" : left_end,
          "Stance left": stance_left, "percent_stance_left":percent_stance_left,
        "Initial swing left" : Initial_swing_left,"Percent initial left" :percent_Initial_swing_left ,
          "Mid swing left": Mid_swing_left, "Percent mid swing left ":percent_mid_swing_left,
          "Terminal left" : Termial_swing_left , "Percent termial left": percent_termial_swing_left}

df=pd.DataFrame(data_out_right)
df.to_csv(processed_data_path, index=False)






# if check_start_left_right ==0 :
#     check_left_right =0 
#     while number_frame <= len(left_force)-100 :
#         start.append(number_frame)
#         if check_left_right == 0:
#             stance_left.append(number_frame)
#             After_flight_right.append(number_frame)
#             zero_left = find_zero( number_frame , left_force) # finnish stance phase of the left leg and start the flight phase
#             number_frame=zero_left
#             Flight_left.append(zero_left)
#             check_left_right=1
#         # Find the frame that finish the  Flight left phase by finding the start stancing phase of right leg 
#         start_right = find_not_zero(number_frame , check_left_right)
#         number_frame =start_right
#         if check_left_right ==1 :
#             stance_right.append(number_frame)
#             After_flight_left.append(number_frame)
#             zero_right= find_zero(number_frame, right_force) # finnish stance phase  of the right leg and start the different flight phase
#             number_frame =zero_right
#             Flight_right.append(zero_right)
#             check_left_right =0
#         # Find the frame that finish the  Flight right phase by finding the start stancing phase of left leg 
#         start_left =find_not_zero(number_frame ,check_left_right)
#         number_frame = start_left
#         end.append(number_frame-1)
#         total=end[-1]-start[-1]+1
#         percent_stance_right.append((Flight_right[-1]-stance_right[-1]-1)/total)
#         percent_flight_right.append((After_flight_right[-1]-Flight_right[-1])/total)
#         percent_after_flight_right.append((end[-1]-After_flight_right[-1])/total)
#         percent_stance_left.append((Flight_left[-1]-stance_left[-1]-1)/total)
#         percent_flight_left.append((After_flight_left[-1]-Flight_left[-1])/total)
#         percent_after_flight_left.append((end[-1]-After_flight_left[-1])/total)
#         cycle_number+=1
#         cycle.append(cycle_number)
# #right
# if check_start_left_right ==1 :
#     check_left_right =1 
#     while number_frame <= len(left_force)-70 :
#         start.append(number_frame)
#         if check_left_right ==1 :
#             stance_right.append(number_frame)
#             After_flight_left.append(number_frame)
#             zero_right= find_zero(number_frame, right_force) # finnish stance phase  of the right leg and start the different flight phase
#             number_frame =zero_right
#             Flight_right.append(zero_right)
#             check_left_right =0
#         # Find the frame that finish the  Flight right phase by finding the start stancing phase of left leg 
#         start_left =find_not_zero(number_frame ,check_left_right)
#         number_frame = start_left
#         if check_left_right == 0:
#             stance_left.append(number_frame)
#             After_flight_right.append(number_frame)
#             zero_left = find_zero( number_frame , left_force) # finnish stance phase of the left leg and start the flight phase
#             number_frame=zero_left
#             Flight_left.append(zero_left)
#             check_left_right=1
#         # Find the frame that finish the  Flight left phase by finding the start stancing phase of right leg 
#         start_right = find_not_zero(number_frame , check_left_right)
#         number_frame =start_right
#         end.append(number_frame-1)
#         total=end[-1]-start[-1]+1
#         percent_stance_right.append((Flight_right[-1]-stance_right[-1]-1)/total)
#         percent_flight_right.append((After_flight_right[-1]-Flight_right[-1])/total)
#         percent_after_flight_right.append((end[-1]-After_flight_right[-1])/total)
#         percent_stance_left.append((Flight_left[-1]-stance_left[-1]-1)/total)
#         percent_flight_left.append((After_flight_left[-1]-Flight_left[-1])/total)
#         percent_after_flight_left.append((end[-1]-After_flight_left[-1])/total)
#         cycle_number+=1
#         cycle.append(cycle_number)
        

# print(len(cycle)," ", len(start), " ", len(end), " " , len(stance_right))


# data_out={"cycle":cycle, "start":start , "end" : end, 
#           "Stance right " :stance_right,"percent_stance_right":percent_stance_right  ,
#           "Flight_right" : Flight_right,"percent_flight_right" :percent_flight_right ,
#           "After flight right": After_flight_right, "percent_after_flight_right ":percent_after_flight_right,
#           "Stance left": stance_left, "percent_stance_left":percent_stance_left,
#           "Flight left" : Flight_left ,"percent_flight_left" : percent_flight_left,
#             "After flight left ": After_flight_left ,"percent_after_flight_left" :percent_after_flight_left}

# df=pd.DataFrame(data_out)
# df.to_csv(processed_data_path, index=False)
# output_path = "output.csv"


