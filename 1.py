# start taxi

'''
6 3 15

0 0 1 0 0 0
0 0 1 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 1 0
0 0 0 1 0 0

6 5

2 2 5 6
5 4 1 6
4 2 3 5

'''

'''
변수명 정리

n(격자 수) => n
m(손님 수) => m
fuel(연료의 양) => fuel
택시 좌표 => taxiX, taxiY
지도 => gridMap



'''


import tkinter
import numpy as np
import time
from collections import deque
'''
window = tkinter.Tk()
window.title("Algorithm")

canvas = tkinter.Canvas(width = 400, height= 400, bg= "white")
canvas.grid(row= 0, column= 0, rowspan=10)
global n, m, fuel'''

##################################################
#
#   Gui commnad
#
##################################################



#nButton clicked command
def click_nButton():
    global n, m, fuel
    temp = (nEntry.get()).split()
    n = int(temp[0])
    m = int(temp[1])
    fuel = int(temp[2])

    #print(n, m,fuel)
    nToStr = str(n)
    mToStr = str(m)
    fuelToStr = str(fuel)
    nConditonLabel.config(text = "n, m, fuel : "+ nToStr + ", " + mToStr + ", " + fuelToStr)

    global draftMap 
    draftMap = [[0 for col in range(n)] for row in range(n)]
    #print(draftMap)
  
# create map : 2D array // 1 -> wall , 0 -> road
def createMap(l):
    draftMap = np.reshape(l, (n,n))

    global gridMap
    gridMap = draftMap.tolist()
    draw_map()


# map_button clicked command
def click_mapButton():
    result = mapText.get("1.0", "end")
    result2 = result.split()
    result2 = list(map(int, result2))
    createMap(result2)

def draw_map():
    mapPadding = 20
    # draw map // wall's color : gray, road's color : white
    for y in range(n):
        for x in range(n):
            mapX = x * 50 + mapPadding
            mapY = y * 50 + mapPadding
            if gridMap[y][x] == 0:
                canvas.create_rectangle(mapX , mapY, mapX + 50, mapY + 50, fill= "white")
            else:
                canvas.create_rectangle(mapX , mapY, mapX + 50, mapY + 50, fill= "gray")
    #print(gridMap)
    mapConditonLabel.config(text = "Successfully drawn.")

global taxiCount
taxiCount = 0

def click_taxiButton():
    #To be used in algorithms
    global taxiX, taxiY       
    taxiLocation = (taxiEntry.get()).split()
    taxiXTemp = int(taxiLocation[0])
    taxiYTemp = int(taxiLocation[1])

    global taxiCount, taxi
    taxiCondition = ""

    if(gridMap[taxiXTemp - 1][taxiYTemp - 1] != 1 and taxiCount == 0):
        taxiX = taxiXTemp
        taxiY = taxiYTemp
        taxi = canvas.create_image((taxiY - 1) * 50 + 45, (taxiX - 1) * 50 + 45, image = taxiImg)
        taxiCount = 1
        taxiXToStr = str(taxiX)
        taxiYToStr = str(taxiY)
        taxiCondition = "Taxi location : " + taxiXToStr + ", " + taxiYToStr
    elif(taxiCount == 1):
        taxiCondition = "Taxi already exists."
    elif(gridMap[taxiXTemp - 1][taxiYTemp - 1] == 1 ):
        taxiCondition = "Taxi cannot exist here."
    taxiConditonLabel.config(text = taxiCondition)


def click_userButton():
    result = userText.get("1.0", "end")
    result2 = result.split()
    temp = list(map(int, result2))
    global srcs, dsts
    srcs = []
    dsts = []
    for i in range(m):
        srcs.append([temp[0 + 4*i], temp[1 + 4*i]])
        dsts.append([temp[2 + 4*i], temp[3 + 4*i]])
    
    userCondition = ""
    
    for i in range(m):
        user = "User" + str(i + 1) + " src : " + str(srcs[i]) + " / dst: " + str(dsts[i]) + "\n"
        userCondition += user
    userConditionLabel.config(text = userCondition)
    #draw user src, dst Img
    register_imgFile()
    import_userImg()
    #print(srcs)
    #print(dsts)

def import_userImg():
    #import img
    for i in range(m):   
        canvas.create_image((srcs[i][1] - 1) * 50 + 45, (srcs[i][0] - 1) * 50 + 45, image = userSrcImg[i])
        canvas.create_image((dsts[i][1] - 1) * 50 + 45, (dsts[i][0] - 1) * 50 + 45, image = userDstImg[i]) 

