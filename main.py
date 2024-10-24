# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 18:20:30 2024

@author: 21624
"""

import numpy as np
import random

class gridworld:

    def __init__(self,map_size):
        self.size=map_size  #生成地图规格
        self.state=0#agent的初始位置
        self.goal=(map_size-1,map_size-1)#目标宝藏的位置
        
    def reset(self):#显而易见
        self.state=0
        return self.state

    def move(self,action):#智能体状态更新的方法（包括奖励值的返回）
        if action==0:#左
            self.state=max(self.state-1,0)#考虑边界
        if action==1:#右
            self.state=min(self.state+1,self.size-1)
        if self.state==(self.size-1):#达到宝藏位置，游戏结束
            reward=1
            done=1
        if self.state!=(self.size-1):#没到达，游戏继续
            reward=0
            done=0
        return self.state,reward,done
    
    def redraw(self):#可视化表达，下面几行无需多言
        for n in range(self.size):
            if n==self.state:
                print("o",end="")
            if n==(self.size-1):
                print("X",end="")
            else:
                print("-",end="")
        print("\n")
        
        
        
class Qlearning:
    
    def __init__(self,env,sum_steps=6,action_space=2,learning_rate=0.1,gamma=0.1,exploration_rate=0.2):
        """
        以下为qlearning算法的核心参数：
        Q表无需多言
        lr学习速率，也叫alpha
        gamma即折扣因子，范围一般是0-1（也有一些创新论文把这个参数设置为大于1），表示了对长远
        奖励的注意力，0表示只关注当前奖励值（显然是不合适的）
        exploration_rate是指自由探索的概率，即不参照q表选择行动，前期需要靠自由探索找到奖励点
        """
        self.q_table=np.zeros((sum_steps,action_space))
        self.lr=learning_rate
        self.gamma=gamma
        self.ex=exploration_rate
        self.env=env
        
    def action_choice(self):#动作的选择
        if random.uniform(0,1)<self.ex:#random.uniform(0,1)的意思是在这个区间内随机选择一个
            return random.randint(0,1)#这是自由探索环节
        else:
            return np.argmax(self.q_table[self.env.state])#这是按q表选择环节，np.argmax()是返回最大值的索引
        
    def update(self,reward,action,state,new_state):
        """
        下面是qlearning算法的核心--q表的更新
        具体公式看图片
        """
        self.q_table[state][action]=self.q_table[state][action]+self.lr*(max(self.q_table[new_state][0],self.q_table[new_state][1])*self.gamma+reward-self.q_table[state][action])
        
    def train(self,episodes,test,sum_steps=6):#训练过程，test表示是否输出训练过程
        if test:
            self.env.redraw()#输出行动过程
        for i in range(episodes):
            for m in range(sum_steps):
                action=self.action_choice()#行动选择
                state=self.env.state#智能体旧状态记录，q表更新时要用到
                self.env.state,reward,done=self.env.move(action)#智能体状态更新
                self.update(reward,action,state,self.env.state)#q表更新
                if test:
                    print(self.q_table)
                    #print(reward)
                if test:
                    self.env.redraw()
                #print(self.env.state)
                if done==1:
                    if test:
                        print("win")
                    self.env.reset()#智能体状态复原
                    break
            if done==0:
                if test:
                    print("failed")
                self.env.reset()
        
        

size=5
train=0
test=1
epoch=10000
        
env=gridworld(size)
Q=Qlearning(env)   
#Q.train(500,0)
Q.train(epoch,train)
Q.train(1,test)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        