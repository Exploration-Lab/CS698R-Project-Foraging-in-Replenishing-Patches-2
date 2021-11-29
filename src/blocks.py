import gym 

class EnvClass:

    def __init__(self):
        
        envs = []
        
        env1 = gym.make("gym_env:firp-v0") 
        initial_bush_rewards = [0,70,70,0,70,0,70,0]
        repl_rate = [0,4,4,0,4,0,4,0]
        env1.set_env(initial_bush_rewards, repl_rate)
        
        env2 = gym.make("gym_env:firp-v0") 
        initial_bush_rewards = [0,0,70,70,0,70,0,70]
        repl_rate = [0,0,8,2,0,2,0,8]
        env2.set_env(initial_bush_rewards, repl_rate)
        
        env3 = gym.make("gym_env:firp-v0") 
        initial_bush_rewards = [70,0,0,70,70,0,70,0]
        repl_rate = [2,0,0,4,8,0,16,0]
        env3.set_env(initial_bush_rewards, repl_rate)
        
        
        self.envs = [env1,env2,env3]

        
    def getBlock(self,i):
        
        return self.envs[i-1]