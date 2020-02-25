from PyQt5.QtWidgets import QApplication,QMainWindow

for i in range(1,10):
    for j in range(1,i+1):
        if i==j:
            print(str(i)+'*'+str(j) +'='+str(i*j))
        else :
            print(str(i)+'*'+str(j) +'='+str(i*j)+';    ',end='')