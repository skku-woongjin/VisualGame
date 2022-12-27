#1 Hi
from regex import B
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms

from IPython import get_ipython
from IPython.display import display 
import matplotlib.pyplot as plt
from matplotlib.pyplot import imshow
import cv2
#get_ipython().run_line_magic('matplotlib', 'inline')

from PIL import Image
import requests
import torch
from torchvision import transforms
from torchvision.transforms.functional import InterpolationMode

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


##js파일 만들기
import math
import random
from random import shuffle
import json


#상위 카테고리
bigCateList =["FOOD", "VEHICLE", "ANIMAL", "SPORTS", "FURNITURE", "ETC"]

bigCateAnswer = random.choice(bigCateList)


#하위 카테고리

if(bigCateAnswer == "FOOD"): 
    smallCateList1 =["APPLE", "BANANA", "ORANGE", "CARROT", "PIZZA", "DONUT", "CAKE"]

elif (bigCateAnswer == "VEHICLE"):
    smallCateList1 =["BICYCLE", "CAR", "MOTORCYCLE", "AIRPLANE", "BUS", "TRAIN", "TRUCK", "BOAT"]
  
elif(bigCateAnswer == "ANIMAL"):
    smallCateList1 =["BIRD", "CAT", "DOG", "HORSE", "SHEEP", "COW", "ELEPHANT", "BEAR", "ZEBRA", "GIRAFFE"]
  
elif (bigCateAnswer == "SPORTS"): 
    smallCateList1 =["SKIS", "SNOWBOARD", "TENNIS", "SKATEBOARD"]
  
elif (bigCateAnswer == "FURNITURE"): 
    smallCateList1 =["CHAIR", "BED", "TABLE", "TV", "CELL_PHONE", "BOOK", "CLOCK", "SCISSORS", "TEDDY_BEAR"]
  
elif (bigCateAnswer == "ETC"): 
    smallCateList1 =["PERSON", "STOP_SIGN", "UMBRELLA"]
  
smallCateAnswer = random.choice(smallCateList1)

imgNumAnswer = smallCateAnswer.lower() + str(random.randrange(1, 102))  # 1이상 102미만 


with open('static//DATA.json', 'r') as f:
    json_file = json.load(f)

answerPic = json_file[bigCateAnswer][smallCateAnswer][imgNumAnswer]     #정답
sameCatePic = json_file[bigCateAnswer][smallCateAnswer]         #같은 카테고리


tmp_answer= " ".join(answerPic)
tmp_answer2 = tmp_answer.replace("\\","//")
answerPic = []
answerPic = tmp_answer2.split()

### Easy버전

img_arrs = []       #image 3x3 출력용, == pictures2
CateList = [" "]

img_arrs.append(answerPic)
Number2 = []         # == lotto2


while len(Number2) < 6 :     # 3x3이라서 8개(정답 제외)의 '랜덤 그림'
    a = random.randint(1, 101)
    if a not in Number2:
        Number2.append(a)
        bigCateRandom = random.choice(bigCateList)
    
        if(bigCateRandom == "FOOD"): 
            smallCateList2 =["APPLE", "BANANA", "ORANGE", "CARROT", "PIZZA", "DONUT", "CAKE"]

        elif (bigCateRandom == "VEHICLE"):
            smallCateList2 =["BICYCLE", "CAR", "MOTORCYCLE", "AIRPLANE", "BUS", "TRAIN", "TRUCK", "BOAT"]
  
        elif(bigCateRandom == "ANIMAL"):
            smallCateList2 =["BIRD", "CAT", "DOG", "HORSE", "SHEEP", "COW", "ELEPHANT", "BEAR", "ZEBRA", "GIRAFFE"]
  
        elif (bigCateRandom == "SPORTS"): 
            smallCateList2 =["SKIS", "SNOWBOARD", "TENNIS", "SKATEBOARD"]
  
        elif (bigCateRandom == "FURNITURE"): 
            smallCateList2 =["CHAIR", "BED", "TABLE", "TV", "CELL_PHONE", "BOOK", "CLOCK", "SCISSORS", "TEDDY_BEAR"]
  
        elif (bigCateRandom == "ETC"): 
            smallCateList2 =["PERSON", "STOP_SIGN", "UMBRELLA"]
        
        smallCateRandom = random.choice(smallCateList2)
        CateList.append(smallCateRandom)        #AA

        img_arrs.append(json_file[bigCateRandom][smallCateRandom][smallCateRandom.lower()+str(a)])




