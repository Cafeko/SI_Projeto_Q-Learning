import connection as cn

s = cn.connect(2037)
 
print(cn.get_state_reward(s, "right"))