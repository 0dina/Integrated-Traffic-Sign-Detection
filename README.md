
# 교통 표지 객체 검출을 위한 실제–합성 데이터 통합 학습

**Integrated Learning for Traffic Sign Detection using Real and Synthetic Data**

---

## 프로젝트 개요 (Overview)

본 프로젝트는 **소량의 실제 교통 표지 데이터 환경에서 학습 데이터 구성 방식이 객체 검출 모델의 일반화 성능에 미치는 영향**을 분석한다.
실제 데이터, 실제 데이터 기반 증강 데이터, 합성 데이터, 그리고 **실제·합성 데이터를 결합한 통합 학습 전략**을 단계적으로 비교하였다.

단일 단계 검출기(YOLO 계열)와 이단계 검출기(Faster R-CNN)를 함께 사용하여, **모델 구조에 따른 데이터 민감도 차이**도 함께 분석한다.

---

This project investigates **how different training data compositions affect the generalization performance of traffic sign detection models** under limited real-world data conditions.
We systematically compare real data, augmented real data, synthetic data, and **integrated learning combining real and synthetic datasets**.

Both **single-stage detectors (YOLO series)** and a **two-stage detector (Faster R-CNN)** are evaluated to analyze architectural sensitivity to data diversity.

---

## 연구 목적 (Objectives)

* 소량의 실제 데이터만으로 학습할 때 발생하는 한계 분석
* 합성 데이터 단독 학습의 효과와 한계 검증
* 실제·합성 데이터 통합 학습의 일반화 성능 향상 효과 분석
* YOLO 계열과 Faster R-CNN 간 데이터 의존성 차이 비교

* Analyze limitations of training with small-scale real-world datasets
* Evaluate effectiveness and drawbacks of synthetic-only training
* Verify generalization improvement via integrated learning
* Compare data sensitivity between YOLO-based and Faster R-CNN-based detectors

---

## 데이터셋 구성 (Dataset Configuration)

| Dataset  | Description                                                           |
| -------- | --------------------------------------------------------------------- |
| A        | Real-world dataset only (416×416, 254 images)                         |
| A_aug    | Augmented real dataset (rotation, brightness, gamma, blur)            |
| 1stAug   | Synthetic dataset reflecting environmental variations                 |
| 2ndAug   | Synthetic dataset including image distortion effects                  |
| A+1stAug | Integrated dataset (real + 1st synthetic)                             |
| A+2ndAug | Integrated dataset (real + 2nd synthetic)                             |
| B        | Real-world test dataset (640×640, 837 images, unseen during training) |

* 모든 실험은 동일한 테스트 데이터셋 **B**를 사용하여 평가함
* 데이터 구성 방식 외의 조건은 동일하게 유지

---

## 실험 환경 및 모델 (Experimental Setup)

### 모델 (Models)

| Model                          | Type                  |
| ------------------------------ | --------------------- |
| YOLOv8n                        | Single-stage detector |
| YOLO11n                        | Single-stage detector |
| Faster R-CNN (ResNet-50 + FPN) | Two-stage detector    |

### 학습 조건 (Training)

* 사전 학습 가중치 미사용 (from scratch)
* 동일한 입력 크기 및 평가 조건 적용
* 데이터 구성만 변경하여 비교

### 평가 지표 (Metrics)

* Precision (P)
* Recall (R)
* F1-score
* mAP@0.5
* mAP@0.5:0.95
* AR@100

---

## 주요 실험 결과 요약 (Key Results)

### 한글 요약

* 실제 데이터(A) 단독 학습은 모든 모델에서 일반화 성능이 제한적
* 실제 데이터 기반 증강(A_aug)은 성능을 개선하나 한계 존재
* 합성 데이터 단독 학습은 데이터 양 대비 성능이 매우 낮음
* **실제·합성 데이터 통합 학습(A+Aug)** 조건에서 모든 모델이 최고 성능 달성
* Faster R-CNN은 통합 학습 조건에서 가장 큰 성능 향상을 보임

### English Summary

* Real-only training shows limited generalization
* Augmented real data improves performance but remains insufficient
* Synthetic-only training performs poorly despite large data volume
* **Integrated learning achieves the best performance across all models**
* Faster R-CNN benefits most from real–synthetic data integration

---

## 기술 스택 (Technology Stack)

### 모델 및 프레임워크

| Category         | Tools                        |
| ---------------- | ---------------------------- |
| Deep Learning    | PyTorch                      |
| Detection Models | YOLOv8, YOLO11, Faster R-CNN |
| Framework        | Ultralytics YOLO             |

### 데이터 처리 및 증강

| Category         | Tools                                                            |
| ---------------- | ---------------------------------------------------------------- |
| Image Processing | OpenCV                                                           |
| Data Handling    | NumPy                                                            |
| Augmentation     | Rotation, Scaling, Brightness, Gamma, Gaussian Blur, Motion Blur |

### 평가 및 실험 환경

| Category     | Details                       |
| ------------ | ----------------------------- |
| Evaluation   | COCO metrics                  |
| Benchmarking | FPS, GPU memory usage         |
| Environment  | Python 3.8, CUDA GPU, Windows |

---

## 연구 의의 (Contributions)


본 연구는 합성 데이터가 단독으로는 한계를 가지지만, 실제 데이터와 결합될 경우 **도메인 정규화 역할을 수행하여 일반화 성능을 크게 향상시킨다**는 점을 실험적으로 입증한다.
이는 제한된 실제 데이터 환경에서 효과적인 학습 전략 수립에 중요한 시사점을 제공한다.

This work empirically demonstrates that **synthetic data alone is insufficient**, but when combined with real data, it effectively regularizes the learned representation toward the real-world domain.
The findings provide practical guidance for data-efficient training in resource-constrained environments.