Number3 = [imgNumAnswer]    #lotto3

while len(Number3) < 3 :     # 3x3이라서 8개(정답 제외)의 '같은 카테고리 그림'
    a = random.randint(1, 101)
    if a not in Number3:
        Number3.append(a)
        img_arrs.append(json_file[bigCateAnswer][smallCateAnswer][smallCateAnswer.lower()+str(a)])
        CateList.append(smallCateAnswer)        #AA

img_arrs_shuffle = random.sample(img_arrs, len(img_arrs))

img_arrs_shuffle_img = []
for i in range(9):
    img_arrs_shuffle_img.append(img_arrs_shuffle[i][0])

# ### Hard버전

temp_str = ' '.join(img_arrs_shuffle_img)

temp_str2 = temp_str.replace("\\", "//")

img_arrs_shuffle_img = []
img_arrs_shuffle_img = temp_str2.split()




##BLIP 시작 

def load_demo_image(image_dir,image_size,device):
    raw_image = Image.open(image_dir).convert('RGB')   

    w,h = raw_image.size
    display(raw_image.resize((w//5,h//5)))
    
    transform = transforms.Compose([
        transforms.Resize((image_size,image_size),interpolation=InterpolationMode.BICUBIC),
        transforms.ToTensor(),
        transforms.Normalize((0.48145466, 0.4578275, 0.40821073), (0.26862954, 0.26130258, 0.27577711))
        ]) 
    image = transform(raw_image).unsqueeze(0).to(device)   
    return image


import base64


image_list = ""     #인코딩

for img in img_arrs_shuffle_img:    
    with open(img, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        image_list += str(encoded_string)
        image_list += " "

img_arrs_shuffle[img_arrs_shuffle.index(answerPic)][1] = " ".join(img_arrs_shuffle[img_arrs_shuffle.index(answerPic)][1:])


#전역 변수 : captionset
captionset = str(img_arrs_shuffle.index(answerPic)) + "*" + img_arrs_shuffle[img_arrs_shuffle.index(answerPic)][1] + '*' + image_list

#BLIP VQA model
from models.blip_vqa import blip_vqa


image_size=384
image=load_demo_image(img_arrs_shuffle[img_arrs_shuffle.index(answerPic)][0],image_size=image_size,device=device)
tempimage = image


model_url = 'https://storage.googleapis.com/sfr-vision-language-research/BLIP/models/model_base_vqa_capfilt_large.pth'

global model
model_=blip_vqa(pretrained=model_url,image_size=image_size,vit='base')
model_.eval()
model_=model_.to(device)

#BLIP VQA
#함수로 



def quest(question):

    with torch.no_grad():
        answer=model_(tempimage,question,train=False,inference='generate')
        print('answer: '+answer[0])
    return answer[0]


combo = " "

from flask import Flask, render_template, request, jsonify, send_from_directory
import sys, os
app = Flask(__name__)

level = ''


picFolder = os.path.join('static', 'pics')
app.config['UPLOAD_FOLDER'] = picFolder


@app.route('/', methods = ['GET', 'POST'])
def hello():
    
    return render_template("appWeb.html")

@app.route("/reload", methods=['GET', 'POST'])     #caption >> level 
def get_level():
    content = request.get_json(silent=True)
    # level = content["level"]
   # combo = content["combo"]
    combo == 1
    level = "Easy"


        #상위 카테고리
    bigCateList =["FOOD", "VEHICLE", "ANIMAL", "SPORTS", "FURNITURE", "ETC"]

    bigCateAnswer = random.choice(bigCateList)
    #bigCateRandom = random.choice(bigCateList)

    #하위 카테고리

    if(bigCateAnswer == "FOOD"): 
        smallCateList1 =["APPLE", "BANANA", "ORANGE", "CARROT", "PIZZA", "DONUT", "CAKE"]

    elif (bigCateAnswer == "VEHICLE"):
        smallCateList1 =["BICYCLE", "CAR", "MOTORCYCLE", "AIRPLANE", "BUS", "TRAIN", "TRUCK", "BOAT"]
    
    elif(bigCateAnswer == "ANIMAL"):
        smallCateList1 =["BIRD", "CAT", "DOG", "HORSE", "SHEEP", "COW", "ELEPHANT", "BEAR", "ZEBRA", "GIRAFFE"]
    
    elif (bigCateAnswer == "SPORTS"): 
        smallCateList1 =["SKIS", "SNOWBOARD", "TENNIS", "SKATEBOARD"]
    
    elif (bigCateAnswer == "FURNITURE"): 
        smallCateList1 =["CHAIR", "BED", "TABLE", "TV", "CELL_PHONE", "BOOK", "CLOCK", "SCISSORS", "TEDDY_BEAR"]
    
    elif (bigCateAnswer == "ETC"): 
        smallCateList1 =["PERSON", "STOP_SIGN", "UMBRELLA"]
    
    smallCateAnswer = random.choice(smallCateList1)

    answerNum = random.randrange(1, 102)

    imgNumAnswer = smallCateAnswer.lower() + str(answerNum)  # 1이상 102미만 

    answerPic = json_file[bigCateAnswer][smallCateAnswer][imgNumAnswer]     #정답
    
    tmp_answer= " ".join(answerPic)
    tmp_answer2 = tmp_answer.replace("\\","//")
    answerPic = []
    answerPic = tmp_answer2.split()

#    sameCatePic = json_file[bigCateAnswer][smallCateAnswer]         #같은 카테고리


    wordCnt = answerPic[1].count(" ")

    if(level == "Easy"):   ###Easy버전

        while(wordCnt >= 10) :
                    #상위 카테고리
            bigCateList =["FOOD", "VEHICLE", "ANIMAL", "SPORTS", "FURNITURE", "ETC"]

            bigCateAnswer = random.choice(bigCateList)
            #bigCateRandom = random.choice(bigCateList)

            #하위 카테고리

            if(bigCateAnswer == "FOOD"): 
                smallCateList1 =["APPLE", "BANANA", "ORANGE", "CARROT", "PIZZA", "DONUT", "CAKE"]

            elif (bigCateAnswer == "VEHICLE"):
                smallCateList1 =["BICYCLE", "CAR", "MOTORCYCLE", "AIRPLANE", "BUS", "TRAIN", "TRUCK", "BOAT"]
            
            elif(bigCateAnswer == "ANIMAL"):
                smallCateList1 =["BIRD", "CAT", "DOG", "HORSE", "SHEEP", "COW", "ELEPHANT", "BEAR", "ZEBRA", "GIRAFFE"]
            
            elif (bigCateAnswer == "SPORTS"): 
                smallCateList1 =["SKIS", "SNOWBOARD", "TENNIS", "SKATEBOARD"]
            
            elif (bigCateAnswer == "FURNITURE"): 
                smallCateList1 =["CHAIR", "BED", "TABLE", "TV", "CELL_PHONE", "BOOK", "CLOCK", "SCISSORS", "TEDDY_BEAR"]
            
            elif (bigCateAnswer == "ETC"): 
                smallCateList1 =["PERSON", "STOP_SIGN", "UMBRELLA"]
            
            smallCateAnswer = random.choice(smallCateList1)

            answerNum = random.randrange(1, 102)
            imgNumAnswer = smallCateAnswer.lower() + str(answerNum)  # 1이상 102미만 

            answerPic = json_file[bigCateAnswer][smallCateAnswer][imgNumAnswer]     #정답
            tmp_answer= " ".join(answerPic)
            tmp_answer2 = tmp_answer.replace("\\","//")
            answerPic = []
            answerPic = tmp_answer2.split()

        #    sameCatePic = json_file[bigCateAnswer][smallCateAnswer]         #같은 카테고리
            wordCnt = answerPic[1].count(" ")

        if(combo == 1 or combo == 2 or combo == 3):        

            img_arrs = []       #image 3x3 출력용, == pictures2
            CateList = [" "]

            img_arrs.append(answerPic)
            Number2 = []         # == lotto2


            while len(Number2) < 6 :     # 3x3이라서 8개(정답 제외)의 '랜덤 그림'
                a = random.randint(1, 101)
                if a not in Number2:
                    Number2.append(a)
                    bigCateRandom = random.choice(bigCateList)
                
                    if(bigCateRandom == "FOOD"): 
                        smallCateList2 =["APPLE", "BANANA", "ORANGE", "CARROT", "PIZZA", "DONUT", "CAKE"]

                    elif (bigCateRandom == "VEHICLE"):
                        smallCateList2 =["BICYCLE", "CAR", "MOTORCYCLE", "AIRPLANE", "BUS", "TRAIN", "TRUCK", "BOAT"]
            
                    elif(bigCateRandom == "ANIMAL"):
                        smallCateList2 =["BIRD", "CAT", "DOG", "HORSE", "SHEEP", "COW", "ELEPHANT", "BEAR", "ZEBRA", "GIRAFFE"]
            
                    elif (bigCateRandom == "SPORTS"): 
                        smallCateList2 =["SKIS", "SNOWBOARD", "TENNIS", "SKATEBOARD"]
            
                    elif (bigCateRandom == "FURNITURE"): 
                        smallCateList2 =["CHAIR", "BED", "TABLE", "TV", "CELL_PHONE", "BOOK", "CLOCK", "SCISSORS", "TEDDY_BEAR"]
            
                    elif (bigCateRandom == "ETC"): 
                        smallCateList2 =["PERSON", "STOP_SIGN", "UMBRELLA"]
                    
                    smallCateRandom = random.choice(smallCateList2)
                    CateList.append(smallCateRandom)        #AA

                    img_arrs.append(json_file[bigCateRandom][smallCateRandom][smallCateRandom.lower()+str(a)])

            Number3 = [answerNum]    #lotto3

            while len(Number3) < 3 :     # 3x3이라서 8개(정답 제외)의 '같은 카테고리 그림'
                b = random.randint(1, 101)
                if b not in Number3:
                    Number3.append(b)
                    img_arrs.append(json_file[bigCateAnswer][smallCateAnswer][smallCateAnswer.lower()+str(b)])
                    CateList.append(smallCateAnswer)        #AA

            img_arrs_shuffle = random.sample(img_arrs, len(img_arrs))


            img_arrs_shuffle_img = []
            for i in range(9):
                img_arrs_shuffle_img.append(img_arrs_shuffle[i][0])

            temp_str = ' '.join(img_arrs_shuffle_img)

            temp_str2 = temp_str.replace("\\", "//")

            img_arrs_shuffle_img = []
            img_arrs_shuffle_img = temp_str2.split()
            
            

        elif(combo == 4 or combo == 5 or combo == 6):        

            img_arrs = []       #image 3x3 출력용, == pictures2
            CateList = [" "]

            img_arrs.append(answerPic)
            Number2 = []         # == lotto2


            while len(Number2) < 5 :     # 3x3이라서 8개(정답 제외)의 '랜덤 그림'
                a = random.randint(1, 101)
                if a not in Number2:
                    Number2.append(a)
                    bigCateRandom = random.choice(bigCateList)
                
                    if(bigCateRandom == "FOOD"): 
                        smallCateList2 =["APPLE", "BANANA", "ORANGE", "CARROT", "PIZZA", "DONUT", "CAKE"]

                    elif (bigCateRandom == "VEHICLE"):
                        smallCateList2 =["BICYCLE", "CAR", "MOTORCYCLE", "AIRPLANE", "BUS", "TRAIN", "TRUCK", "BOAT"]
            
                    elif(bigCateRandom == "ANIMAL"):
                        smallCateList2 =["BIRD", "CAT", "DOG", "HORSE", "SHEEP", "COW", "ELEPHANT", "BEAR", "ZEBRA", "GIRAFFE"]
            
                    elif (bigCateRandom == "SPORTS"): 
                        smallCateList2 =["SKIS", "SNOWBOARD", "TENNIS", "SKATEBOARD"]
            
                    elif (bigCateRandom == "FURNITURE"): 
                        smallCateList2 =["CHAIR", "BED", "TABLE", "TV", "CELL_PHONE", "BOOK", "CLOCK", "SCISSORS", "TEDDY_BEAR"]
            
                    elif (bigCateRandom == "ETC"): 
                        smallCateList2 =["PERSON", "STOP_SIGN", "UMBRELLA"]
                    
                    smallCateRandom = random.choice(smallCateList2)
                    CateList.append(smallCateRandom)        #AA

                    img_arrs.append(json_file[bigCateRandom][smallCateRandom][smallCateRandom.lower()+str(a)])

            Number3 = [answerNum]    #lotto3

            while len(Number3) < 4 :     # 3x3이라서 8개(정답 제외)의 '같은 카테고리 그림'
                b = random.randint(1, 101)
                if b not in Number3:
                    Number3.append(b)
                    img_arrs.append(json_file[bigCateAnswer][smallCateAnswer][smallCateAnswer.lower()+str(b)])
                    CateList.append(smallCateAnswer)        #AA

            img_arrs_shuffle = random.sample(img_arrs, len(img_arrs))


            img_arrs_shuffle_img = []
            for i in range(9):
                img_arrs_shuffle_img.append(img_arrs_shuffle[i][0])

            temp_str = ' '.join(img_arrs_shuffle_img)

            temp_str2 = temp_str.replace("\\", "//")

            img_arrs_shuffle_img = []
            img_arrs_shuffle_img = temp_str2.split()

        elif(combo == 7 or combo == 8 or combo == 9):        

            img_arrs = []       #image 3x3 출력용, == pictures2
            CateList = [" "]

            img_arrs.append(answerPic)
            Number2 = []         # == lotto2


            while len(Number2) < 4 :     # 3x3이라서 8개(정답 제외)의 '랜덤 그림'
                a = random.randint(1, 101)
                if a not in Number2:
                    Number2.append(a)
                    bigCateRandom = random.choice(bigCateList)
                
                    if(bigCateRandom == "FOOD"): 
                        smallCateList2 =["APPLE", "BANANA", "ORANGE", "CARROT", "PIZZA", "DONUT", "CAKE"]

                    elif (bigCateRandom == "VEHICLE"):
                        smallCateList2 =["BICYCLE", "CAR", "MOTORCYCLE", "AIRPLANE", "BUS", "TRAIN", "TRUCK", "BOAT"]
            
                    elif(bigCateRandom == "ANIMAL"):
                        smallCateList2 =["BIRD", "CAT", "DOG", "HORSE", "SHEEP", "COW", "ELEPHANT", "BEAR", "ZEBRA", "GIRAFFE"]
            
                    elif (bigCateRandom == "SPORTS"): 
                        smallCateList2 =["SKIS", "SNOWBOARD", "TENNIS", "SKATEBOARD"]
            
                    elif (bigCateRandom == "FURNITURE"): 
                        smallCateList2 =["CHAIR", "BED", "TABLE", "TV", "CELL_PHONE", "BOOK", "CLOCK", "SCISSORS", "TEDDY_BEAR"]
            
                    elif (bigCateRandom == "ETC"): 
                        smallCateList2 =["PERSON", "STOP_SIGN", "UMBRELLA"]
                    
                    smallCateRandom = random.choice(smallCateList2)
                    CateList.append(smallCateRandom)        #AA

                    img_arrs.append(json_file[bigCateRandom][smallCateRandom][smallCateRandom.lower()+str(a)])

            Number3 = [answerNum]    #lotto3

            while len(Number3) < 5 :     # 3x3이라서 8개(정답 제외)의 '같은 카테고리 그림'
                b = random.randint(1, 101)
                if b not in Number3:
                    Number3.append(b)
                    img_arrs.append(json_file[bigCateAnswer][smallCateAnswer][smallCateAnswer.lower()+str(b)])
                    CateList.append(smallCateAnswer)        #AA

            img_arrs_shuffle = random.sample(img_arrs, len(img_arrs))


            img_arrs_shuffle_img = []
            for i in range(9):
                img_arrs_shuffle_img.append(img_arrs_shuffle[i][0])

            temp_str = ' '.join(img_arrs_shuffle_img)

            temp_str2 = temp_str.replace("\\", "//")

            img_arrs_shuffle_img = []
            img_arrs_shuffle_img = temp_str2.split()

        else:        

            img_arrs = []       #image 3x3 출력용, == pictures2
            CateList = [" "]

            img_arrs.append(answerPic)
            Number2 = []         # == lotto2


            while len(Number2) < 3 :     # 3x3이라서 8개(정답 제외)의 '랜덤 그림'
                a = random.randint(1, 101)
                if a not in Number2:
                    Number2.append(a)
                    bigCateRandom = random.choice(bigCateList)
                
                    if(bigCateRandom == "FOOD"): 
                        smallCateList2 =["APPLE", "BANANA", "ORANGE", "CARROT", "PIZZA", "DONUT", "CAKE"]

                    elif (bigCateRandom == "VEHICLE"):
                        smallCateList2 =["BICYCLE", "CAR", "MOTORCYCLE", "AIRPLANE", "BUS", "TRAIN", "TRUCK", "BOAT"]
            
                    elif(bigCateRandom == "ANIMAL"):
                        smallCateList2 =["BIRD", "CAT", "DOG", "HORSE", "SHEEP", "COW", "ELEPHANT", "BEAR", "ZEBRA", "GIRAFFE"]
            
                    elif (bigCateRandom == "SPORTS"): 
                        smallCateList2 =["SKIS", "SNOWBOARD", "TENNIS", "SKATEBOARD"]
            
                    elif (bigCateRandom == "FURNITURE"): 
                        smallCateList2 =["CHAIR", "BED", "TABLE", "TV", "CELL_PHONE", "BOOK", "CLOCK", "SCISSORS", "TEDDY_BEAR"]
            
                    elif (bigCateRandom == "ETC"): 
                        smallCateList2 =["PERSON", "STOP_SIGN", "UMBRELLA"]
                    
                    smallCateRandom = random.choice(smallCateList2)
                    CateList.append(smallCateRandom)        #AA

                    img_arrs.append(json_file[bigCateRandom][smallCateRandom][smallCateRandom.lower()+str(a)])

            Number3 = [answerNum]    #lotto3

            while len(Number3) < 6 :     # 3x3이라서 8개(정답 제외)의 '같은 카테고리 그림'
                b = random.randint(1, 101)
                if b not in Number3:
                    Number3.append(b)
                    img_arrs.append(json_file[bigCateAnswer][smallCateAnswer][smallCateAnswer.lower()+str(b)])
                    CateList.append(smallCateAnswer)        #AA

            img_arrs_shuffle = random.sample(img_arrs, len(img_arrs))


            img_arrs_shuffle_img = []
            for i in range(9):
                img_arrs_shuffle_img.append(img_arrs_shuffle[i][0])
            
            temp_str = ' '.join(img_arrs_shuffle_img)

            temp_str2 = temp_str.replace("\\", "//")

            img_arrs_shuffle_img = []
            img_arrs_shuffle_img = temp_str2.split()


            

    
    

    elif(level == "Hard"):   ###Hard버전


        if(combo == 1 or combo == 2 or combo == 3) :

            img_arrs = []       #image 3x3 출력용, == pictures2
            CateList = [" "]

            img_arrs.append(answerPic)
            Number2 = []         # == lotto2


            while len(Number2) < 3 :     # 3x3이라서 8개(정답 제외)의 '랜덤 그림'
                c = random.randint(1, 101)
                if c not in Number2:
                    Number2.append(c)
                    bigCateRandom = random.choice(bigCateList)
                
                    if(bigCateRandom == "FOOD"): 
                        smallCateList2 =["APPLE", "BANANA", "ORANGE", "CARROT", "PIZZA", "DONUT", "CAKE"]

                    elif (bigCateRandom == "VEHICLE"):
                        smallCateList2 =["BICYCLE", "CAR", "MOTORCYCLE", "AIRPLANE", "BUS", "TRAIN", "TRUCK", "BOAT"]
            
                    elif(bigCateRandom == "ANIMAL"):
                        smallCateList2 =["BIRD", "CAT", "DOG", "HORSE", "SHEEP", "COW", "ELEPHANT", "BEAR", "ZEBRA", "GIRAFFE"]
            
                    elif (bigCateRandom == "SPORTS"): 
                        smallCateList2 =["SKIS", "SNOWBOARD", "TENNIS", "SKATEBOARD"]
            
                    elif (bigCateRandom == "FURNITURE"): 
                        smallCateList2 =["CHAIR", "BED", "TABLE", "TV", "CELL_PHONE", "BOOK", "CLOCK", "SCISSORS", "TEDDY_BEAR"]
            
                    elif (bigCateRandom == "ETC"): 
                        smallCateList2 =["PERSON", "STOP_SIGN", "UMBRELLA"]
                    
                    smallCateRandom = random.choice(smallCateList2)
                    CateList.append(smallCateRandom)        #AA

                    img_arrs.append(json_file[bigCateRandom][smallCateRandom][smallCateRandom.lower()+str(c)])
                    

            Number3 = [answerNum]    #lotto3

            while len(Number3) < 6 :     # 3x3이라서 8개(정답 제외)의 '같은 카테고리 그림'
                d = random.randint(1, 101)
                if d not in Number3:
                    Number3.append(d)
                    img_arrs.append(json_file[bigCateAnswer][smallCateAnswer][smallCateAnswer.lower()+str(d)])
                    CateList.append(smallCateAnswer)        #AA

            img_arrs_shuffle = random.sample(img_arrs, len(img_arrs))
            # print(img_arrs_shuffle.index(answerPic))        #정답 그림 인덱스 

            # print(img_arrs_shuffle[img_arrs_shuffle.index(answerPic)][0])  #정답 하나
            img_arrs_shuffle_img = []
            for i in range(9):
                img_arrs_shuffle_img.append(img_arrs_shuffle[i][0])

            temp_str = ' '.join(img_arrs_shuffle_img)

            temp_str2 = temp_str.replace("\\", "//")

            img_arrs_shuffle_img = []
            img_arrs_shuffle_img = temp_str2.split()

        elif(combo == 4 or combo == 5 or combo == 6) :

            img_arrs = []       #image 3x3 출력용, == pictures2
            CateList = [" "]

            img_arrs.append(answerPic)
            Number2 = []         # == lotto2


            while len(Number2) < 2 :     # 3x3이라서 8개(정답 제외)의 '랜덤 그림'
                c = random.randint(1, 101)
                if c not in Number2:
                    Number2.append(c)
                    bigCateRandom = random.choice(bigCateList)
                
                    if(bigCateRandom == "FOOD"): 
                        smallCateList2 =["APPLE", "BANANA", "ORANGE", "CARROT", "PIZZA", "DONUT", "CAKE"]

                    elif (bigCateRandom == "VEHICLE"):
                        smallCateList2 =["BICYCLE", "CAR", "MOTORCYCLE", "AIRPLANE", "BUS", "TRAIN", "TRUCK", "BOAT"]
            
                    elif(bigCateRandom == "ANIMAL"):
                        smallCateList2 =["BIRD", "CAT", "DOG", "HORSE", "SHEEP", "COW", "ELEPHANT", "BEAR", "ZEBRA", "GIRAFFE"]
            
                    elif (bigCateRandom == "SPORTS"): 
                        smallCateList2 =["SKIS", "SNOWBOARD", "TENNIS", "SKATEBOARD"]
            
                    elif (bigCateRandom == "FURNITURE"): 
                        smallCateList2 =["CHAIR", "BED", "TABLE", "TV", "CELL_PHONE", "BOOK", "CLOCK", "SCISSORS", "TEDDY_BEAR"]
            
                    elif (bigCateRandom == "ETC"): 
                        smallCateList2 =["PERSON", "STOP_SIGN", "UMBRELLA"]
                    
                    smallCateRandom = random.choice(smallCateList2)
                    CateList.append(smallCateRandom)        #AA

                    img_arrs.append(json_file[bigCateRandom][smallCateRandom][smallCateRandom.lower()+str(c)])
                    

            Number3 = [answerNum]    #lotto3

            while len(Number3) < 7 :     # 3x3이라서 8개(정답 제외)의 '같은 카테고리 그림'
                d = random.randint(1, 101)
                if d not in Number3:
                    Number3.append(d)
                    img_arrs.append(json_file[bigCateAnswer][smallCateAnswer][smallCateAnswer.lower()+str(d)])
                    CateList.append(smallCateAnswer)        #AA

            img_arrs_shuffle = random.sample(img_arrs, len(img_arrs))
            # print(img_arrs_shuffle.index(answerPic))        #정답 그림 인덱스 

            # print(img_arrs_shuffle[img_arrs_shuffle.index(answerPic)][0])  #정답 하나
            img_arrs_shuffle_img = []
            for i in range(9):
                img_arrs_shuffle_img.append(img_arrs_shuffle[i][0])

            temp_str = ' '.join(img_arrs_shuffle_img)

            temp_str2 = temp_str.replace("\\", "//")

            img_arrs_shuffle_img = []
            img_arrs_shuffle_img = temp_str2.split()

        elif(combo == 7 or combo == 8 or combo == 9) :

            img_arrs = []       #image 3x3 출력용, == pictures2
            CateList = [" "]

            img_arrs.append(answerPic)
            Number2 = []         # == lotto2


            while len(Number2) < 1 :     # 3x3이라서 8개(정답 제외)의 '랜덤 그림'
                c = random.randint(1, 101)
                if c not in Number2:
                    Number2.append(c)
                    bigCateRandom = random.choice(bigCateList)
                
                    if(bigCateRandom == "FOOD"): 
                        smallCateList2 =["APPLE", "BANANA", "ORANGE", "CARROT", "PIZZA", "DONUT", "CAKE"]

                    elif (bigCateRandom == "VEHICLE"):
                        smallCateList2 =["BICYCLE", "CAR", "MOTORCYCLE", "AIRPLANE", "BUS", "TRAIN", "TRUCK", "BOAT"]
            
                    elif(bigCateRandom == "ANIMAL"):
                        smallCateList2 =["BIRD", "CAT", "DOG", "HORSE", "SHEEP", "COW", "ELEPHANT", "BEAR", "ZEBRA", "GIRAFFE"]
            
                    elif (bigCateRandom == "SPORTS"): 
                        smallCateList2 =["SKIS", "SNOWBOARD", "TENNIS", "SKATEBOARD"]
            
                    elif (bigCateRandom == "FURNITURE"): 
                        smallCateList2 =["CHAIR", "BED", "TABLE", "TV", "CELL_PHONE", "BOOK", "CLOCK", "SCISSORS", "TEDDY_BEAR"]
            
                    elif (bigCateRandom == "ETC"): 
                        smallCateList2 =["PERSON", "STOP_SIGN", "UMBRELLA"]
                    
                    smallCateRandom = random.choice(smallCateList2)
                    CateList.append(smallCateRandom)        #AA

                    img_arrs.append(json_file[bigCateRandom][smallCateRandom][smallCateRandom.lower()+str(c)])
                    

            Number3 = [answerNum]    #lotto3

            while len(Number3) < 8 :     # 3x3이라서 8개(정답 제외)의 '같은 카테고리 그림'
                d = random.randint(1, 101)
                if d not in Number3:
                    Number3.append(d)
                    img_arrs.append(json_file[bigCateAnswer][smallCateAnswer][smallCateAnswer.lower()+str(d)])
                    CateList.append(smallCateAnswer)        #AA

            img_arrs_shuffle = random.sample(img_arrs, len(img_arrs))

            img_arrs_shuffle_img = []
            for i in range(9):
                img_arrs_shuffle_img.append(img_arrs_shuffle[i][0])

            temp_str = ' '.join(img_arrs_shuffle_img)

            temp_str2 = temp_str.replace("\\", "//")

            img_arrs_shuffle_img = []
            img_arrs_shuffle_img = temp_str2.split()

        else:

            img_arrs = []       #image 3x3 출력용, == pictures2
            CateList = [" "]

            img_arrs.append(answerPic)

            Number3 = [answerNum]    #lotto3

            while len(Number3) < 9 :     # 3x3이라서 8개(정답 제외)의 '같은 카테고리 그림'
                d = random.randint(1, 101)
                if d not in Number3:
                    Number3.append(d)
                    img_arrs.append(json_file[bigCateAnswer][smallCateAnswer][smallCateAnswer.lower()+str(d)])
                    CateList.append(smallCateAnswer)        #AA

            img_arrs_shuffle = random.sample(img_arrs, len(img_arrs))

            img_arrs_shuffle_img = []
            for i in range(9):
                img_arrs_shuffle_img.append(img_arrs_shuffle[i][0])

            temp_str = ' '.join(img_arrs_shuffle_img)
            temp_str2 = temp_str.replace("\\", "//")
            img_arrs_shuffle_img = []
            img_arrs_shuffle_img = temp_str2.split()

    import base64

    global image_list     #인코딩
    image_list = ""
    for img in img_arrs_shuffle_img:    
        with open(img, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            image_list += str(encoded_string)
            image_list += " "



    global image
    global tempimage
    tempimage = image
    image_size=384
    image=load_demo_image(img_arrs_shuffle[img_arrs_shuffle.index(answerPic)][0],image_size=image_size,device=device)

    img_arrs_shuffle[img_arrs_shuffle.index(answerPic)][1] = " ".join(img_arrs_shuffle[img_arrs_shuffle.index(answerPic)][1:])

    global captionset
    captionset = str(img_arrs_shuffle.index(answerPic)) + '*' + img_arrs_shuffle[img_arrs_shuffle.index(answerPic)][1] + '*' + image_list

    return "success"


@app.route("/vqa", methods=['POST'])
def update_name():
    content = request.get_json(silent=True)

    return quest(content["question"])   #key값을 question으로 설정

@app.route("/caption", methods=['GET'])
def get_cap():

    return captionset
        


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

