import numpy as np

'''
- Tail event detection
-- Parameters
>> tail_dta , event_idx, event_threshold 
-- Return
>> Detected event
By: Mahdi Zarei: 09-16-20
'''
def event_count (tail_dta , event_type,  event_idx, event_interval_threshold = 200, scale_Flp_Strgl = 20, move_time_threshold = 40):    
    event_turn= []    
    event_turn_right = []
    event_turn_left = []
    event_struggle = []
    event_move = []
    
    event_turn_idx = []
    event_turn_right_idx = []
    event_turn_left_idx = []    
    event_struggle_idx = []
    event_move_idx = []      

    flg_event = 0 
    flg_non_event = 0
    st_non_event = 0
    en_non_event = 0
    event_count = 0    
    en_F = 0
    for i in range (len(tail_dta)):    
        if i in event_idx:                            
            if flg_event == 0:
                flg_event = 1
                if flg_non_event == 1:                
                    if en_non_event - st_non_event > event_interval_threshold:
                        if event_count > 0:    
                            sub_dta = tail_dta[st_F:en_F]
                            if event_type == 'turn_struggle':
                                sub_dts_l_N = len([sub_dta[t] for t in range(len(sub_dta)//2) if sub_dta[t]<0])
                                sub_dts_l_P = len([sub_dta[t] for t in range(len(sub_dta)//2) if sub_dta[t]>0])
                                sub_dts_u_N = len([sub_dta[t] for t in range(len(sub_dta)//2) if sub_dta[t]<0])
                                sub_dts_u_P = len([sub_dta[t] for t in range(len(sub_dta)//2) if sub_dta[t]>0])
                                sub_dts_size_NP = len([sub_dta[t] for t in range(len(sub_dta)) if np.abs(sub_dta[t])>15])                                
                                if (sub_dts_l_N > scale_Flp_Strgl and sub_dts_u_P > scale_Flp_Strgl) or\
                                (sub_dts_l_P > scale_Flp_Strgl and sub_dts_u_N > scale_Flp_Strgl) :
                                    event_struggle.append ([st_F,en_F])                                
                                    event_struggle_idx.append(st_F)                                
#                                 elif len([sub_dta[t] for t in range(len(sub_dta)) if np.abs(sub_dta[t])>0]) > scale_Flp_Strgl:
#                                     sub_dts_l_N > scale_Flp_Strgl or \
#                                     sub_dts_l_P > scale_Flp_Strgl or \
#                                     sub_dts_u_N > scale_Flp_Strgl or \
#                                     sub_dts_u_P > scale_Flp_Strgl:
                                else:
                                    event_turn.append ([st_F,en_F])
                                    event_turn_idx.append(st_F)
                                    if len(sub_dta) > 0:                
                                        if np.max (sub_dta) >= -np.min (sub_dta):
                                            event_turn_right.append ([st_F,en_F])
                                            event_turn_right_idx.append(st_F)
                                        elif np.min (sub_dta) < -np.max (sub_dta):
                                            event_turn_left.append ([st_F,en_F])
                                            event_turn_left_idx.append(st_F)                                    
                
                            elif event_type == 'move':
                                if len(sub_dta) > move_time_threshold:
                                    event_move.append ([st_F,en_F])
                                    event_move_idx.append(st_F)
                        event_count = event_count + 1
                        st_F = i   
                    flg_non_event = 0
            else:
                en_F = i
        else:
            en_non_event = i
            if flg_non_event == 0:
                st_non_event = i
                flg_non_event = 1
                flg_event = 0
    if event_type == 'turn_struggle':
        output = [event_turn, event_turn_idx,event_turn_right, event_turn_right_idx, event_turn_left, event_turn_left_idx, event_struggle, event_struggle_idx]
    elif event_type == 'move':
        output = [event_move, event_move_idx]
    return output
'''
- Decomposition the tail movement curve into THREE subclasses
-- Parameters
>> tail_dta: "array of the angles value" , 
    offset: "event interval size" , 
    scale: "Maximum foreward angles size" , 
    scale_flip: "Maximum flip angles size ??"
>> tail_dta_MOVE_idx, tail_dta_STRUGGLE_idx, tail_dta_FLIP_idx:  "3 subsets of the tail movement data" 
By: Mahdi Zarei: 09-10-20
'''
    
def tail_movement_CLASS (tail_dta , scale_move = 20, event_interval_thre = 200, scale_turn_Strgl = 20):
    tail_dta_MOVE = {}
    tail_dta_MOVE ['idx'] = []
    tail_dta_Flp_Strgl = {}
    tail_dta_Flp_Strgl ['idx'] = []
    tail_dta_Flp_Strgl ['angle'] = []    
    for t in range(len(tail_dta)):
        if np.abs(tail_dta[t] )> 5:
            if np.abs(tail_dta[t] )<= scale_move:
                tail_dta_MOVE ['idx'].append(t)            

            elif np.abs(tail_dta[t]) > scale_move :
                tail_dta_Flp_Strgl['idx'].append(t)
                tail_dta_Flp_Strgl['angle'].append(tail_dta[t])
    tail_dta_Flp_Strgl['idx'].append(t)
    tail_dta_Flp_Strgl['angle'].append(tail_dta[t])                
    event_TYPE = ['move' , 'turn_struggle']
    event_move, event_move_idx = event_count (tail_dta , 
                              event_type = event_TYPE[0] ,
                              event_idx = tail_dta_MOVE ['idx'], 
                              event_interval_threshold = event_interval_thre)
    
    event_turn, event_turn_idx, event_turn_right, event_turn_right_idx,event_turn_left, event_turn_left_idx, event_struggle, event_struggle_idx = event_count (tail_dta , 
                                                                                  event_type = event_TYPE [1] ,
                                                                                  event_idx = tail_dta_Flp_Strgl ['idx'], 
                                                                                  event_interval_threshold = event_interval_thre,
                                                                                  scale_Flp_Strgl = scale_turn_Strgl)
    
    return np.asarray(event_move), np.asarray(event_move_idx) , \
        np.asarray(event_turn), np.asarray(event_turn_idx),\
np.asarray(event_turn_right), np.asarray(event_turn_right_idx),\
np.asarray(event_turn_left), np.asarray(event_turn_left_idx),\
np.asarray(event_struggle), np.asarray(event_struggle_idx)                                                          
    
    

'''
Rescaling and interpolating  dff
'''

def rescale(sig, sig_size , extend_size):
    n = len(sig)
    return np.interp(np.linspace(0, sig_size, extend_size), np.arange(n), sig)


'''
This function removes the overlaped events and the related indices and extends the original event
by: Mahdi Zarei: 09-25-2020
'''
def source_target_hit (tail_dta , event_source, event_source_idx, event_target, event_target_idx, effect_size = 100 ):
    mached_sor_tar = []    
    for s_idx in range(len(event_source)):
        s = event_source [s_idx]
        s_interval = np.arange (s[0]-effect_size, s[1]+effect_size)
        mached_sor_tar_idx = 0
        for t_idx in range(len(event_target)):
            t = event_target [t_idx]
            t_interval = np.arange (t[0], t[1])
            if len(set(s_interval) & set(t_interval) ) > 0:
                mached_sor_tar.append(mached_sor_tar_idx)                
                event_source [s_idx][0] = np.minimum (s[0], t[0] )
                event_source [s_idx][1] = np.maximum (s[1], t[1])
                event_source_idx = np.hstack ([ np.asarray (event_source_idx), t_idx])
                
            mached_sor_tar_idx = mached_sor_tar_idx + 1       
    event_target = np.delete(event_target,mached_sor_tar, 0)
    event_target_idx = np.delete(event_target_idx,mached_sor_tar, 0)
    return event_source , event_source_idx, event_target, event_target_idx, mached_sor_tar 


'''
Number of events for each stimulus (light or dark)
by: Mahdi Zarei; 09-26-2020
'''
def event_condition_count(event_idx, input_time_interval, no_inputs, stim):
    event_count = []
    if stim == 'light':
        for sc in range(1,no_inputs,2):
            event_count.append (len([i for i in range(len(event_idx)) if event_idx[i]>=input_time_interval*sc\
                        and event_idx[i]<=input_time_interval*(sc+1)]))
    else:
        for sc in range(0,no_inputs,2):
            event_count.append (len([i for i in range(len(event_idx)) if event_idx[i]>input_time_interval*sc\
                        and event_idx[i]<input_time_interval*(sc+1)]))    
    return event_count

	
def stats_event_condition_count (event_X_idx, input_time_interval):
    event_cnd_count_L = []
    event_cnd_count_D = []
    for e in range(4):    
        event_cnd_count_L.append (event_condition_count (event_X_idx[e], input_time_interval,no_inputs = 9, stim= 'light'))       
        event_cnd_count_D.append (event_condition_count (event_X_idx[e], input_time_interval,no_inputs = 9, stim= 'dark')       )
    return event_cnd_count_L, event_cnd_count_D


def tail_mv_TO_events (tail_dta):
    # >> Tail signal decomposition ...
    # event_move, event_move_idx , event_turn, event_turn_idx, event_struggle, event_struggle_idx = \
    # tail_movement_CLASS (tail_dta, scale_move = 15, event_interval_thre = 25, scale_turn_Strgl = 15)
    
    event_move, event_move_idx , event_turn, event_turn_idx, event_turn_right, event_turn_right_idx,event_turn_left, event_turn_left_idx, \
        event_struggle, event_struggle_idx = tail_movement_CLASS (tail_dta, scale_move = 20, event_interval_thre = 200, scale_turn_Strgl = 20)
        
        

    event_turn, event_turn_idx , event_move, event_move_idx, mached_sor_tar =\
    source_target_hit (tail_dta, event_turn , event_turn_idx, event_move, event_move_idx, effect_size = 100)

    event_struggle , event_struggle_idx  , event_move, event_move_idx, mached_sor_tar =\
    source_target_hit (tail_dta, event_struggle , event_struggle_idx,  event_move, event_move_idx, effect_size = 100)
    
    #event_struggle , event_struggle_idx, event_turn, event_turn_idx, mached_sor_tar =\
    #source_target_hit (tail_dta, event_struggle ,event_struggle_idx,  event_turn, event_turn_idx, effect_size = 10 )               
    

    # Turn RIGHT source_target_hit <<<<
    event_turn_right, event_turn_right_idx , event_move, event_move_idx, mached_sor_tar =\
    source_target_hit (tail_dta, event_turn_right , event_turn_right_idx, event_move, event_move_idx, effect_size = 100)
	
    # Assigning the turn evens that happens immediately before or after struggle to struggle
    event_struggle , event_struggle_idx, event_turn_right, event_turn_right_idx, mached_sor_tar =\
    source_target_hit (tail_dta, event_struggle ,event_struggle_idx,  event_turn_right, event_turn_right_idx, effect_size = 100)           
                       
    # Turn LEFT source_target_hit
    event_turn_left, event_turn_left_idx , event_move, event_move_idx, mached_sor_tar =\
    source_target_hit (tail_dta, event_turn_left , event_turn_left_idx, event_move, event_move_idx, effect_size = 100)
    
    event_struggle , event_struggle_idx, event_turn_left, event_turn_left_idx, mached_sor_tar =\
    source_target_hit (tail_dta, event_struggle ,event_struggle_idx,  event_turn_left, event_turn_left_idx, effect_size = 100 )           
    
    
    # outputs
    # event_intervals = [event_struggle , event_turn, event_move]
    # event_idx = [event_struggle_idx , event_turn_idx, event_move_idx]
    
    event_intervals = {'event_struggle':event_struggle ,
                       'event_turn':event_turn, 
                       'event_turn_right': event_turn_right,
                       'event_turn_left': event_turn_left,
                       'event_move':event_move}
    
    event_idx = {'event_struggle_idx':event_struggle_idx , 
                 'event_turn_idx':event_turn_idx,
                 'event_turn_right_idx':event_turn_right_idx,
                 'event_turn_left_idx':event_turn_left_idx,                 
                 'event_move_idx':event_move_idx}
    
    return event_intervals, event_idx


# - - - - - - - - - - - - - - - - - - - - - - - -  #
#              Get some statistics                 #
# - - - - - - - - - - - - - - - - - - - - - - - -  #
def event_condition_count__LD_transition(event_idx, input_time_interval, no_inputs, stim):
    '''
    Remove first dark interval; first_dark =  2 
    Whole time interval ; first_dark =  0    
    '''
    first_dark = 0    
    event_count_20per = []
    event_count_100per = []
    if stim == 'light_transition':
        for sc in range(1,no_inputs,2):
            event_count_20per.append (len([i for i in range(len(event_idx)) if event_idx[i]>=input_time_interval*sc\
                        and event_idx[i] < (input_time_interval*sc + input_time_interval*0.2)]))
        for sc in range(1,no_inputs,2):
            event_count_100per.append (len([i for i in range(len(event_idx)) if event_idx[i]>=input_time_interval*sc\
                        and event_idx[i] < (input_time_interval*sc + input_time_interval)]))
            
    else:
        for sc in range(first_dark,no_inputs,2):
            event_count_20per.append (len([i for i in range(len(event_idx)) if event_idx[i]>=input_time_interval*sc\
                        and event_idx[i] < (input_time_interval*sc + input_time_interval*0.2)]))    
        for sc in range(first_dark,no_inputs,2):
            event_count_100per.append (len([i for i in range(len(event_idx)) if event_idx[i]>=input_time_interval*sc\
                        and event_idx[i] < (input_time_interval*sc + input_time_interval)]))    
            
    return event_count_20per, event_count_100per

def stats_event_condition_count__LD_transition (event_X_idx, input_time_interval):
    event_cnd_count_L_20 = []
    event_cnd_count_L_100 = []
    
    event_cnd_count_D_20 = []
    event_cnd_count_D_100 = []
    
    # events = {'event_struggle_idx', 'event_turn_right_idx', 'event_turn_left_idx', 'event_move_idx'}    
    events = ['event_struggle_idx', 'event_turn_right_idx', 'event_turn_left_idx', 'event_move_idx']    
    for e in events:
        event_cnd_count_L_20.append (event_condition_count__LD_transition (event_X_idx[e], input_time_interval,no_inputs = 9, stim= 'light_transition')[0])       
        event_cnd_count_L_100.append (event_condition_count__LD_transition (event_X_idx[e], input_time_interval,no_inputs = 9, stim= 'light_transition')[1])       
        
        event_cnd_count_D_20.append (event_condition_count__LD_transition (event_X_idx[e], input_time_interval,no_inputs = 9, stim= 'dark_transition')[0])
        event_cnd_count_D_100.append (event_condition_count__LD_transition (event_X_idx[e], input_time_interval,no_inputs = 9, stim= 'dark_transition')[1])
    return event_cnd_count_L_20, event_cnd_count_L_100, event_cnd_count_D_20, event_cnd_count_D_100



# - - - - - - - - - - - - - - - - - - - - - - - -  #
#                  PLOTS                           #
# - - - - - - - - - - - - - - - - - - - - - - - -  #
import matplotlib.pyplot as plt

def plot_ld_stimuli (tail_dta, ax, input_time_interval, no_inputs):
    int_st = 0
    int_end = input_time_interval
    int_size = input_time_interval*2
    for int in range(no_inputs):
        ax.axvspan(int_st, int_end, facecolor='#818581', alpha=0.5)
        int_st = int_st + int_size
        int_end = int_end + int_size    
    ax.set_xlim ([0, len(tail_dta)])



def plot_tail_events( tail_dta, event_X_idx, fileName, fileaddr):        
    
    figl = plt.figure (figsize= (20,12))
    ax = figl.add_subplot (5,1, 1) 
    ax.plot(tail_dta)
    ax.set_title ('Tail movement' ,color='b', fontsize = 17)
    ax.tick_params (axis='y', colors='b'), ax.tick_params (axis='x', colors='b')
    ax.set_ylim ([-100, 100]), ax.grid(linestyle='--', linewidth='0.5', color='red')
    ax.set_xlim ([0, len(tail_dta)]),ax.set_ylabel ('Angle', fontsize = 17 , color ='b')
    plot_ld_stimuli (tail_dta, ax , input_time_interval= len(tail_dta)/9, no_inputs=5 )
    
    ax = figl.add_subplot (5,1, 2)
    ax.plot(tail_dta)
    ax.plot(event_X_idx['event_turn_right_idx'], tail_dta[event_X_idx['event_turn_right_idx']], 'o', color = '#fabe64')
    ax.set_title ('Turns right' ,color='b', fontsize = 17)
    ax.tick_params (axis='y', colors='b'), ax.tick_params (axis='x', colors='b')
    ax.set_ylim ([-100, 100]), ax.grid(linestyle='--', linewidth='0.5', color='red')
    ax.set_xlim ([0, len(tail_dta)]),ax.set_ylabel ('Angle', fontsize = 17 , color ='b')
    plot_ld_stimuli (tail_dta, ax , input_time_interval= len(tail_dta)/9, no_inputs=5 )
    
    ax = figl.add_subplot (5,1, 3)
    ax.plot(tail_dta)	
    ax.plot(event_X_idx['event_turn_left_idx'], tail_dta[event_X_idx['event_turn_left_idx']], 'o', color = '#965a00')
    ax.set_title ('Turns left' ,color='b', fontsize = 17)
    ax.tick_params (axis='y', colors='b'), ax.tick_params (axis='x', colors='b')
    ax.set_ylim ([-100, 100]), ax.grid(linestyle='--', linewidth='0.5', color='red')
    ax.set_xlim ([0, len(tail_dta)]),ax.set_ylabel ('Angle', fontsize = 17 , color ='b')
    plot_ld_stimuli (tail_dta, ax , input_time_interval= len(tail_dta)/9, no_inputs=5 )
    
    ax = figl.add_subplot (5,1, 4)
    ax.plot(tail_dta)
    if len(event_X_idx['event_struggle_idx']) > 0:
        ax.plot(event_X_idx['event_struggle_idx'], tail_dta[event_X_idx['event_struggle_idx']], 'o', color = '#ff0000')
        ax.set_title ('Struggles' ,color='b', fontsize = 17)
        ax.tick_params (axis='y', colors='b'), ax.tick_params (axis='x', colors='b')
        ax.set_ylim ([-100, 100]), ax.grid(linestyle='--', linewidth='0.5', color='red')
        ax.set_xlim ([0, len(tail_dta)]), ax.set_ylabel ('Angle', fontsize = 17 , color ='b')
    plot_ld_stimuli (tail_dta, ax , input_time_interval= len(tail_dta)/9, no_inputs=5 )    

    
    ax = figl.add_subplot (5,1, 5)
    ax.plot(tail_dta)
    ax.plot(event_X_idx['event_move_idx'], tail_dta[event_X_idx['event_move_idx']], 'o', color = '#9600ff'), ax.grid ('on')
    ax.set_title ('Foreward Move', fontsize = 17, color='b' ),
    ax.tick_params (axis='y', colors='b'), ax.tick_params (axis='x', colors='b')
    ax.set_ylim ([-40, 40]), ax.grid(linestyle='--', linewidth='0.5', color='red')
    # ax.set_xlim ([0, len(tail_dta)])
    ax.set_xlabel ('Time', fontsize = 20 , color ='b'),ax.set_ylabel ('Angle', fontsize = 17 , color ='b')
    plot_ld_stimuli (tail_dta, ax , input_time_interval= len(tail_dta)/9, no_inputs=5 )
    
    # ax = figl.add_subplot (5,1, 5) 
    # # ax.set_xlim ([0,1125])
    # ax.set_yticks([])
    # ax.set_title ('Stimuli', fontsize= 17)
    
    plt.tight_layout()
    
    plt.savefig(fileaddr, dpi = 400)
    



	