def register_imgFile():
    #fileList = os.listdir("img")
    #ImgList = [k for k in fileList if(k.endswith(".PNG") or (k.endswith(".png")==True))]
    userDstImgList = ["img/dst1.png", "img/dst2.png", "img/dst3.png", "img/dst4.png", "img/dst5.png"]
    userSrcImgList = ["img/src1.png", "img/src2.png", "img/src3.png", "img/src4.png", "img/src5.png"]
    global userSrcImg, userDstImg
    userSrcImg = []
    userDstImg = []
    for i in range(m):
        userSrcImg.append(tkinter.PhotoImage(file=userSrcImgList[i]))
        userDstImg.append(tkinter.PhotoImage(file=userDstImgList[i]))
global isRun
isRun = True

def result(code):
    global isRun
    resultText =""
    if code == 1:
        resultText = "You can't go to all the users"
    elif code == 2:
        resultText = "Lack of Fuel"
    elif code == 3:
        resultText = "You can't go to the user's destination"
    elif code == 4:
        resultText = "Lack of Fuel (to the destination)"
    elif code == 5:
        resultText = "Don't Run"

    print(resultText)
    resultLabel.config(text = resultText)
    isRun = False
        
def click_runButton():
    if isRun == True:
        mapPadding = 20
        for i in range(n+1):
            mapX = qy[i] * 50 + mapPadding
            mapY = qx[i] * 50 + mapPadding
            if i == n:
                break
            canvas.create_rectangle(mapX, mapY, mapX + 50, mapY + 50, fill= "white")
            window.update()
        
            if i < n:
                mapX = qy[i+1] * 50 + mapPadding
                mapY = qx[i+1] * 50 + mapPadding
                canvas.create_rectangle(mapX, mapY, mapX + 50, mapY + 50, fill= "white")
                window.update()
                draw_taxi(qy[i+1], qx[i+1])
    else:
        result(5)


def draw_taxi(x, y):
    canvas.create_image(x * 50 + 45, y * 50 + 45, image = taxiImg)
    window.update()
    time.sleep(1)

def update_fuel(f):
    fuelCondition = "Amount of Fuel: " + str(f)
    resultLabel.config(text = fuelCondition)



def click_clearButton():
    canvas.delete("all")
    global taxiCount, n, m, fuel
    taxiCount = 0
    n = 0
    m = 0
    fuel = 0
    canvas.delete("all")
    
    

#############################################################
# 
# algorithm
# 
#############################################################  
def bfs(dst):
    get_q(q)
    visited[q[0][0]][q[0][1]] = True
    dst[q[0][0]][q[0][1]] = 0  
    while q:
    	x, y = q.popleft()
    	for i in range(4):
    		nx, ny = x + dx[i], y + dy[i]
    		if 0 <= nx < n and 0 <= ny < n and gridMap[nx][ny] == 0 and not visited[nx][ny]:
    			visited[nx][ny] = True
    			q.append((nx, ny))
    			dst[nx][ny] = dst[x][y] + 1


def click_calcuateButton(): 
    global q, dx, dy, isRun
    user = {}
    q = deque()
    dx, dy = [0,0,-1,1], [-1,1,0,0]
    f = fuel
    q.append((taxiX-1, taxiY-1))
    
    for i in range(m):
    	user[i] = [srcs[i][0] - 1, srcs[i][1] - 1, dsts[i][0] - 1, dsts[i][1] -1]
    
    # user sort
    user = dict(sorted(user.items(), key = lambda x: (x[1][0], x[1][1])))


    while True:
        global visited
        arr = []
        minimum = 1000
        visited = [[False] * n for _ in range(n)]
        dst = [[-1] * n for _ in range(n)]
    
    	# bfs(First taxi location)
        bfs(dst)
        
    	# Calculate the distance to the guests and Find the closest location.
        for i in user:
            if dst[user[i][0]][user[i][1]] != -1:
                if dst[user[i][0]][user[i][1]] < minimum:
                    minimum = dst[user[i][0]][user[i][1]]
                    arr = [i]
                elif dst[user[i][0]][user[i][1]] == minimum:
                    arr.append(i)
    
    	# If you can't go to all the users
        if not arr:
            print(-1)
            result(1)
            break
        
    	# Minus the amount of fuel needed from the amount of fuel to the user.
        f -= dst[user[arr[0]][0]][user[arr[0]][1]]
        # If f is less than 0 after subtracting it, it will not reach the destination.
        if f <= 0:
            print(-1)
            result(2)
            break
        else:
    		# Go to the destination.
            q = deque()
            q.append((user[arr[0]][0], user[arr[0]][1]))
            visited = [[False] * n for _ in range(n)]
            #dst = [[-1] * n for _ in range(n)]
    
    		# Put the destination coordinates of the user into q and execute bfs.
            bfs(dst)
            
    		# If you can't go to the user's destination, dst = -1
            if dst[user[arr[0]][2]][user[arr[0]][3]] == -1:
                print(-1)
                result(3)
                break
            
    		# Minus the amount of fuel needed to get to the destination from the current amount of fuel.
            f -= dst[user[arr[0]][2]][user[arr[0]][3]]
    
    		# The amount of fuel x2 After charging, the user cancels it.
            if f >= 0:
                f += dst[user[arr[0]][2]][user[arr[0]][3]] * 2
                q.append((user[arr[0]][2], user[arr[0]][3]))
                del user[arr[0]]
            else:
    			# If F is less than 0, the fuel is exhausted on the way, so it's over.
                print(-1)
                result(4)
                break
        print(f) 
    	# If you take all the users , the current fuel will be output and the end.
        if not user:
            get_q(q)
            print(f)
            update_fuel(f)
            isRun = True
            break
