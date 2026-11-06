# conference-schedule

PACL 노션 홈에 임베드하는 학회 마감 위젯입니다.

- 일정은 [ccfddl](https://github.com/ccfddl/ccf-deadlines)에서 접속할 때마다 받아옵니다. 받아오지 못하면 `snapshot/`의 사본을 씁니다.
- 마감 시각은 모두 한국시간(KST)으로 바꿔서 보여줍니다. Rebuttal·Notification은 원래 날짜 그대로입니다.
- 보기는 **한 줄 / 학회별 / 목록** 세 가지이고, 고른 보기와 기간은 브라우저에 기억됩니다.

## 고치는 곳

| 하고 싶은 것 | 파일 |
| --- | --- |
| 학회 추가·삭제 | `conferences.json` — ccfddl의 `conference/<분류>/<이름>.yml` 경로를 적습니다 |
| ccfddl에 없는 일정 (삼성휴먼테크, Supplementary 등) | `extras.json` |
| 사본 갱신 | ccfddl 저장소의 yml을 `snapshot/`에 덮어쓰기 |

## 노션에 넣기

노션에서 `/embed` → `https://reo91004.github.io/conference-schedule/` 를 붙여 넣습니다.
