# -*- coding: cp1251 -*-
import cv2
import os
import datetime
import transliterate
#открыть дирректорию
def OpenMyFile():
    path= os.getcwd()
    files = os.listdir(path)
    video = filter(lambda x: x.endswith('.avi'), files)
    files = os.listdir(path+"/screenshot")
    images = filter(lambda x: x.endswith('.jg'), files)
    return images, video
#Функция вычисления хэша
def CalcImageHash(image):
    resized = cv2.resize(image, (6,6), interpolation = cv2.INTER_AREA) #Уменьшим картинку
    gray_image = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY) #Переведем в черно-белый формат
    avg=gray_image.mean() #Среднее значение пикселя
    ret, threshold_image = cv2.threshold(gray_image, avg, 255, 0) #Бинаризация по порогу
    #print("Бинаризация по порогу=", threshold_image)
    #Рассчитаем хэш
    _hash=""
    for x in range(6):
        for y in range(6):
            val=threshold_image[x,y]
            if val==255:
                _hash=_hash+"1"
            else:
                _hash=_hash+"0"
    return _hash
def CompareHash(h1,h2):
    l=len(h1)
    i=0
    count=0
    while i<l:
        if h1[i]!=h2[i]:
            count=count+1
        i=i+1
    return count
def puttextimage(img, text):  #добавляем надпись на картинку
    font = cv2.FONT_HERSHEY_SIMPLEX
    # org
    org = (50, 50)
    # fontScale
    fontScale = 0.5
    # Blue color in BGR
    color = (255, 0, 0)
    # Line thickness of 2 px
    thickness = 2
    text=transliterate.translit(text, reversed=True)
    # Using cv2.putText() method
    img = cv2.putText(img, text, org, font, fontScale, color, thickness, cv2.LINE_AA)
    return img

def FindScreen(_file):
    i=0 #считаем нахождение
    j=0 #считаем кадры
    _cap = cv2.VideoCapture(_file)
    while(_cap.isOpened()):
        ret, frame = _cap.read()
        if ret==False:    # ожидание конца файла
            break
        j+=1
        if j%10==0: #  проверяем только каждый 10 кадр
            hash2=CalcImageHash(frame)
            for hash in hash1:
                diff=CompareHash(hash, hash2)
                if diff<100:
                    print(diff)
                    frame=puttextimage(frame, _file+ str(i))
                    file_tr=transliterate.translit(_file, reversed=True)
                    cv2.imwrite("images/" +file_tr+ str(i)+".jpg",frame)
                    i+=1
    _file=transliterate.translit(_file, reversed=True)
    f.write(_file + " - " +str(i) + '\n')
    _cap.release()
    cv2.destroyAllWindows() #закрытие всех окон(обязательно)
    return
f = open('log.txt', 'a')
f.write("Begin: " + str(datetime.datetime.now()) + '\n') #пишем время начала работы
images,video=OpenMyFile()
path= os.getcwd()
if not os.path.exists(path+"/images"):
    os.mkdir("images")
hash1=[]
for x in images:
    print("/screenshot/"+x)
    img = cv2.imread("screenshot/"+x)
    hash1.append(CalcImageHash(img))
    print("hash1=", hash1)

for file in video:
    print("file=", file)
    FindScreen(file)

f.write("End: " + str(datetime.datetime.now()) + '\n') #пишем время окончания работы
f.close()
