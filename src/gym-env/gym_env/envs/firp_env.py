import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np

class FIRP(gym.Env):

    def __init__(self):
        self.action_space = spaces.Discrete(8)# action i means go to bush i and if you are already there then it means mine it
        self.observation_space = spaces.Discrete(9)#8 is the home palce
        self.max_time = 300.0
        self.elapsed_time = 0.0
        self.rewarding_bush = [False,False,False,False,False,False,False,False]
        self.replenish_rate=[0,0,0,0,0,0,0,0]
        self.initial_bush_rewards =[0,0,0,0,0,0,0,0]##need to store this for easy reset functionality
        self.current_bush_rewards =[0,0,0,0,0,0,0,0]
        self.collected_reward = 0
        self.present_state =8

    def set_env(self, initial_bush_rewards, replenish_rate):
        self.initial_bush_rewards = np.array(initial_bush_rewards, dtype=np.float32)
        self.current_bush_rewards  = np.array(initial_bush_rewards, dtype=np.float32)
        self.replenish_rate = np.array(replenish_rate, dtype=np.float32)
        self.collected_reward =0
        self.elapsed_time =0
        self.present_state = 8
        for i in range(len(initial_bush_rewards)):
            if(initial_bush_rewards[i]!=0):
                self.rewarding_bush[i] = True
            else:
                self.rewarding_bush[i] = False
        return

    def reset(self):
        self.collected_reward =0
        self.elapsed_time =0
        self.current_bush_rewards = np.copy(self.initial_bush_rewards)
        self.present_state =8
        return

    def get_movement_time(self,start_vertex, end_vertex):
        
        r = 1/(2*np.sin(np.pi/8))
        
        if(start_vertex==8):
            return r
        distance = min(abs(start_vertex-end_vertex), (8-abs(start_vertex-end_vertex)))
        if(distance==1):
            return 1
        elif(distance ==2):
            return (2*r*np.sin(np.pi/4))
        elif(distance==3):
            return (2*r*np.sin(3*np.pi/8))
        else:
            return 2*r

    def step(self, action):
        if(self.elapsed_time>=self.max_time):
            return (self.present_state,max(0,self.max_time-self.elapsed_time)), 0, True, {}

        if(action==self.present_state):
            if(self.rewarding_bush[self.present_state]==False):
                self.elapsed_time+=1
                done = (self.elapsed_time>=self.max_time)
                return ((self.present_state, max(0,self.max_time-self.elapsed_time)), 0, done, {})
            else:
                self.elapsed_time+=1
                done = (self.elapsed_time>=self.max_time)
                if(done and self.elapsed_time!=self.max_time):
                    return((self.present_state, max(0,self.max_time-self.elapsed_time)), 0, done, {})
                
                this_reward = self.current_bush_rewards[self.present_state]
                self.collected_reward += int(0.9* this_reward)
                self.current_bush_rewards +=self.replenish_rate
                for i in range(len(self.current_bush_rewards)):
                    if(self.current_bush_rewards[i]>200):
                        self.current_bush_rewards[i]=200

                self.current_bush_rewards[self.present_state] = int(0.9*this_reward)##cause mined bush doesnt replenish 
                return((self.present_state, max(0,self.max_time-self.elapsed_time)), int(this_reward*0.9), done, {})
                
        else:
            self.elapsed_time += self.get_movement_time(self.present_state,action)
            done = (self.elapsed_time>=self.max_time)
            if(done and self.elapsed_time!=self.max_time):
                return((self.present_state, max(0,self.max_time-self.elapsed_time)), 0, done, {})
            self.present_state = action
            return((self.present_state, max(0,self.max_time-self.elapsed_time)), 0, done, {})
    
    def get_curr_state(self):
        return((self.present_state, self.elapsed_time, self.current_bush_rewards, self.collected_reward))
    
    def render(self):
        pass
