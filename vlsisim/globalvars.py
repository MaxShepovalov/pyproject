#global variables

#Notify levels
notify_errors = True
notify_warnings = True
notify_info = True
notify_debug = True

#state for simulation. 'Run','Stop'
state = 'Run'

#current iteration. Integer
time = 0

#forces update if wire's value did not changed. Default: False
force_same_v_update = False

#notify about new tasks. Default: False
notify_new_task = True

#Digital threshhold for ADC. Consider values higher than threshold as logical 1
digital_thr = 1.0

#Digital levels
digital_high = 5.0
digital_low = 0.0

#automatically connect wires when add device
autoconnect = True