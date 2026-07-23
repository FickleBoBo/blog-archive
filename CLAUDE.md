# PS 블로그 자동화

## 사용자

- PS(Problem Solving) 블로그를 운영하며 독자들이 찾아오는 양질의 블로그를 목표로 함
- 포스트 품질 기준: 아이디어는 문제의 핵심을 짚어 잘 이해되게, 코드는 깔끔하고 완벽하며 일관되게
- 주 언어: Java, C++ (향후 Python 추가 가능)
- 풀이 플랫폼: 백준, 프로그래머스, 리트코드, 코드포스, SWEA
- 반복 작업 자동화를 강하게 선호
- 토큰 효율성을 중시 — API로 가능한 건 API, MCP는 최소한으로
- 간결한 명령어로 일관된 결과를 원함
- 잘못된 코드가 관례에 반영되는 것을 방지하기 위해 리뷰와 관례 갱신을 분리
- 풀이 포스트(`_drafts/`, `_posts/`)는 사용자 허락 없이 직접 수정하지 않는다
- `/commit`은 사용자가 스킬로 직접 호출할 때만 실행한다 (수정 보고 ≠ 커밋 요청)
- 커밋은 반드시 사용자의 명시적 허락을 받은 후에만 실행한다 — 리뷰 통과 후에도 자동 커밋 금지

## 프로젝트 구조

- **블로그**: `~/Desktop/GITHUB/FickleBoBo.github.io` (Jekyll, chirpy 테마)
- **풀이 코드**: `~/Desktop/GITHUB/Algorithm/{YYYY-MM}/src/day_{DD}/{platform}_{number}/Main.java|cpp`
- 플랫폼 접두사: `boj_`, `prms_`, `cofo_`, `leet_`, `swea_`

## 워크플로우

```
/ps {YYYY-MM-DD|YYYY-MM} [번호...]  → _drafts/에 포스트 생성 (번호 생략 시 해당 날짜/월 전체)
/review [번호]        → 검수 (인자 없으면 _drafts/ 전체)
/sync [번호]          → 코드 블록 최신화 (인자 없으면 _drafts/ 전체)
/commit [번호...]     → _drafts/ → _posts/ 이동 + 체크리스트 갱신 + 양쪽 레포 커밋
```

## 스킬

| 명령어                  | 유형     | 설명                                                       |
| ----------------------- | -------- | ---------------------------------------------------------- |
| `/ps {YYYY-MM-DD|YYYY-MM} [번호...]`  | 스크립트 | 포스트 자동 생성 (SWEA TODO만 MCP 필요)                    |
| `/review [번호]`        | Claude   | 포스트 검수 (Phase 1: 스크립트, Phase 2: Sonnet 분석, Phase 3: Opus 등급 판정) |
| `/sync [번호]`          | 스크립트 | 코드 블록을 Algorithm 디렉토리와 동기화                    |
| `/commit [번호...]`     | 스크립트 | 드래프트 이동 + 체크리스트 갱신 + 양쪽 레포 커밋           |
| `/checklist-update`     | 스크립트 | 체크리스트 자동 체크 (백준 전용)                            |
| `/conventions`          | 스크립트 | 기존 포스트 스캔 → 코드 관례(`tools/conventions.md`) 갱신  |

## 도구

### 공통 모듈

| 파일                | 설명                                                                    |
| ------------------- | ----------------------------------------------------------------------- |
| `tools/config.py`   | 공통 설정 (경로, 플랫폼 매핑, 언어 설정, 파일명 치환 등)               |
| `tools/code_utils.py` | 공통 유틸 (파일명 파싱, 포스트 검색, Java 전처리, 코드 읽기)          |

### 스킬별 스크립트

| 파일                          | 대응 스킬             | 설명                                         |
| ----------------------------- | --------------------- | -------------------------------------------- |
| `tools/generate_posts.py`     | `/ps`                 | 포스트 템플릿 생성 (API로 제목/링크 fetch)   |
| `tools/review_check.py`       | `/review` Phase 1     | 기계적 검수 (구조, 수식 공백, 복잡도 표기 등) |
| `tools/sync.py`               | `/sync`               | 코드 블록 diff 확인 + 적용                   |
| `tools/commit.py`             | `/commit`             | 드래프트 이동 + algo/blog 양쪽 커밋          |
| `tools/checklist_update.py`   | `/checklist-update`   | _posts/ 스캔 → 체크리스트 자동 체크          |
| `tools/conventions_scan.py`   | `/conventions`        | 포스트 스캔 → 코드 관례 추출                 |

### 기타

| 파일                          | 설명                                                     |
| ----------------------------- | -------------------------------------------------------- |
| `tools/checklist_progress.py` | 체크리스트 진행률 표시                                   |
| `tools/conventions.md`        | 코드 관례 레퍼런스 (`/conventions`로 갱신)               |
| `tools/run.sh`                | Jekyll 로컬 서버 (livereload + incremental + drafts)     |
| `_layouts/drafts.html`        | 드래프트 전용 페이지 레이아웃                            |
| `_tabs/drafts.md`             | 사이드바 Drafts 탭 (로컬에서 드래프트만 모아보기)        |

## 체크리스트

`checklists/` 디렉토리에 4개 체크리스트 (2026-03-25 생성, 교차검증 완료):

| 파일          | 소스                        | 섹션 | 문제 수 |
| ------------- | --------------------------- | ---- | ------- |
| step.md       | 단계별로 풀어보기           | 68   | 531     |
| barkingdog.md | 바킹독 문제집 (구버전 제외) | 33   | 484     |
| series.md     | 시리즈 문제집               | 90   | 513     |
| codeplus.md   | 코드플러스 문제집           | 110  | 882     |
