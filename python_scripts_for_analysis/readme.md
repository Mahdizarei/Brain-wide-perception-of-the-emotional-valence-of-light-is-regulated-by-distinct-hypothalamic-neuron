# Light/Dark choice

## light_dark_choice function is need for this analyses

```python

id_L =[]
id_D =[]
id_trans_L =[]
id_trans_D =[]
id_Init_L =[]
id_Init_D =[]
id_NOResp =[]    
for i in range(len(df_tmp)):
    ld_res = light_dark_choice (df_tmp[i], interval_size =200, repetition = 7, interval_strtl_steps = 3)
    if ld_res [0] == 'Light':
        id_L.append(i)
    if ld_res [0] == 'Dark':
        id_D.append(i)
    if ld_res [0] == 'Light_transition':
        id_trans_L.append(i)
    if ld_res [0] == 'Dark_transition':
        id_trans_D.append(i)
    if ld_res [0] == 'Light_initial':
        id_Init_L.append(i)
    if ld_res [0] == 'Dark_initial':
        id_Init_D.append(i)
    if ld_res [0] == 'no_response':
        id_NOResp.append(i)
        
```

# Tail events detection
## Three functions are need for this analysis: 
1. ### tail_movement_CLASS
2. ### event_count which is called by tail_movement_CLASS (it is in TestingThescripts_Tail_mv.py)
3. ### source_target_hit

```python

# Tail angles time series
tail_dta = array([0.     , 1.4004 , 1.4004 , ..., 0.92304, 0.92304, 0.92304])

# DETECTING THE EVENTS (Evenet intervals and onset)
event_move, event_move_idx , event_turn, event_turn_idx, event_struggle, event_struggle_idx = \
  tail_movement_CLASS (tail_dta, scale_move = 15, event_interval_thre = 25, scale_turn_Strgl = 15)

'''
Merging the overlapped events (The priority of the turn is higher
than the priority of the move, and the priority of the struggle is higher than the priority of the turn. )
 '''
event_turn, event_turn_idx , event_move, event_move_idx, mached_sor_tar = \ 
    source_target_hit (tail_dta, event_turn , event_turn_idx, event_move, event_move_idx, effect_size = 5)

event_struggle , event_struggle_idx  , event_move, event_move_idx, mached_sor_tar = \ 
    source_target_hit (tail_dta, event_struggle , event_struggle_idx,  event_move, event_move_idx, effect_size = 200)

event_struggle , event_struggle_idx, event_turn, event_turn_idx, mached_sor_tar = \
    source_target_hit (tail_dta, event_struggle ,event_struggle_idx,  event_turn, event_turn_idx, effect_size = 25 )    
   

# Foreward movements
[[405, 1009], [1103, 1106], [1212, 1213], ... ,[96936, 96955]]

# Turns
[[348, 404], [4663, 4713], [13325, 13347], ..., [88019, 88081]]

# Struggles
[[76328, 76527], [91107, 91146]]

```
