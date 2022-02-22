'''
This function removes the overlaped events and the related indices and extends the original event
by: Mahdi Zarei: 09-25-2020
'''

def source_target_hit (tail_dta , event_source, event_source_idx, event_target, event_target_idx, effect_size = 25 ):
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
