
Traffic Sign Detection with Integrated Learning
실제·합성 데이터 통합 학습을 통한 교통 표지 인식 일반화 성능 분석

 프로젝트 개요
본 프로젝트는 소량의 실제 교통 표지 데이터 환경에서 객체 탐지 모델의 일반화 성능을 향상시키기 위한 데이터 구성 전략을 분석하는 것을 목표로 한다. 실제 데이터, 실제 기반 증강 데이터, 합성 데이터, 그리고 이들을 결합한 통합 학습(Integrated Learning) 방식을 비교하여, 데이터 출처와 구성 방식이 모델 성능에 미치는 영향을 정량적으로 평가하였다.
YOLO 계열 단일 단계 탐지 모델과 Faster R-CNN 기반 이중 단계 탐지 모델을 사용하여, 데이터 의존성과 모델 구조 차이에 따른 성능 변화를 분석하였다.

 연구 목적
* 소량의 실제 데이터만으로 학습할 경우 발생하는 일반화 성능 한계 분석
* 합성 데이터 단독 학습의 효과와 한계 검증
* 실제 데이터와 합성 데이터를 결합한 통합 학습 전략의 유효성 평가
* 서로 다른 객체 탐지 모델 구조(YOLO vs Faster R-CNN)의 데이터 활용 특성 비교

 데이터셋 구성
데이터셋	설명
A	실제 교통 표지 이미지로만 구성된 소량 데이터셋 (416×416, 254장)
A_aug	실제 데이터 기반 증강 데이터셋 (회전, 밝기, 감마, 블러 등)
1stAug	환경적 변화 반영 합성 데이터셋 (PNG 객체 기반)
2ndAug	영상 왜곡(모션 블러, 가우시안 블러) 반영 합성 데이터셋
A+1stAug	실제 데이터 + 1차 합성 데이터 통합 학습
A+2ndAug	실제 데이터 + 2차 합성 데이터 통합 학습
B	학습에 사용하지 않은 실제 테스트 데이터셋 (640×640, 837장)
모든 실험은 **동일한 테스트 데이터셋(B)**을 사용하여 공정하게 비교하였다.

 실험 설정
* 모델
    * YOLOv8n
    * YOLO11n
    * Faster R-CNN (ResNet-50 + FPN)
* 학습 방식
    * From-scratch 학습 (사전 학습 가중치 미사용)
    * 동일한 입력 해상도 및 평가 조건 유지
* 평가 지표
    * Precision (P)
    * Recall (R)
    * F1-score
    * mAP@50
    * mAP@50–95
    * AR@100 (일부 실험)

 주요 실험 결과 요약
* 실제 데이터(A) 단독 학습은 모든 모델에서 일반화 성능이 제한적임을 확인
* 실제 데이터 기반 증강(A_aug)은 성능을 개선하였으나, 복잡한 테스트 환경 대응에는 한계 존재
* 합성 데이터 단독 학습(1stAug, 2ndAug)은 데이터 수가 많음에도 불구하고 현실 적합성 부족으로 성능 저하
* 실제·합성 데이터 통합 학습(A+1stAug, A+2ndAug) 조건에서 모든 모델이 최고 성능 기록
* Faster R-CNN은 통합 학습 조건에서 가장 큰 성능 향상을 보이며, 데이터 다양성 활용도가 높음을 확인
 데이터 수 증가보다 데이터 출처의 다양성이 일반화 성능에 더 중요함을 실험적으로 검증

 기술 스택
모델 
* YOLOv8n
* YOLO11n
* Faster R-CNN (ResNet-50 + FPN)
프레임워크
* PyTorch
* Ultralytics YOLO
데이터 처리 / 증강
* OpenCV
* NumPy
* Custom augmentation scripts (rotation, scale, beta/gamma adjustment, Gaussian blur, motion blur)
평가 및 분석
* COCO Evaluation Metrics
* FPS 및 GPU 메모리 사용량 측정
개발 환경
* Python 3.8
* CUDA / GPU
* Windows + VS Code
