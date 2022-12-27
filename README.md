# 프로젝트명
2022 SKKU 산학 협력 프로젝트 / 웅진씽크빅 / Talking NPC / VisualGame

2022년도 웅진씽크빅 기업과 함께한 산학 협력 프로젝트

<br>

> 영어로 진행되는 게임으로, 여러 가지 그림 중 정답 그림을 맞춰가는 게임입니다.

> 정답 그림에 대한 힌트(Caption)가 제공되고, 영어로 질문하면 visual question answering model인 ‘BLIP’이 질문에 대한 답변을 진행합니다.

<br>
<br>
<br>

## BLIP : Bootstrapping Language-Image Pre-training for Unified Vision-Language Understanding and Generation

<br>

[BLIP 논문](https://arxiv.org/abs/2201.12086)

[BLIP Github](https://github.com/salesforce/BLIP)

Vision-Language Pre-training(VLP)는 vision-language taks의 성능을 매우 향상시켜주었다. 하지만 현재 존재하는 pre-trained model들은 웹에서 수집된 image-text에 대한 dataset을 이용하는데, 이는 최적의 상태가 아닌 단점이 있다. 그리하여 소개될 모델인 ‘BLIP’은 새로운 VLP framework로, 불필요한 웹 data를 ‘bootstrapping’하는 방식을 이용하여 불필요한 정보를 효과적으로 제거하는 방식을 이용하였다.

<br>

![123](https://user-images.githubusercontent.com/104834390/209679867-8bfb6d54-2f1d-455b-a91a-bed964424df4.gif)

<br>
<br>

BLIP은 4가지의 model version이 존재하여 필요한 모델을 선택하여 사용하면 됩니다.

 1. Image Captioning
 2. VQA
 3. Feature Extraction
 4. Image Text Matching


해당 기능을 확인하고 싶으면 [BLIP Colab](https://colab.research.google.com/github/salesforce/BLIP/blob/main/demo.ipynb#scrollTo=6835daef)에서 확인해보실 수 있습니다.

이 외에도 [Web 데모](https://huggingface.co/spaces/Salesforce/BLIP)를 통해서도 확인해보실 수 있습니다.

<br>
<br>

### BLIP 실행 방법 (Colab 기준)
<br>
<br>

1. 우선 BLIP model에게 필요한 모듈을 설치해주고, BLIP의 github 주소를 git clone해줍니다.

```
# install requirements
import sys
if 'google.colab' in sys.modules:
    print('Running in Colab.')
    !pip3 install transformers==4.15.0 timm==0.4.12 fairscale==0.4.4
    !git clone https://github.com/salesforce/BLIP
    %cd BLIP
```
<br>

2. img_url 부분에 본인이 원하는 이미지 주소를 첨부하고 셀을 재생시킵니다.

```
from PIL import Image
import requests
import torch
from torchvision import transforms
from torchvision.transforms.functional import InterpolationMode

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def load_demo_image(image_size,device):
    img_url = 'https://storage.googleapis.com/sfr-vision-language-research/BLIP/demo.jpg'    #본인이 원하는 이미지 주소 넣기
    raw_image = Image.open(requests.get(img_url, stream=True).raw).convert('RGB')   

    w,h = raw_image.size
    display(raw_image.resize((w//5,h//5)))
    
    transform = transforms.Compose([
        transforms.Resize((image_size,image_size),interpolation=InterpolationMode.BICUBIC),
        transforms.ToTensor(),
        transforms.Normalize((0.48145466, 0.4578275, 0.40821073), (0.26862954, 0.26130258, 0.27577711))
        ]) 
    image = transform(raw_image).unsqueeze(0).to(device)   
    return image
 
```
<br>

3. 그 뒤 원하는 task의 셀을 재생하면 그에 맞는 답변을 해줍니다.



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

```
BLIP
 ┣ configs
 ┃ ┣ bert_config.json
 ┃ ┣ caption_coco.yaml
 ┃ ┣ med_config.json
 ┃ ┣ nlvr.yaml
 ┃ ┣ nocaps.yaml
 ┃ ┣ pretrain.yaml
 ┃ ┣ retrieval_coco.yaml
 ┃ ┣ retrieval_flickr.yaml
 ┃ ┣ retrieval_msrvtt.yaml
 ┃ ┗ vqa.yaml
 ┣ models
 ┃ ┣ __pycache__
 ┃ ┃ ┣ blip.cpython-38.pyc
 ┃ ┃ ┣ blip.cpython-39.pyc
 ┃ ┃ ┣ blip_vqa.cpython-38.pyc
 ┃ ┃ ┣ blip_vqa.cpython-39.pyc
 ┃ ┃ ┣ med.cpython-38.pyc
 ┃ ┃ ┣ med.cpython-39.pyc
 ┃ ┃ ┣ vit.cpython-38.pyc
 ┃ ┃ ┣ vit.cpython-39.pyc
 ┃ ┃ ┣ __init__.cpython-38.pyc
 ┃ ┃ ┗ __init__.cpython-39.pyc
 ┃ ┣ blip.py
 ┃ ┣ blip_itm.py
 ┃ ┣ blip_nlvr.py
 ┃ ┣ blip_pretrain.py
 ┃ ┣ blip_retrieval.py
 ┃ ┣ blip_vqa.py
 ┃ ┣ med.py
 ┃ ┣ nlvr_encoder.py
 ┃ ┣ vit.py
 ┃ ┗ __init__.py
 ┣ image_set 
 ┣ answer.txt
 ┗ final.py
requirements.txt
```
<br>
<br>

- final.py : 유니티와의 연동을 위한 파일입니다.
- image_set : 게임에서 사용된 image_set 폴더입니다. 추가적인 설명은 밑에서 진행하겠습니다.
- configs, models : BLIP model을 구동하기 위해 필요한 파일들입니다.
- answer.txt : 정답 그림에 대한 경로를 임시저장하는 파일입니다.



<br>
<br>
<br>

## 사용 예제

1. 게임에 들어가게 되면 Easy / Hard로 게임 난이도를 선택할 수 있습니다.

  Easy는 힌트(Caption)단어가 5개 이하이며 같은 카테고리에 있는 그림들(3개)이 적게 나타나고, Hard는 힌트(Caption)단어가 6개 이상이며 같은 카테고리에 있는 그림들(6개)이 많이 나타납니다.

2. 난이도를 선택하면, 그림 세트와 Hint가 주어지고, Ai에게 질문을 합니다.

3. 질문을 하면, Ai가 정답 그림에 대한 답변을 해주게 됩니다.<br>

4. 정답인 것 같은 그림에 O 버튼을 드래그하여 문제를 맞출 수 있습니다.<br>

### Process

1. 게임이 시작되면, 난이도에 맞는 caption과 이미지를 선정하고, 다른 카테고리에 있는 이미지들을 랜덤으로 선정합니다.

2. 정답 이미지와 함께 저장되어 있는 설명(caption)을 유저에게 전달하고, BLIP에게 정답 이미지를 전달해줍니다.

3. 유저가 질문을 하면 request를 받아 서버에 전달합니다.

4. BLIP 모델이 질문을 해석하여 정답을 도출하고, 다시 유니티로 전달해줍니다.

5. 해당 그림을 맞춘다면, 다음 게임으로 넘어가지만, 틀릴 경우 목숨이 감소합니다.

<br>
<br>
<br>


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

  COCO Dataset Link : [COCO Dataset](https://cocodataset.org/#home)
  
  
<br>
<br>
<br>

## Reference

- [BLIP 논문](https://arxiv.org/abs/2201.12086)

- [BLIP Github](https://github.com/salesforce/BLIP)

- [COCO Dataset](https://cocodataset.org/#home)
