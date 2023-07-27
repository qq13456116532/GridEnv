
from MyGridEnv import  GridEnv

env = GridEnv(render_mode='human')
start = env.reset()
print("start =",start)
env.render()
over = False
while not over:
    user_in = input()
    if(user_in=='n'):
        next_state, r, over,*_ =env.step('n')
        print("state =",next_state)
    if (user_in == 'e'):
        next_state, r, over, *_ = env.step('e')
        print("state =", next_state)
    if (user_in == 's'):
        next_state, r, over, *_ = env.step('s')
        print("state =", next_state)
    if (user_in == 'w'):
        next_state, r, over, *_ = env.step('w')
        print("state =", next_state)
    env.render()
