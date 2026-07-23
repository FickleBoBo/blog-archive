---
name: tag-taxonomy
description: 태그 판정은 tools/tags.md가 단일 소스지만 note가 실무와 어긋날 수 있음 — 심판은 발행본 grep. /review 스킬 Phase 3·4에 낡은 전제 있음
metadata: 
  node_type: memory
  type: project
  originSessionId: be48e301-ac00-47ab-95c0-a4f7234a365b
---

태그 어휘·부착 기준의 단일 소스는 **`tools/tags.md`** (135 vocab, 15 카테고리, closed vocabulary). 판정 기준은 전부 거기 note로 기록해 뒀으니 **여기 중복하지 말고 tags.md를 읽을 것.** 이 메모리는 *도구가 기록 못 하는 것*만 남긴다.

## ★ tags.md의 note가 틀릴 수 있다 — 심판은 발행본 grep

`[bfs]` note가 "unweighted shortest path는 명시적으로 shortest path 추가"라고 **지시했는데 발행본 22/22가 안 따랐다.** 2178 미로 탐색·14940 쉬운 최단거리·1697 숨바꼭질·7576 토마토 전부 `[graph, bfs]`. note는 어휘 파일 작성일(2026-04-09) 것이고 부착은 그 **다음 날** 일어났으니 순서 문제도 아니었음.

→ 2026-07-17에 **실무 쪽으로 note를 정정**(`shortest path`는 가중치 최단경로 전용). 근거: 붙이면 `shortest path` 검색 결과가 `bfs`와 거의 겹쳐 구분값이 사라짐.

**교훈: 태그 판정 전 `grep -rh "^tags:" _posts`로 실제 용례를 세라.** note만 믿지 말 것. 서브에이전트 추천도 그대로 받지 말 것 — 이번에 청크 3이 2206에 `shortest path`를 추천했고 note상으론 맞았지만 실무와 어긋났음.

## ★ 코퍼스 선례가 없으면 solved.ac API를 직접 조회 (추측 금지) — 2026-07-18

grep으로 발행본 용례가 안 나오는(선례 0) 태그는 **추측하지 말고 solved.ac 실제 태그를 조회**할 것. 방법은 [[boj-shutdown-status]]: `curl`/`WebFetch`는 403이지만 **puppeteer에 시스템 Chrome `executablePath` 넘기면** solved.ac API(`/api/v3/problem/show?problemId=`) 뚫림. **iCloud 미러의 `labels` 필드는 solved.ac 알고리즘 태그가 아니다**(백준 자체 메타 — 스페셜저지/다국어). 비어 있어도(`[]`) solved.ac API엔 태그가 있음.

실측 실패 사례: 17128을 코퍼스 대조도 solved.ac 조회도 없이 "구조가 비슷하다"며 `sliding window`로 달았다가, solved.ac 조회(수학/구현/누적 합, sliding window 없음)로 `[implementation, prefix sum]` 정정. 미러 labels가 `[]`라 넘어갔던 게 원인. **미러 labels 비었다고 solved.ac를 건너뛰지 말 것.**

## ⚠️ `/review` 스킬의 낡은 전제 (미수정 — 고쳐야 함)

Phase 4에 이렇게 적혀 있는데 **거짓이다**:
> 현재는 모든 글이 `[Unlinked]` 상태라 batch 내 harmonize만 가능 / 태그 부착된 글이 쌓이면 … (별도 리팩토링 시점에 도입)

**발행본 534개는 전부 태그가 붙어 있다(`unlinked: 0`).** 스킬이 말한 "쌓이면 도입" 시점이 이미 왔는데 스킬은 옛 전제로 돈다. Phase 3의 강제 4단계 (d)도 "tags.md 정의 읽기 + solved.ac 직접 확인"만 시키고 **발행본 대조를 안 시킨다.** → (d)에 "발행본에서 같은 태그 용례를 grep으로 대조"를 넣고 Phase 4 문단을 정정할 것.

## 코퍼스 최초 태그 (선례 0 — 여기서 정한 게 곧 선례)

2차 배치 32개에서 처음 등장: `knapsack`, `monotonic queue`, `union find`(4개), `modular inverse`, `fermat's little theorem`, `lucas' theorem`. 실무와 대조할 방법이 없어 `attach_when` 정의만으로 판단함. 나중에 흔들리면 이 글들이 기준점.

## 도구 사용법 (실측)

- **프론트매터는 flat full ancestry** — `[math, number theory, sieve of eratosthenes]` 식으로 부모까지 다 들어감. 하지만 **추천/부착은 specific만** 하면 auto-companion이 부모를 채운다. `[union find, graph]`처럼 부모를 같이 넣지 말 것.
- **`technique` 산하는 부모가 안 붙는다** (`auto_companion: false`). `monotonic queue`·`sliding window`·`backtracking`·`parametric search` 부착해도 `technique`은 미부착 — 정상.
- **`rename`은 포스트만 고친다.** `tags.md` 헤더를 **먼저** 수정해야 함(안 하면 `target tag not in vocabulary`로 die). changelog는 `log_change`가 자동 append.
- **`attach`/`detach`는 `--post NUM --tag TAG` 단건.** `--apply` 없으면 드라이런. 51회 돌리면 CLI로는 느리니(각각 534개 스캔) 인프로세스로:
  ```python
  import sys; sys.path.insert(0,'tools')
  import tag_migrate; from tag_utils import parse_tags_md
  tags_dict = parse_tags_md()            # ← load_tags 아님. 이름 주의
  tag_migrate.cmd_attach(['--post','1717','--tag','union find','--apply'], tags_dict)
  ```
- **번호 충돌 사전 확인**: `from tag_migrate import collect_target_posts` → 각 번호가 1건 매칭인지. `find_posts`가 PS_DIRS 게이트를 타서 legacy·tmp·루트는 안 보임(= `commit.py`와 달리 안전).

## 잡다한 실측

- `xargs`는 한글 파일명 공백에서 깨진다 → `-Z`/`-0` 쓰거나 python으로.
- `grep -rl ... | xargs grep -l`로 태그 조합을 세다가 **0건으로 오측**한 적 있음. 실제론 1건이었음.
- 태그 통계는 python `rglob` + 정규식이 안전.

관련: [[blog-soft-reboot]] [[code-conventions]]
