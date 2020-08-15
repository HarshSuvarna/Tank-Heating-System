import numpy as np
from Heater_MPC_support import simu

options={}
options['FIG_SIZE'] = [8,8]

class ModelPredictiveControl:
    def __init__(self):
        self.horizon =20
        self.dt = 0.1
        self.ref = [80,0]
        self.time_length = 10
        
    def plant_model(self, prev_temp, dt, u1,u2):
        knob_angle = u1
    
        # Knob angle to temperature
        knob_temp = (knob_angle * (0.5))
        # Calculate dT or change in temperature.
        tau = 6
        dT = (knob_temp - prev_temp[0])/tau
        # new temp = current temp + change in temp.
        state =u2 + prev_temp[0] + dT
        
        return [state,0]

    def cost_function(self, u, *args):
        state = args[0]
        cost = 0.0
        
        ref = args[1]  

        for i in range(0, self.horizon):
            state = self.plant_model(state,self.dt,u[i*2],u[i*2+1])
            
            cost+=( state[0] - ref[0] )**2
        return cost

simu(options,ModelPredictiveControl)




