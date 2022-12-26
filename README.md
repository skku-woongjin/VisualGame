# 프로젝트명
2022 SKKU 산학 협력 프로젝트 / 웅진씽크빅 / Talking NPC / VisualGame

2022년도 웅진씽크빅 기업과 함께한 산학 협력 프로젝트

<br>

> 영어로 진행되는 게임으로, 여러 가지 그림 중 정답 그림을 맞춰가는 게임입니다.

> 정답 그림에 대한 힌트(Caption)가 제공되고, 영어로 질문하면 visual question answering model인 ‘BLIP’이 질문에 대한 답변을 진행합니다.

![vg바탕](https://user-images.githubusercontent.com/104834390/209525193-a965eaed-e5f9-4b63-adf6-155d823b2e1a.png)
<br>
<br>
<br>
<br>

## 프로젝트 소개

<p align="justify">
프로젝트 개요/동기

기업의 니즈에 맞춰 아이가 웅진 메타버스 플랫폼 안에서 재미있게 학습을 할 수 있는 방법에 대한 솔루션을 제공하고자 하였습니다.

따라서 게임 형식을 통해 아이들의 흥미를 유발하였고, 게임이 영어로 진행되도록 하여 영어를 자연스럽게 학습할 수 있도록 하였습니다.

</p>

<p align="center">

</p>

<br>

## 기술 스택

| Python |
| :--------: |

<br>
<br>
<br>

## Framework
Flask / AWS EC2

<br>
<br>
<br>

## 설치 방법

### Clone Repository

```sh
git clone https://github.com/Taerogrammer/VisualGame.git
```

### Prerequisites

```sh
pip install -r requirements.txt
```

<br>
<br>
<br>

## 파일 구조

📦BLIP

 ┣ 📂configs
 
 ┃ ┣ 📜bert_config.json
 
 ┃ ┣ 📜caption_coco.yaml
 
 ┃ ┣ 📜med_config.json
 
 ┃ ┣ 📜nlvr.yaml
 
 ┃ ┣ 📜nocaps.yaml
 
 ┃ ┣ 📜pretrain.yaml
 
 ┃ ┣ 📜retrieval_coco.yaml
 
 ┃ ┣ 📜retrieval_flickr.yaml
 
 ┃ ┣ 📜retrieval_msrvtt.yaml
 
 ┃ ┗ 📜vqa.yaml
 
 ┣ 📂static
 
 ┃ ┣ 📂image_set
 
 ┃ ┣ 📜background.jpg
 
 ┃ ┣ 📜checkbox.js
 
 ┃ ┣ 📜checklistWeb.js
 
 ┃ ┣ 📜DATA.json
 
 ┃ ┣ 📜divide.css
 
 ┃ ┣ 📜loading.js
 
 ┃ ┣ 📜multi.js
 
 ┃ ┣ 📜multiCSS.css
 
 ┃ ┗ 📜style.css
 
 ┣ 📂templates
 
 ┃ ┣ 📜appWeb.html
 
 ┃ ┗ 📜reload.html
 
 ┣ 📂transform
 
 ┃ ┗ 📜randaugment.py
 
 ┣ 📂__pycache__
 
 ┃ ┗ 📜app.cpython-39.pyc
 
 ┣ 📜final.py
 
 ┗ 📜requirements.txt

<br>
<br>

- final.py : 유니티와의 연동을 위한 파일입니다.
- image_set : 게임에서 사용된 iamge_set 입니다. 추가적인 설명은 밑에서 진행하겠습니다.


## 사용 예제

1. 게임에 들어가게 되면 Easy / Hard로 게임 난이도를 선택할 수 있습니다.

  Easy는 힌트(Caption)단어가 5개 이하이며 같은 카테고리에 있는 그림들(3개)이 적게 나타나고, Hard는 힌트(Caption)단어가 6개 이상이며 같은 카테고리에 있는 그림들(6개)이 많이 나타납니다.

2. 난이도를 선택하면, 그림 세트와 Hint가 주어지고, Ai에게 질문을 합니다.

3. 질문을 하면, Ai가 정답 그림에 대한 답변을 해주게 됩니다.<br>

![vg1](https://user-images.githubusercontent.com/104834390/209526458-9d19addb-a991-47cc-84ac-2c1a3bf8e7e0.png)

4. 정답인 것 같은 그림에 O 버튼을 드래그하여 문제를 맞출 수 있습니다.<br>

![vg2](https://user-images.githubusercontent.com/104834390/209526620-e87a3b0a-93ac-4a35-ac58-6a425fa7b0a5.png)

### Process

1. 게임이 시작되면, 난이도에 맞는 caption과 image를 선정하고, 다른 카테고리에 있는 이미지들은 랜덤으로 선정됩니다.

2. 유저가 질문을 하면 request를 받아 서버에 전달합니다

3. BLIP 모델이 질문을 해석하여 정답을 도출하고, 다시 유니티로 전달해줍니다.

4. 해당 그림을 맞춘다면, 다음 게임으로 넘어가지만, 틀릴 경우 목숨이 감소합니다.

<br>
<br>
<br>

## 시연 영상

- 파일 용량 이슈로, 2배속으로 진행하였습니다.

https://user-images.githubusercontent.com/104834390/209529166-473830ea-8ba8-422f-a445-8dd98aa598b1.mov


## API 설명

### /reload [POST]

- 유니티 내부에서 질문을 하면, 질문에 대한 답변을 해줍니다. 

Request
```
{ "question' : "what color?" }
```

Response 
```
{ "answer" : "gray" }
```


### Dataset

- COCO Image set을 이용하여 이미지들을 구성하였습니다.

- 6가지의 카테고리로 나누었고, 그 안에서 또 세부적으로 나누었습니다.

### Iamge Categories

 ┣ 📂ANIMAL
 
 ┃ ┣ 📂bear, bird, cat, cow, dog, elephant, giraffe, horse, sheep, zebra
 
 ┣ 📂ETC
 
 ┃ ┣ 📂person, stop_sign, umbrella
 
 ┣ 📂FOOD
 
 ┃ ┣ 📂apple, banana, cake, carrot, donut, orange, pizza
 
 ┣ 📂FURNITURE
 
 ┃ ┣ 📂bed, bench, book, cell_phone, chair, clock, scissors, table, teddy_bear, tv
 
 ┣ 📂SPORTS
 
 ┃ ┣ 📂skateboard, skis, snowboard, tennis
 
 ┣ 📂VEHICLE
 
 ┃ ┣ 📂airplane, bicycle, boat, bus, car, motorcycle, train, truck
 
 
<br>
- 상위 카테고리 : ANIMAL, ETC, FOOD, FURNITURE, SPORTS, VEHICLE

- 하위 카테고리 : 상위 폴더 밑에 있는 카테고리 (bear, bird, cat ...) 

- 하위 카테고리 안에 각각 100가지의 그림들이 들어가 있습니다.

- 난이도 조절에서 선택되는 같은 카테고리의 기준은 하위 카테고리입니다.
