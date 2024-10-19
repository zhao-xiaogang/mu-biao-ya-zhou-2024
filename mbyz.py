#!/usr/bin/env python2
#coding: utf8

import random
random.seed(3261.56) # 上证2024.10.18收盘指数做随机种子, 以确保每次仿真结果一致
from random import random as rand

games = filter(None,'''
国安 海牛 0.74 0.23 7-3-2
申花 深圳 0.77 0.21 2-0-0
沧州 海港 0.38 0.58 0-4-8
西海岸 蓉城 0.31 0.66 0-0-1
南通 国安 0.26 0.71 0-1-3
蓉城 申花 0.5 0.46 3-2-0
海港 天津 0.44 0.53 9-1-2
国安 河南 0.57 0.41 8-0-4
泰山 海港 0.67 0.32 5-3-4
'''.split('\n'))


def sim_main():
  team_score_dict = {
    '申花': 73.5, # 当申花和海港积分相同时,因申花一胜一平海港,申花的排名会靠前,所以这里申花的积分+0.5,以便于排名
    '海港': 72,
    '蓉城': 58,
    '国安': 49.5, # 国安和蓉城的比赛中国安一胜一平,故+0.5
  }

  def simulated(line):
    team_a, team_b, x, y, z = line.split()
    r1, r2 = rand(), rand()
    if r1 < 0.1:
      # 采用懂球帝猜胜负数据(截止2024.10.19上午)模拟
      # 10%的可能性进入本分支(平局概率偏小,严重偏离事实,故采用10%)
      q1, q2 = float(x), 1-float(y)
    elif r1 < 0.7:
      # 采用交锋历史数据(12场)模拟
      # 60%的可能性进入本分支
      s, p, f = map(float,z.split('-'))
      q1, q2 = s / (s+p+f), (s+p) / (s+p+f)
    else:
      # 纯随机模拟胜负平的概率各1/3
      # 30%的可能性进入本分支————三分天注定七分靠打拼
      q1, q2 = 1/3.0, 2/3.0
    if r2 < q1:
      return (team_a, 3, team_b, 0, '胜')
    elif r2 < q2:
      return (team_a, 1, team_b, 1, '平')
    else:
      return (team_a, 0, team_b, 3, '负')

  output = []
  for line in games[:-1]:
    a, x, b, y, z = simulated(line)
    if a in team_score_dict:
      team_score_dict[a] += x
    if b in team_score_dict:
      team_score_dict[b] += y
    output.append(a+z+b)

  score_team_list = sorted([(v,k) for k,v in team_score_dict.items()], reverse=True)

  while True:
    a, x, b, y, z = simulated(games[-1])
    if z != '平':
      break
  output.append(a+z+b)
  zxb_winner = a if x == 3 else b
  ygzg = ['无缘亚冠', '亚冠二级联赛区', '亚冠精英赛附加赛区', '亚冠精英赛区']
  output.append(score_team_list[0][1]+'联赛冠军')
  output.append(zxb_winner+'足协杯冠军')
  for socre, team in score_team_list:
    if team == zxb_winner:
      output.append(team+'亚冠精英赛区'+str(int(socre))+'分')
    else:
      output.append(team+ygzg.pop()+str(int(socre))+'分')
  if len(ygzg) == 0:
    output.append(zxb_winner+'亚冠精英赛区')
  return ' '.join(output)

result_map = {}
result_count = [
  ['申花联赛冠军', 0],
  ['海港联赛冠军', 0],
  ['蓉城亚冠精英赛附加赛区', 0],
  ['蓉城亚冠二级联赛区', 0],
  ['蓉城无缘亚冠', 0],
]
N = 1000000
for i in range(N):
  t = sim_main()
  for i in range(len(result_count)):
    if result_count[i][0] in t:
      result_count[i][1] += 1
  if t not in result_map:
    result_map[t] = 1
  else:
    result_map[t] += 1

result_list = sorted([(v,k) for k,v in result_map.items()], reverse=True)
j = 1
t_percent = 0
for count, txt in result_list:
  percent = float(count)/N*100
  t_percent += percent
  if t_percent > 95:
    break
  print '第{}号结局(概率{:.3f}%)'.format(j, float(count)/N*100), txt
  j += 1

print '-' * 100
print '仿真{}次,共{}个结局,以上只是部分结局(占95%),其中'.format(N, len(result_list))
for t, c in result_count:
  print '{}概率{:.2f}%'.format(t, float(c)/N*100)

print '本结果纯属娱乐'
