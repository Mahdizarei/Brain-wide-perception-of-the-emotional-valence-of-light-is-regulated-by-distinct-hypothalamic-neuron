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

def tail_movement_CLASS (tail_dta , scale_move = 15, event_interval_thre = 25, scale_turn_Strgl = 10):
    tail_dta_MOVE = {}
    tail_dta_MOVE ['idx'] = []
    tail_dta_Flp_Strgl = {}
    tail_dta_Flp_Strgl ['idx'] = []
    tail_dta_Flp_Strgl ['angle'] = []    
    for t in range(len(tail_dta)):
        if np.abs(tail_dta[t] )> 2:
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
    
    event_turn, event_turn_idx, event_struggle, event_struggle_idx = event_count (tail_dta , 
                                                                                  event_type = event_TYPE [1] ,
                                                                                  event_idx = tail_dta_Flp_Strgl ['idx'], 
                                                                                  event_interval_threshold = event_interval_thre,
                                                                                  scale_Flp_Strgl = scale_turn_Strgl)
    
    return np.asarray(event_move), np.asarray(event_move_idx) , \
np.asarray(event_turn), np.asarray(event_turn_idx), np.asarray(event_struggle), np.asarray(event_struggle_idx)