global qx, qy
qx = []
qy = []

def get_q(queue):
    x, y = q[0][0], q[0][1]
    qx.append(x)
    qy.append(y)

############################################################
# 
#   GUi
#
#############################################################


window = tkinter.Tk()
window.title("Algorithm")
canvas = tkinter.Canvas(width = 400, height= 400, bg= "white")
canvas.grid(row= 0, column= 0, rowspan=10)
global n, m, fuel
    # Input n, m, fuel

nLabel = tkinter.Label(window, text="N , M , Fuel : ")
nEntry = tkinter.Entry(window, width = 15)
nButton = tkinter.Button(window, text="Enter", command=click_nButton)
nLabel.grid(row=0, column=1, pady = 10, padx=10)
nEntry.grid(row=0, column=2, pady =10)
nButton.grid(row=0, column=3, padx = 10)

 # Input map
mapLabel = tkinter.Label(window, text="Map: ")
mapText = tkinter.Text(window, height= 10, width= 15)
mapButton = tkinter.Button(window, text="Enter", command=click_mapButton)


mapLabel.grid(row = 1, column = 1)
mapText.grid(row = 1, column = 2)
mapButton.grid(row = 1, column = 3)

'''
canvas = tkinter.Canvas(width = 350, height= 350, bg= "white")
canvas.grid(row= 0, column= 0)
'''

#Input taxi
taxiImg = tkinter.PhotoImage(file="taxi.png")  # 30 x 30
taxiLabel = tkinter.Label(window, text = "Taxi location : ")
taxiEntry = tkinter.Entry(window, width = 15)
taxiButton = tkinter.Button(window, text="Enter", command=click_taxiButton)

taxiLabel.grid(row=2, column=1)
taxiEntry.grid(row=2, column=2)
taxiButton.grid(row=2, column=3)

userLabel = tkinter.Label(window, text = "User src, dst : ")
userText = tkinter.Text(window, height = 5, width = 15)
userButton = tkinter.Button(window, text = "Enter", command=click_userButton)

userLabel.grid(row=3, column=1)
userText.grid(row=3, column=2)
userButton.grid(row=3, column=3)

nConditonLabel = tkinter.Label(window, text = "")
mapConditonLabel = tkinter.Label(window, text= "")
taxiConditonLabel = tkinter.Label(window, text = "")
userConditionLabel = tkinter.Label(window, text="")
resultLabel = tkinter.Label(window, text="")

rowNum = 5
nConditonLabel.grid(row = rowNum, column=1) 
rowNum += 1
mapConditonLabel.grid(row = rowNum, column=1)
rowNum += 1
taxiConditonLabel.grid(row = rowNum, column = 1)
rowNum += 1
userConditionLabel.grid(row = rowNum, column=1)
resultLabel.grid(row=5, column= 2, rowspan= 4, padx= 10 )


calculateButton = tkinter.Button(window, text="Calculate", command=click_calcuateButton)
calculateButton.grid(row=rowNum + 1, column=1)

runButton = tkinter.Button(window, text="Run", command=click_runButton)
runButton.grid(row=rowNum + 1, column=2)

clearButton = tkinter.Button(window, text="Clear", command=click_clearButton)
clearButton.grid(row = rowNum +1, column= 3)

#canvas.create_oval(55, 55, 34, 34, fill= "black")  
#window.update() 

#taxiX = 4
#taxiY = 5
#canvas.create_image(taxiX * 50 + 45, taxiY * 50 + 45, image = taxiImg)


window.mainloop()
