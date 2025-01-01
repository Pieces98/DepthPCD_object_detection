# Depth Camera based object detection

## Introduction
이 프로젝트는 **[ROS2와 AI를 활용한 자율주행 로봇개발자 부트캠프 2기](https://github.com/addinedu-advance-2nd)**(24.10.28-24.12.27)에서 [2차 프로젝트](https://github.com/addinedu-advance-2nd/storagy-repo-3)로 진행된 [Storagy로봇](https://xyzcorp.io/storagy)을 사용한 서비스 제작 중 Depth Camera를 활용한 장애물 감지 기능 구현의 연장 프로젝트입니다. 

## Sensor

- LiDAR: sick tim571
- Depth Camera: Orbbec Astra Stereo S U3.0

<p align="center">
  <img src="./assets/sample_data.gif">
</p>


## Goal 
이 프로젝트의 목표는 다음과 같습니다. 

- ROS2 토픽으로 발행되는 LiDAR, Depth Camera의 정보를 활용하여 ROS2 Navigation2 패키지에서 costmap에 반영할 수 있는 토픽 발행
  - Ubuntu 22.04 Jammy, ROS2 Humble 환경에서의 동작을 목표
- GPU, 인터넷이 없는 환경에서 CPU만을 활용하여 10Hz의 속도로 정보 갱신

## Todo

#### Pointcloud
- [ ] 좌표 변환 및 ROI 제한
- [ ] (Optional) 땅 제거
- [ ] (Optional) LiDAR에서 감지되는 장애물(ex-벽) 제거

#### RGB Image
- [ ] Pointcloud-RGB image 투영
- [ ] (Optional) YOLO 경량화
