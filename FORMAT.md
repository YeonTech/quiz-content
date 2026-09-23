# 문제 양식 (quiz-content)

앱은 `index.json`(매니페스트)을 읽고 → 거기 나열된 세트 파일들을 받아 문제를 합친다.

## 파일 구조
```
index.json            # 매니페스트: version + 세트 목록
sets/minsang-01.json  # 문제 세트 (여러 개 가능)
sets/minsang-02.json
...
```

## index.json
```json
{
  "version": "2026-09-23T03:23:11Z",   // 갱신할 때마다 바꾼다(앱이 변경 감지)
  "sets": [
    { "id": "minsang-01", "file": "sets/minsang-01.json", "title": "민상법 기초 1" },
    { "id": "minsang-02", "file": "sets/minsang-02.json", "title": "민상법 기초 2" }
  ]
}
```
- **새 세트를 추가하면 여기 `sets`에 한 줄 추가 + `version`을 새 시각으로 바꾼다.**

## 세트 파일 (sets/*.json)
```json
{
  "id": "minsang-02",
  "title": "민상법 기초 2",
  "questions": [
    {
      "id": "ms-0031",                    // 세트/전체에서 유일한 id
      "topic": "채권법",                   // 아래 5개 중 하나만
      "tags": ["임대차", "보증금"],         // 세부 유형(비슷한 유형 묶기용, 0개 이상)
      "difficulty": 2,                     // 1(쉬움)~3(어려움)
      "prompt": "문제 지문",
      "choices": ["보기1", "보기2", "보기3", "보기4"],   // 정확히 4개
      "answer": 1,                         // 정답 인덱스, 0부터 시작(0~3)
      "explanation": "정답 근거(조문/법리) 서술",
      "choiceExplanations": [              // 정확히 4개, 각 보기별 맞음/틀림 이유
        "보기1이 틀린 이유",
        "보기2가 정답인 이유",
        "보기3이 틀린 이유",
        "보기4가 틀린 이유"
      ]
    }
  ]
}
```

## 규칙 (꼭 지킬 것)
- `answer`는 **0부터 시작**하는 인덱스(첫 보기=0). 흔한 실수 주의.
- `choices` **4개**, `choiceExplanations` **4개**(choices와 순서 대응).
- `id`는 **전체에서 유일**(중복 금지). 새 문제는 이어서 `ms-0031`, `ms-0032`...
- `topic`은 다음 5개 중 하나만: **`민법총칙` `물권법` `채권법` `상법총칙` `회사법`**
  (예상 점수·약점 분석이 이 topic 기준으로 계산됨)
- JSON 문법(따옴표·쉼표) 정확히. 큰따옴표 안에 큰따옴표 쓰면 `\"`로 이스케이프.

## 추가 절차
1. `sets/`에 새 파일 추가(또는 기존 파일 `questions`에 이어붙이기).
2. `index.json`의 `version`을 현재 시각으로 갱신(+새 파일이면 `sets`에 등록).
3. `python3 validate.py` 로 검증.
4. `git add -A && git commit -m "..." && git push`.
5. 앱은 **다음 실행 때 자동으로 새 문제를 받아옴**(재배포 불필요).
