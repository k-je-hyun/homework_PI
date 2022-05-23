Python 3.10.4 (tags/v3.10.4:9d38120, Mar 23 2022, 23:13:41) [MSC v.1929 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import math
# github 에 엑셀 파일을 csv 파일로 변경하여 업로드 하고 raw파일을 불러와 데이터를 가져오는 방법.
# names = ['','','',''] 는 각 열의 이름을 지정해주어 불러오기 편하게 설정.
data_v=pd.read_csv('https://raw.githubusercontent.com/k-je-hyun/anemometer_data/main/Anemometer_Data1.csv',names=['X','Y','W','T'])

n = int(input("구간 개수 :"))
x = data_v["X"]
y = data_v["Y"]
w = data_v['W']
t = data_v["T"]

time=24377//n

pdM=np.array([])
tiM=np.array([])
xM=np.array([])
# u´의 x , y , z(=w) 성분의 root mean square 구하기
# numpy 에서 곱셈 기호 * 로 행렬을 곱하면 각 요소의 곱으로 구해지고 내적은 @를 이용하여 구함.

for i in range(n):
  xM=np.append(xM,i+1)
  tx_e=0
  ty_e=0
  tw_e=0
  tt_e=0
  tv_e=0
  print("구간 =",i+1)
  for j in range(time):
    x_element = float(x[[j+(time*i)]])
    y_element = float(y[[j+(time*i)]])
    w_element = float(w[[j+(time*i)]])
    t_element = float(t[[j+(time*i)]])
    tx_e = x_element**2 + tx_e
    ty_e = y_element**2 + ty_e
    tw_e = w_element**2 + tw_e
    tt_e = t_element + tt_e
    v_element = math.sqrt(x_element**2 + y_element**2 + w_element**2)
    tv_e = v_element + tv_e
  x_e_mean_square = math.sqrt(tx_e/time)
  y_e_mean_square = math.sqrt(ty_e/time)
  w_e_mean_square = math.sqrt(tw_e/time)
  t_e_mean = tt_e/time
  v_e_mean = tv_e/time
  TI=math.sqrt((x_e_mean_square**2 + y_e_mean_square**2 + w_e_mean_square**2)/3)/v_e_mean
  tiM=np.append(tiM,TI)
  print("Turbulence Intensity =" ,TI)
  pd = (3.143+0.3696*v_e_mean*TI)*(34-t_e_mean)*(v_e_mean-0.05)**0.6223
  pdM=np.append(pdM,pd)
  print("PD =",pd)
  print("===============================")
plt.plot(xM,tiM)
plt.xlabel('intervals')
plt.ylabel('Turbulence Intensity')
plt.title("Turbulence Intensity")
plt.show()
plt.plot(xM,pdM)
plt.hlines(15,0,n,colors='r',linestyle='solid')   # PD = 15% 인 부분 선 긋기
plt.xlabel('intervals')
plt.ylabel('PD')
plt.title('PD')
plt.show()