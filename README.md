# trademark-phonetic-similarity(상표 칭호 유사도 계산)

## 문제 정의 및 목표
출원상표가 선출원상표와 동일 또는 유사하고 지정 상품이 동일 또는 유사한 경우 해당 출원상표는 특허청 심사관에 의하여 거절된다. 
따라서 출원시점에 출원상표가 타인의 선출원상표와 유사하다는 판단을 할 수 있다면 시간, 금액적인 측면에서 많은 비용을 줄일 수 있다. 
이 프로젝트는 특히 두 상표가 칭호가 유사할 경우로 제한하여 연구를 진행한다. 

특허청 데이터 중 칭호가 유사하여 거절된 데이터 10만쌍(한글, 영문)과 머신러닝 기술을 활용하여 두 상표의 유사, 비유사를 판단한다.

[특허청 키프리스 바로가기](http://plus.kipris.or.kr/)

## 기본 아이디어

1. 단어쌍를 발음에 기초하여 벡터화한다.
2. 벡터화된 값을 input으로 하여 Convolution NN을 실행한다.
3. 두 단어쌍의 결과값을 심사관의 판단에 기초하여 지도학습을 수행한다.

위 연구는 지능정보기술연구원의 AIRI400 프로젝트에서 진행하고 있습니다.

연구 참여자 : 고경표, 이재오 교육생

연구 멘토 : 이상훈, 이광희 연구원

[지능정보기술연구원 바로가기](http://airi.kr/research-division/notice/?mod=document&uid=28)
