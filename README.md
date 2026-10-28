# Dropseal 사이트

Dropseal 앱의 소개, 개인정보 처리방침, 지원 페이지. `docs/` 폴더를 깃허브 페이지로 게시한다.

- 언어: 영어(사이트 첫 화면), 한국어 `ko/`, 일본어 `ja/`, 중국어 간체 `zh-Hans/`, 번체 `zh-Hant/`
- 문구는 `src/content.py`에서 고치고 `python3 src/build.py`로 `docs/`의 페이지 15개를 다시 만든다. `docs/*.html`을 직접 고치지 않는다.
- 색: Radix Colors `sand`·`ruby` (MIT), 아이콘: Phosphor Icons (MIT, `src/icons/`)
- 글꼴: Pretendard, Instrument Serif (SIL OFL 1.1) — `docs/fonts/`에 직접 포함해 외부 요청 없음. 일본어·중국어는 각 언어의 시스템 글꼴을 쓴다.
