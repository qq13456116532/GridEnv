import random
import sys
from typing import Optional

import pygame
import  gym

class GridEnv(gym.Env):
    metadata = {
        "render_modes": ["human", "rgb_array"],
        "render_fps": 50,
    }
    def getTerminal(self):
        return self.terminate_states

    def getGamma(self):
        return self.gamma

    def getStates(self):
        return self.states

    def getAction(self):
        return self.actions
    def getTerminate_states(self):
        return self.terminate_states
    def setAction(self,s):
        self.state=s

    def __init__(self,render_mode: Optional[str] = None):

        self.states = [1,2,3,4,5,6,7,8] #状态空间
        self.x=[140,220,300,380,460,140,300,460]
        self.y=[250,250,250,250,250,150,150,150]
        self.terminate_states = dict()  #终止状态为字典格式
        self.terminate_states[6] = 1
        self.terminate_states[7] = 1
        self.terminate_states[8] = 1
        self.mode = render_mode
        self.actions = ['n','e','s','w']

        self.rewards = dict();        #回报的数据结构为字典
        self.rewards['1_s'] = -1.0
        self.rewards['3_s'] = 1.0
        self.rewards['5_s'] = -1.0

        self.t = dict();             #状态转移的数据格式为字典
        self.t['1_s'] = 6
        self.t['1_e'] = 2
        self.t['2_w'] = 1
        self.t['2_e'] = 3
        self.t['3_s'] = 7
        self.t['3_w'] = 2
        self.t['3_e'] = 4
        self.t['4_w'] = 3
        self.t['4_e'] = 5
        self.t['5_s'] = 8
        self.t['5_w'] = 4

        self.gamma = 0.8         #折扣因子
        self.viewer = None
        self.state = None

    def step(self, action):
        # 系统当前状态
        state = self.state
        if state in self.terminate_states:
            return state, 0, True, {}
        key = "%d_%s" % (state, action)  # 将状态和动作组成字典的键值

        # 状态转移
        if key in self.t:
            next_state = self.t[key]
        else:
            next_state = state
        self.state = next_state

        is_terminal = False

        if next_state in self.terminate_states:
            is_terminal = True

        if key not in self.rewards:
            r = 0.0
        else:
            r = self.rewards[key]

        # 状态，reward，结束，截断条件，info
        return next_state, r, is_terminal, False,{}

    def reset(
            self,
            *,
            seed: Optional[int] = None,
            options: Optional[dict] = None,
    ):
        self.state = self.states[int(random.random() * len(self.states))]
        return self.state

    def render(self, close=False):
        if close:
            if self.viewer is not None:
                pygame.quit()
                self.viewer = None
            return

        screen_width = 600
        screen_height = 400

        if self.viewer is None:
            pygame.init()
            self.viewer = pygame.display.set_mode((screen_width, screen_height))
            self.robot_image = pygame.image.load('robot.png')  # 加载机器人图片，注意替换为你的图片路径
            self.robot_image = pygame.transform.scale(self.robot_image, (60, 60))
            self.trap_image = pygame.image.load('trap.png')  # 加载机器人图片，注意替换为你的图片路径
            self.trap_image = pygame.transform.scale(self.trap_image, (80, 80))
            self.gold_image = pygame.transform.scale(pygame.image.load('gold.png'), (80, 80))  # 加载并调整 gold 图片大小

            # 创建网格世界
            # 创建网格世界
            self.lines = [(100, screen_height - 300, 500, screen_height - 300),
                          (100, screen_height - 200, 500, screen_height - 200),
                          (100, screen_height - 300, 100, screen_height - 100),
                          (180, screen_height - 300, 180, screen_height - 100),
                          (260, screen_height - 300, 260, screen_height - 100),
                          (340, screen_height - 300, 340, screen_height - 100),
                          (420, screen_height - 300, 420, screen_height - 100),
                          (500, screen_height - 300, 500, screen_height - 100),
                          (100, screen_height - 100, 180, screen_height - 100),
                          (260, screen_height - 100, 340, screen_height - 100),
                          (420, screen_height - 100, 500, screen_height - 100)]

            self.circles = {'kulo1': [(140, screen_height - 150), 40, (0, 0, 0)],
                            'kulo2': [(460, screen_height - 150), 40, (0, 0, 0)],
                            'gold': [(300, screen_height - 150), 40, (255, 230, 0)],
                            'robot': [(self.x[self.state - 1], screen_height - self.y[self.state - 1]), 30,
                                      (204, 153, 102)]}
        if self.state is None:
            return None
        self.circles['robot'][0] = (self.x[self.state - 1], screen_height - self.y[self.state - 1])
        self.viewer.fill((255, 255, 255))  # Fill the background white
        for line in self.lines:
            pygame.draw.line(self.viewer, (0, 0, 0), line[:2], line[2:], 2)

        self.robot_pos = (self.x[self.state - 1] - 30, screen_height - self.y[self.state - 1] - 30)  # 转换为左上角坐标
        self.kulo1_pos = (self.circles['kulo1'][0][0] - 40, self.circles['kulo1'][0][1] - 40)
        self.kulo2_pos = (self.circles['kulo2'][0][0] - 40, self.circles['kulo2'][0][1] - 40)
        self.gold_pos = (self.circles['gold'][0][0] - 40, self.circles['gold'][0][1] - 40)  # 获取 gold 的位置

        for key, circle in self.circles.items():
            if key == 'robot':
                # 使用 blit() 方法将机器人图片绘制到屏幕上
                self.viewer.blit(self.robot_image, self.robot_pos)
            elif key == 'kulo1':
                self.viewer.blit(self.trap_image, self.kulo1_pos)
            elif key == 'kulo2':
                self.viewer.blit(self.trap_image, self.kulo2_pos)
            elif key == 'gold':  # 为 gold 绘制图片
                self.viewer.blit(self.gold_image, self.gold_pos)
        pygame.display.flip()
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                sys.exit()
        return None if self.mode == 'human' else pygame.surfarray.array3d(pygame.display.get_surface())










