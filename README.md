# trademark-phonetic-similarity(상표 칭호 유사 판단)

## 문제 정의 및 목표
출원상표가 선출원상표와 동일 또는 유사하고 지정 상품이 동일 또는 유사한 경우 해당 출원상표는 특허청 심사관에 의하여 거절된다. 
따라서 출원시점에 출원상표가 타인의 선출원상표와 유사하다는 판단을 할 수 있다면 시간, 금액적인 측면에서 많은 비용을 줄일 수 있다. 
이 프로젝트는 특히 두 상표가 칭호가 유사할 경우로 제한하여 연구를 진행한다. 

특허청 데이터 중 칭호가 유사하여 거절된 데이터 1.2만쌍(한글, 영문)과 머신러닝 기술을 활용하여 두 상표의 유사, 비유사를 판단한다.

[특허청 키프리스 바로가기](http://plus.kipris.or.kr/)

### 데이터
sample_trademark_data.csv 파일은 실행을 위한 샘플 데이터입니다.
(label) 0 : 유사, 1: 비유사

실제 데이터의 구성은 다음과 같습니다.

유사데이터 : 12,302쌍, 비유사데이터 : 15,905쌍

## 제약사항
본 연구에선 다음과 같은 제약사항을 두어 상표쌍을 비교하였다.
1. 숫자를 포함한 상표 제외 
2. 영문기준 20글자 이상 상표 제외 (한글의 경우 약 7-8글자가 최대)
3. 한글, 영어 이외의 문자 제외 (한자, 일본어 등) 
4. 상표의 ‘&’는 ‘and’로 치환 
5. 기타 기호들은 전처리 과정에서 삭제

## 기본 아이디어
해당 아이디어는 특허 출원번호(제10-2017-0152299호)에 의하여 보호됩니다.

1. 단어의 칭호적인 특징을 추출하여 벡터화를 통해 이미지로 만듦
2. 벡터화된 값을 input으로 하여 Convolution NN을 실행한다.
3. 두 단어쌍의 결과값을 심사관의 판단에 기초하여 지도학습을 수행한다.

- 예시

![hana VIP vs hana golf](https://github.com/pyobro/airi400-trademarks-phonetic-classification/blob/master/data/image_merge/HANA%20VIP.Hanagolf.0.png)

위의 예시는 hana vip 와 hana golf의 칭호적인 특징을 이용하여 hana vip는 RGB채널의 R채널, hana golf는 B채널에 배치하여 만든 이미지이다. 

## 학습 결과

![tensorboard](https://github.com/pyobro/airi400-trademarks-phonetic-classification/blob/master/epoch20-LR0.001.png)
validation accuracy 기준으로 약 90% 정확도를 달성하였다. 

![random test](https://github.com/pyobro/airi400-trademarks-phonetic-classification/blob/master/result.png)
5번째 상표 결과를 제외하고 모두 정답을 예측하였다. 

| Adam | epoch: 001 | loss: 0.29621 - acc: 0.8691 | val_loss: 0.32331 - val_acc: 0.8613 -- iter: 22560/22560
| Adam | epoch: 002 | loss: 0.26400 - acc: 0.8919 | val_loss: 0.66627 - val_acc: 0.7628 -- iter: 22560/22560
| Adam | epoch: 003 | loss: 0.21131 - acc: 0.9152 | val_loss: 0.23522 - val_acc: 0.9043 -- iter: 22560/22560
| Adam | epoch: 004 | loss: 0.17665 - acc: 0.9300 | val_loss: 0.24968 - val_acc: 0.9043 -- iter: 22560/22560
| Adam | epoch: 005 | loss: 0.13552 - acc: 0.9459 | val_loss: 0.37089 - val_acc: 0.8479 -- iter: 22560/22560
| Adam | epoch: 006 | loss: 0.13026 - acc: 0.9486 | val_loss: 0.34793 - val_acc: 0.8830 -- iter: 22560/22560
| Adam | epoch: 007 | loss: 0.11382 - acc: 0.9679 | val_loss: 0.24277 - val_acc: 0.9092 -- iter: 22560/22560
| Adam | epoch: 008 | loss: 0.08500 - acc: 0.9735 | val_loss: 0.30742 - val_acc: 0.8936 -- iter: 22560/22560
| Adam | epoch: 009 | loss: 0.08363 - acc: 0.9760 | val_loss: 0.27712 - val_acc: 0.9117 -- iter: 22560/22560
| Adam | epoch: 010 | loss: 0.05866 - acc: 0.9860 | val_loss: 0.31002 - val_acc: 0.9096 -- iter: 22560/22560

## 한계와 개선점
본 연구에서 비유사 데이터 쌍은 랜덤으로 상표를 매칭하여 제작하였다. 하지만 이러한 방법으로는 실제 어느정도 유사하지만 심사관에 의해 비유사로 
구분된 데이터 쌍을 대체할 수 없다. 어느 정도 유사하지만 심사관이 비유사하다고 판단 내린 데이터쌍을 확보하여 성능을 개선할 필요가 있다. 

위 연구는 지능정보기술연구원(AIRI)의 AIRI400 프로젝트 1기에서 진행하였습니다.(프로젝트 종료 2017.11.17)

연구 참여자 : 고경표, 이재오 교육생

연구 멘토 : 이상훈, 이광희 연구원

[지능정보기술연구원 바로가기](http://airi.kr/research-division/notice/?mod=document&uid=28)
