import numpy as np
import heapq

def light_dark_choice (data, interval_size = 100, repetition = 9, interval_strtl_steps = 4):
    '''
    light_dark_choice
    by: Mahdi Zarei
    06-30-2020
    '''
    var_all = []
    var_all_Interval = []

    interval_light_strtl_val = np.arange(interval_strtl_steps * 2 + 1)*0
    interval_light_strtl_val [1::2 ] = 1
    interval_light_strtl_val = interval_light_strtl_val.tolist()

    interval_dark_strtl_val = np.arange(interval_strtl_steps * 2 + 1)*0
    interval_dark_strtl_val [0::2 ] = 1
    interval_dark_strtl_val = interval_dark_strtl_val.tolist()

    int_st = 0
    int_end = interval_size
    int_size = interval_size
    for int in range(repetition):
        dtmp = data[int_st: int_end]

        var_all.append(np.average(heapq.nlargest(100, dtmp)))
        # --- Check the stimulus transition event; TRan | if avg (%20) is high
        # if np.average(dtmp[:(np.int(len(dtmp)/interval_strtl_steps))]) < \
        #     np.average(dtmp[3:(np.int(len(dtmp)/interval_strtl_steps))]) and \
        if  np.max(dtmp) in dtmp[:(np.int(len(dtmp)/ 4))] and \
        np.average(heapq.nlargest(5, dtmp)) > np.average(heapq.nlargest(np.int(len(data)/2), data)):  #np.max(dtmp) > np.average(heapq.nsmallest(np.int(len(data)-50), data)):
        #np.average(dtmp[:(np.int(len(dtmp)/interval_strtl_steps + 7))]) > \
        #    np.average(dtmp[np.int(len(dtmp)/interval_strtl_steps + 7):]) :
            var_all_Interval.append(1)
        else:
            var_all_Interval.append(0)
        int_st = int_st + int_size
        int_end = int_end + int_size
    response = 'no_response'
    response_tmp = ''
    l_count = 0
    d_count = 0
    mdl_resp = []
    response = []
    for i in np.arange (0,len(var_all)-1,2):
        if var_all [i] > var_all [i+1]:
            mdl_resp.append('D')
            d_count = d_count + 1
        elif var_all [i] < var_all [i+1]:
            mdl_resp.append('L')
            l_count = l_count + 1
        else:
            mdl_resp.append('NR')
    if l_count > d_count and l_count > 1:#+ 1: #and l_count > 2 :
        response = 'Light' #response.append ('Light')
    if d_count > l_count and d_count > 1:#+ 1 : # and d_count > 2:
        response = 'Dark' #response.append ('Dark')
    if var_all_Interval[3::2 ] == interval_light_strtl_val[3::2 ]:
        response = 'transition_light' # response.append ('Light_transition')        
        response_tmp = 'transition_light'
    if var_all_Interval[2::2 ] == interval_dark_strtl_val[2::2 ] :
        response = 'transition_dark' #response.append ('Dark_transition')    
        response_tmp = 'transition_dark'
    if var_all[1] == np.max(var_all) and var_all[1] > var_all[2]+var_all[3]:
        response = 'initial_light' # response.append ('Light_initial')        
    if var_all[0] == np.max(var_all) and var_all[0] > var_all[1]+var_all[2]:
        response = 'initial_dark' # response.append ('Dark_initial')       
    if  response_tmp == 'transition_light'  and response_tmp == 'transition_dark':
        response = 'transition_light_and_transition_dark'
    return response,mdl_resp,var_all

	
