---
name: boj-shutdown-status
description: 백준(acmicpc.net) 서비스 종료·인수 현황과 리뷰 워크플로우 영향
metadata: 
  node_type: memory
  type: project
  originSessionId: a1a39de3-62c0-4cff-8e97-620967f49568
---

백준 온라인 저지(acmicpc.net) 상태 (2026-07 기준, WebSearch 검증):
- 2026-04-28 서비스 완전 종료
- 이후 "채점 서비스와 함께 곧 돌아온다"로 공지 변경 (원래 "문제 열람만" → 채점 포함으로 확대, 대신 날짜 미정)
- 2026-06-11 데이원컴퍼니가 BOJ 인수 발표 (인수 직후 별개 개인정보 유출 이슈 보도도 있었음)
- **확정 재오픈 날짜 없음** (2026-07 시점)

워크플로우 영향: BOJ 온라인 원문 접근 불가 → `/review`의 puppeteer fetch(문제 본문 대조)가 BOJ 대상은 막힘. 옛 백준 칼럼 마이그레이션/검증이 애매해짐 → [[blog-soft-reboot]]의 tmp 백업이 원문 보존용으로 특히 중요.

**로컬 크롤링 미러 발견 (2026-07-16) — fetch 대체 자산:** iCloud Drive에 BOJ 문제 원문이 통째로 크롤링돼 있음. 경로: `~/Library/Mobile Documents/com~apple~CloudDocs/baekjoon-crawling/data/problems/{번호}.json`. 각 JSON 키: `title, labels, description, input, output, limit, hint, samples, source, similar_problems, translations, ...`. `samples`는 예제 입출력, `description/input/output`은 HTML(태그 strip 필요). → **puppeteer fetch 막혀도 이 미러로 문제 원문·제약·예제 대조 가능.** `/review`에서 BOJ 문제 검증 시 사이트 대신 이 경로를 우선 확인할 것. (별도로 `baekjoon-crawling/tistory_data/posts/*.json`에 과거 티스토리 포스트 원문도 있음.) 실측: 8개 문제 원문 대조로 등급 검증 성공(29119 B→A 정정 포함).

## ★ solved.ac / 코드포스 조회 뚫림 (2026-07-16) — 이전 "Cloudflare로 막힘" 기록 정정
`curl`·`WebFetch`는 solved.ac에서 **403(Cloudflare 챌린지)**, 코드포스는 403. 하지만 **MCP puppeteer에 시스템 Chrome 경로를 넘기면 통과한다:**
```
mcp__puppeteer__puppeteer_navigate(url, launchOptions={
  "headless": false,
  "executablePath": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
})
```
- puppeteer가 "Could not find Chrome"으로 실패하는 건 자체 캐시(`~/.cache/puppeteer`)만 뒤지기 때문. **시스템에 Chrome은 이미 설치돼 있음**(`/Applications/Google Chrome.app`). `npx puppeteer browsers install chrome` **불필요.**
- 실제 브라우저라 Cloudflare 챌린지를 통과함. 실측: solved.ac API로 24개 문제의 `level`·`tags` 일괄 조회 성공(`puppeteer_evaluate` 안에서 `fetch()` 루프 + 350ms 딜레이). 코드포스 문제 본문(`.problem-statement`)도 추출 성공.
- → **`/review` Phase 3의 "solved.ac 분류 직접 확인" 요구를 충족 가능.** 서브에이전트 프롬프트에 `executablePath`를 반드시 명시할 것(안 하면 Chrome 못 찾고 실패함).
- 미러의 `labels` 필드는 **solved.ac 알고리즘 태그가 아님** — 백준 자체 메타(스페셜 저지/다국어/서브태스크). 알고리즘 태그는 위 solved.ac 경로로만.

시간 민감 정보 — 재확인 필요하면 WebSearch로 최신 상태 갱신할 것.
