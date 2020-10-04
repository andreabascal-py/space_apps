#!/usr/bin/env python
# coding: utf-8

# In[19]:


import time
from datetime import date, datetime, timedelta
from IPython.display import clear_output
import pandas as p


# In[20]:


#calcular edad
def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


# In[21]:


#determina factor de actividad
def Activity(act):
    if act == 'sedentary' or act.startswith('s'):
        act_ftr= 1.2
    elif act == 'light' or act.startswith('l'):
        act_ftr= 1.375
    elif act == 'moderate' or act.startswith('m'):
        act_ftr= 1.55
    elif act == 'very' or act.startswith('v'):
        act_ftr=1.725
    elif act=='extra' or act.startswith('e'):
        act_ftr=1.9
    return act_ftr
#determina calorias por comida
def meal_cal(Min,Max,cal_needs):
    calories_interval= []
    min_meal= round(Min * cal_needs)
    calories_interval.append(min_meal)
    max_meal= round(Max * cal_needs)
    calories_interval.append(max_meal)
    
    return calories_interval

#calcular calorias necesarias
def cal_Dia(g,w,h,niv):
    if g == 'male'or g.startswith('m'):
        miff_stJ= 10*w +6.25*h -5*age + 5
    elif g== 'female' or g.startswith('f'):
        miff_stJ= 10*w +6.25*h -5*age - 161
    act= Activity(niv)    
    calorie_needs= round(act*miff_stJ)
    
    break_fast= meal_cal(0.25,0.3,calorie_needs)
    morning_snack= meal_cal(0.05,0.1,calorie_needs)
    lunch= meal_cal(.35,.40,calorie_needs)
    afternoon_snack= meal_cal(0.05,0.1,calorie_needs)
    dinner=meal_cal(.15,.20,calorie_needs)
    
    tot_cal=[calorie_needs, break_fast, morning_snack, lunch, afternoon_snack, dinner]
    return tot_cal


# In[22]:



#determina cuanto debes de dormir
def dor (e,horas_act,):
    matr=p.read_excel(r'C:\Users\Andrea\mat.xlsx')
    if e>65:
        e=65      

    mi=matr.iloc[e,1]
    ma=matr.iloc[e,2]
    
    if horas_act<=mi:
        return mi
    elif mi<horas_act<ma:
        d=round(int((mi+ma)/2))
        return d
    elif horas_act>=ma:
        return ma
    

#calcular hora de dormir
def bed_time(wake_time,sleep_time):
    sleep_hours=str(sleep_time)+':00'
    #to calculate difference in time
    global time_diff
    time_diff = datetime.strptime(wake_time, '%H:%M') - datetime.strptime(sleep_hours, '%H:%M')
    time_s=str(time_diff)
    if time_s.startswith('-1'):
        a=time_s[8:13]
        return a
    else:
        a=time_s[:4]
        return a


def sleep_efficiency(t,at,ft):
    Totsleep_time= t*60
    awake_time= at
    fall_astime= ft
    ratio= (Totsleep_time - awake_time - fall_astime)/ (Totsleep_time)
    efficiency= round(ratio,2)*100
    return efficiency

def lightning_ins(wake_time,sleep_time):
    bedtime_=str(sleep_time)
    avoid_light=datetime.strptime(bedtime_, '%H:%M')- datetime.strptime("2:00", '%H:%M')
    sle=wake_time[:-3]
    x=int(sle)+5
    x1=str(x)+':00'
    prioritize_light=datetime.strptime(wake_time, '%H:%M') - datetime.strptime(x1, '%H:%M')
    a1=str(avoid_light)
    a=a1[:-3]
    b1=str(prioritize_light)
    
    if b1.startswith('-1'):
        b=b1[8:-3]
    else:
        b=b1[:4]
    return [a,b]
    


# In[23]:


def clear():
    time.sleep(1.5)
    clear_output(wait=True)    


# In[24]:


#inputs
print('Settings \n')
print('Name')
name= input('Enter your name: ')
gender= input('Female or Male: ').lower()
print('\n')
print('Birthdate')
bd= input('Enter your birthdate DD MM YYYY: ')
print('\n')
print('Weight')
weigth= float(input('Enter your weight [kg]: '))
print('\n')
print('Height')
height= float(input('Enter your height [cm]: '))
print('\n')
print('Activity Factors')
activity= input('How active are you?: Sedentary/Light/Moderate/Very/Extra ').lower()
print('\n')
print('Sleeping Habits')
cd=int(input('How many hours do you sleep?: '))

clear()


date_of_birth = datetime.strptime(bd, "%d %m %Y")
age=int(calculate_age(date_of_birth))
print('Age: ',age)
print('------------------------------------------------------------- \n')  
c=cal_Dia(gender,weigth,height,activity)
print('Daily Caloric Intake: ',c[0],'calories \n')
print('Breakfast recommended caloric intake;', c[1][0],"-",c[1][1],'calories \n')
print('Morning snack recommended caloric intake;', c[2][0],"-",c[2][1],'calories \n')
print('Lunch recommended caloric intake;', c[3][0],"-",c[3][1],'calories \n')
print('Afternoon snack recommended caloric intake;', c[4][0],"-",c[4][1],'calories \n')
print('Dinner recommended caloric intake;', c[5][0],"-",c[5][1],'calories \n')
print('------------------------------------------------------------- \n')                                                       
print('Sleep')
sleep=dor(age,cd)
print(name,'you should sleep', sleep, 'hours.')
wake=input('At what time do you want to wake up? Enter HH:MM  ')
should_sleep=bed_time(wake,sleep)
print('you should go to sleep at: ', should_sleep,'\n')
print('------------------------------------------------------------- \n')  
print("Lightning Instructions")
ins=lightning_ins(wake,should_sleep)
print('You should avoid white and blue light 2 hours before bed.')
print('At the time: ', ins[0] )
print('You should prioritize bright light after you wake up and during work times')
print('Expose yourself to white light to boosting alertness and mood during the times of: ', wake,'-', ins[1])
print('------------------------------------------------------------- \n')  
print('Sleep Efficiency')
fall_asleep=int(input('How many minutes took you to fall asleep?: '))
awake=int(input('How many minutes where you awake during bedtime?: '))
sleep_eff= sleep_efficiency(sleep,awake,fall_asleep)
print('Last night sleep efficiency was:', sleep_eff,'%')

