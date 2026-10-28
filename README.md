# Dropseal 사이트

Dropseal 앱의 소개, 개인정보 처리방침, 지원 페이지. `docs/` 폴더를 깃허브 페이지로 게시한다.

- 언어: 영어(사이트 첫 화면), 한국어 `ko/`, 일본어 `ja/`, 중국어 간체 `zh-Hans/`, 번체 `zh-Hant/`
- 문구는 `src/content.py`에서 고치고 `python3 src/build.py`로 `docs/`의 페이지 15개를 다시 만든다. `docs/*.html`을 직접 고치지 않는다.
- 첫 화면: 스크롤하면 씰이 녹고(앱과 같은 도형 계산, `docs/site.js`) 끝에서 갈라지며 편지 한 줄이 나타난다. '이렇게 써요'는 휴대폰 화면이 단계를 따라 바뀌고 봉인·해제 장면은 효과음이 들어간 영상(`docs/media/<언어>/`)이다. 움직임 줄이기 설정을 켜면 정지 화면으로 보인다.
- 색: Radix Colors `sand`·`ruby` (MIT), 아이콘: Phosphor Icons (MIT, `src/icons/`)
- 글꼴: Pretendard, Instrument Serif (SIL OFL 1.1) — `docs/fonts/`에 직접 포함해 외부 요청 없음. 일본어·중국어는 각 언어의 시스템 글꼴을 쓴다.
