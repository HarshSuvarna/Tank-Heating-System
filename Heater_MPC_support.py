import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
from scipy.optimize import minimize
import time


def simu(options, MPC):
    

    mpc = MPC()

    num_inputs = 2
    u = np.zeros(mpc.horizon*num_inputs)
    bounds = []

    # Set bounds for inputs bounded optimization.
    for i in range(mpc.horizon):
        bounds += [[0, 180]]
        bounds += [[-0.0, 0.0]]
    time_length = mpc.time_length   
    t = np.arange(0, time_length+mpc.dt, mpc.dt)
    ref = mpc.ref

    state_i = np.array([[0, 0]])
    u_i = np.array([[0, 0]])
    sim_total = len(t)
    #print(sim_total)
    predict_info = [state_i]
    U = np.zeros(sim_total+1)
    #distrubances
    U[20] = 20
    U[50] = -18
    U[80] = 5
    U[30] = -30
    
    
    for i in range(1,sim_total+1):
        
        start_time = time.time()
        
        # Non-linear optimization.
        u_solution = minimize(mpc.cost_function, u, (state_i[-1], ref),method='SLSQP',bounds=bounds,tol = 1e-5)
        #print(u_solution)
        #print(state_i[-1])
        #print(state_i[-1])
        print('Step ' + str(i) + ' of ' + str(sim_total) + '   Time ' + str(round(time.time() - start_time,5)))
        u = u_solution.x
        
        #print(u)
       
        
        y = mpc.plant_model(state_i[-1], mpc.dt, u[0], U[i])
        #print(y)
        predicted_state = np.array([y])
        
        
        for j in range(1, mpc.horizon):
            predicted = mpc.plant_model(predicted_state[-1], mpc.dt, u[2*j],u[2*j+1])
            predicted_state = np.append(predicted_state, np.array([predicted]), axis=0)
        predict_info += [predicted_state]
        state_i = np.append(state_i, np.array([y]), axis=0)
        u_i = np.append(u_i, np.array([(u[0], u[1])]), axis=0)
    #print(u_i)
    #print(state_i)

        


    fig = plt.figure(figsize = (16,10), dpi=120,facecolor=(0.7,0.8,0.8))
    gs = gridspec.GridSpec(4,3)
    

    ax = fig.add_subplot(gs[2:4,:], facecolor = (0.9,0.9,0.9))

    ax.set_ylim(0,210)
    ax.set_xlim(0,mpc.time_length)
    plt.xlabel('Time[s]',fontsize=15)
    plt.ylabel('knob_angle',fontsize=15)
    knob_angle_text = ax.text(25,2,'',size='20',color='k')
    plt.grid(True)
    knob_angle, = ax.plot([],[],'r',linewidth=1,label ='knob_angle')
    plt.legend(loc='upper right',fontsize='small')
    

    ax1 = fig.add_subplot(gs[0:2,:], facecolor = (0.9,0.9,0.9))

    ax1.set_ylim(0,110)
    ax1.set_xlim(0,mpc.time_length)
    plt.xlabel('Time[s]',fontsize=15)
    plt.ylabel('Temperature',fontsize=15)
    temperature_text = ax1.text(0,0,'',size='20',color='k')
    plt.grid(True)
    #prediction, = ax1.plot([],[],'r--',linewidth=1,label ='Predictions')
    temperature, = ax1.plot([],[],'b', linewidth=1,label ='Temperature.')
    plt.legend(loc='upper right',fontsize='small')

    

    def update_plot(num):
        knob_angle.set_data(t[0:num], u_i[0:num,0])
        #KA_text.set_text(str(round(state_i[num],2))+' Degrees')
        
        temperature.set_data(t[0:num], state_i[0:num,0])
        #prediction.set_data(t[0:num+mpc.horizon], predict_info[num][:,0])
        #temperature_text.set_text(str(round(state_i[num][0],2))+' mg/dl')
        #knob_angle_text.set_text(str(round(u_i[num][0],2))+' mg/dl')
        return knob_angle, temperature
    
    temp_animation=animation.FuncAnimation(fig, update_plot,frames=100,interval=100,repeat=True,blit=True)
    print(state_i)
    plt.show()
        
