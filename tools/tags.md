# PS Blog Tag Vocabulary — Single Source of Truth

이 파일은 PS 블로그(`FickleBoBo.github.io`) 태그 시스템의 단일 진실 소스다.
15 카테고리 + 134 태그의 closed vocabulary를 정의한다.

## 운영 원칙

- **Frontmatter 형식**: 옵션 A (flat full ancestry). 글의 `tags` 필드에 ancestry 전체가 명시적으로 들어감
- **Auto-companion**: 자식 태그를 달면 부모 chain 전체가 자동 부착됨 (예: `dijkstra` → `shortest path` + `graph`)
- **부착 기준 (Future-you 검색 가치 테스트)**: "X로 검색한 미래의 자신이 이 글을 *유용한 결과*로 받아들일 것이다" 일 때만 부착
- **Strict 정책**: `attach_policy: strict` 표시된 태그는 *문제 해결의 핵심이 해당 자료구조/기법일 때만* 부착. 단순 보조/라이브러리 사용은 노이즈이므로 부착 금지
- **Closed vocabulary**: 이 파일에 정의되지 않은 태그는 사용 금지. `tag_audit.py`에서 검출
- **`technique` 카테고리는 auto-companion 예외**: 자식 부착해도 `technique` 태그 자체는 부착 안 함
- **Umbrella 단독 부착 허용**: 모든 umbrella 카테고리(data structure, graph, dp, string, math, geometry, game theory + 하위 umbrella)는 자식이 적합하지 않으나 분류 자체가 명확한 경우 단독 부착 가능. 단, specific 자식이 있으면 그것을 우선 (umbrella 단독은 last resort)

## Schema

각 태그는 다음 필드를 가짐:

```
[tag-name]                  태그 헤더 (대괄호로 감쌈)
parent: ...                 부모 태그 (root 카테고리는 생략)
attach_when: ...            부착 기준 (한 줄, 필수)
attach_policy: strict       (선택) 강화 부착 정책
solved_ac: ...              (선택) solved.ac 한국어 태그 매핑 (다중은 쉼표 구분)
auto_companion: false       (선택) auto-companion 예외 (technique만)
note: ...                   (선택) 추가 노트 (cross-reference, disambiguation 등)
```

빈 줄이 태그 정의의 종료를 의미한다.

---

# Tag Definitions

## 1. data structure (16)

[data structure]
attach_when: 자식 자료구조 태그 부착 시 auto-companion. 또는 자식이 적합하지 않으나 자료구조 분류가 풀이의 핵심인 경우 단독 부착 가능.

[stack]
parent: data structure
attach_when: 스택 자료구조 활용이 풀이의 핵심
attach_policy: strict
solved_ac: 스택

[queue]
parent: data structure
attach_when: 큐 자료구조 활용이 풀이의 핵심 (단순 BFS 보조 X)
attach_policy: strict
solved_ac: 큐

[deque]
parent: data structure
attach_when: 덱 자료구조 활용이 풀이의 핵심 (단순 슬라이딩 윈도우 보조 X)
attach_policy: strict
solved_ac: 덱

[priority queue]
parent: data structure
attach_when: 우선순위 큐 사용이 풀이의 핵심
solved_ac: 우선순위 큐

[segment tree]
parent: data structure
attach_when: 세그먼트 트리 자체 또는 변형 사용
solved_ac: 세그먼트 트리

[lazy propagation]
parent: segment tree
attach_when: 구간 업데이트 + lazy 전파 사용
solved_ac: 느리게 갱신되는 세그먼트 트리

[merge sort tree]
parent: segment tree
attach_when: 머지 소트 트리 사용
solved_ac: 머지 소트 트리

[2d segment tree]
parent: segment tree
attach_when: 2차원 세그먼트 트리 사용
solved_ac: 2차원 세그먼트 트리

[persistent segment tree]
parent: segment tree
attach_when: 퍼시스턴트 세그먼트 트리 사용
solved_ac: 퍼시스턴트 세그먼트 트리

[fenwick tree]
parent: data structure
attach_when: 펜윅 트리(BIT) 사용
solved_ac: 펜윅 트리

[2d fenwick tree]
parent: fenwick tree
attach_when: 2차원 펜윅 트리 사용
solved_ac: 2차원 인덱스 트리

[sparse table]
parent: data structure
attach_when: 희소 테이블 사용 (RMQ, LCA 보조 등)
solved_ac: 희소 배열

[hash set／hash map]
parent: data structure
attach_when: 해시 자료구조 선택이 문제 해결의 핵심 (단순 카운팅/룩업 보조 X)
attach_policy: strict
solved_ac: 해시를 사용한 집합과 맵

[tree set／tree map]
parent: data structure
attach_when: 정렬된 set/map 자료구조 선택이 문제 해결의 핵심
attach_policy: strict
solved_ac: 트리를 사용한 집합과 맵

[trie]
parent: data structure
attach_when: 트라이 사용 (string 또는 XOR trie 등)
solved_ac: 트라이
note: string에 한정되지 않는 광범위 자료구조라 data structure에 분류

## 2. graph (31)

[graph]
attach_when: 자식 그래프 태그 부착 시 auto-companion. 또는 자식이 적합하지 않으나 그래프 분류가 풀이의 핵심인 경우 단독 부착 가능.

[bfs]
parent: graph
attach_when: BFS 탐색이 풀이의 핵심
solved_ac: 너비 우선 탐색
note: 무가중치 그래프에서 BFS로 최소 이동 횟수를 구하는 것은 `shortest path`로 치지 않는다. `bfs` 단독으로 둘 것 (2026-07-17 확정)

[dfs]
parent: graph
attach_when: DFS 탐색이 풀이의 핵심
solved_ac: 깊이 우선 탐색

[flood fill]
parent: graph
attach_when: 플러드 필 패턴 (그리드 영역 채우기/세기)
solved_ac: 플러드 필

[topological sort]
parent: graph
attach_when: 위상 정렬 사용
solved_ac: 위상 정렬

[union find]
parent: graph
attach_when: 유니온 파인드(DSU) 사용
solved_ac: 분리 집합
note: 사용처 거의 graph 전용 (kruskal MST, connectivity 등)

[2-sat]
parent: graph
attach_when: 2-SAT 환원/풀이
solved_ac: 2-sat

[articulation]
parent: graph
attach_when: 단절점 또는 단절선 검출
solved_ac: 단절점과 단절선

[bipartite matching]
parent: graph
attach_when: 이분 매칭 (DFS 기반 augmenting path)
solved_ac: 이분 매칭

[hopcroft karp]
parent: bipartite matching
attach_when: 호프크로프트–카프 알고리즘 (BFS+DFS 매칭)
solved_ac: 호프크로프트-카프

[eulerian path]
parent: graph
attach_when: 오일러 경로/회로 (모든 간선 1회 방문)
solved_ac: 오일러 경로
note: tree의 euler tour와는 완전히 다른 개념

[tree]
parent: graph
attach_when: 자식 트리 알고리즘 부착 시 auto-companion. 또는 자식이 적합하지 않으나 트리 분류가 풀이의 핵심인 경우 단독 부착 가능.

[lca]
parent: tree
attach_when: 최소 공통 조상 (sparse table/euler tour 등)
solved_ac: 최소 공통 조상

[euler tour]
parent: tree
attach_when: 트리 DFS 진입/탈출 시퀀스 (subtree → range)
solved_ac: 오일러 경로
note: graph의 eulerian path와는 완전히 다른 개념. 트리 특화 기법

[hld]
parent: tree
attach_when: heavy-light decomposition (트리 경로 쿼리)
solved_ac: 트리의 경로 쿼리

[centroid decomposition]
parent: tree
attach_when: 센트로이드 분할 (트리 분할정복)
solved_ac: 센트로이드 분할

[shortest path]
parent: graph
attach_when: 가중치 그래프의 최단경로. 자식 알고리즘(dijkstra/bellman ford/floyd warshall/0-1 bfs) 부착 시 auto-companion. 또는 자식이 적합하지 않으나 최단경로 분류가 풀이의 핵심인 경우 단독 부착 가능.
note: 무가중치 BFS 거리는 제외 — `bfs` 단독으로 둔다. 붙이면 `bfs`와 검색 결과가 거의 겹쳐 구분값이 사라짐 (2026-07-17 확정)

[dijkstra]
parent: shortest path
attach_when: 다익스트라 알고리즘 (양수 가중치 단일 시작점)
solved_ac: 다익스트라

[bellman ford]
parent: shortest path
attach_when: 벨만-포드 (음수 가중치 또는 음수 사이클 검출)
solved_ac: 벨만–포드

[floyd warshall]
parent: shortest path
attach_when: 플로이드-워셜 (모든 쌍 최단경로)
solved_ac: 플로이드–워셜

[0-1 bfs]
parent: shortest path
attach_when: 0-1 가중치 BFS (deque 활용)
solved_ac: 0-1 너비 우선 탐색

[mst]
parent: graph
attach_when: 자식 MST 알고리즘 부착 시 auto-companion. 또는 자식이 적합하지 않으나 MST 분류가 풀이의 핵심인 경우 단독 부착 가능.

[kruskal]
parent: mst
attach_when: 크루스칼 알고리즘 (간선 정렬 + union find)
solved_ac: 최소 스패닝 트리

[prim]
parent: mst
attach_when: 프림 알고리즘 (정점 기반 priority queue)
solved_ac: 최소 스패닝 트리

[scc]
parent: graph
attach_when: 자식 SCC 알고리즘 부착 시 auto-companion. 또는 자식이 적합하지 않으나 SCC 분류가 풀이의 핵심인 경우 단독 부착 가능.

[tarjan]
parent: scc
attach_when: 타잔 SCC 알고리즘 (low-link)
solved_ac: 강한 연결 요소

[kosaraju]
parent: scc
attach_when: 코사라주 SCC 알고리즘 (두 번 DFS)
solved_ac: 강한 연결 요소

[network flow]
parent: graph
attach_when: 자식 플로우 알고리즘 부착 시 auto-companion. 또는 자식이 적합하지 않으나 네트워크 플로우 분류가 풀이의 핵심인 경우 단독 부착 가능.

[max flow]
parent: network flow
attach_when: 최대 유량 (Ford-Fulkerson 계열)
solved_ac: 최대 유량

[dinic]
parent: max flow
attach_when: 디닉 알고리즘 (level graph + blocking flow)
solved_ac: 디닉 알고리즘

[min cost max flow]
parent: network flow
attach_when: 최소 비용 최대 유량 (SSP 등)
solved_ac: 최소 비용 최대 유량

## 3. dp (14)

[dp]
attach_when: 자식 DP 태그 부착 시 auto-companion. 또는 자식이 적합하지 않으나 DP 분류가 풀이의 핵심인 경우 단독 부착 가능.

[knapsack]
parent: dp
attach_when: 배낭 문제 (0-1, unbounded, bounded 통합)
solved_ac: 배낭 문제

[lis]
parent: dp
attach_when: 가장 긴 증가하는 부분 수열 (DP 또는 이분탐색 변형)
solved_ac: 가장 긴 증가하는 부분 수열: O(n log n)

[lcs]
parent: dp
attach_when: 가장 긴 공통 부분 수열
solved_ac: 가장 긴 공통 부분 수열

[bitmask dp]
parent: dp
attach_when: 비트마스크로 상태 압축한 DP
solved_ac: 비트필드를 이용한 다이나믹 프로그래밍
note: 일반 비트 조작은 technique의 bitmask. 분리

[tree dp]
parent: dp
attach_when: 트리 위에서 DP (서브트리 합/카운트 등)
solved_ac: 트리에서의 다이나믹 프로그래밍
note: 본질이 DP라 dp 카테고리 (graph/tree umbrella가 아님). 트리 문제 검색 시 cross-reference

[digit dp]
parent: dp
attach_when: 자릿수 DP (수의 자릿수를 상태로)
solved_ac: 자릿수 다이나믹 프로그래밍

[interval dp]
parent: dp
attach_when: 구간 DP (행렬 곱셈 순서, 파일 합치기 등)
solved_ac: 다이나믹 프로그래밍

[profile dp]
parent: dp
attach_when: 프로파일 DP / broken profile DP (행 단위 비트 상태 압축)
note: bitmask dp의 변형이지만 dp 직속 flat (digit/interval dp와 같은 격)

[dp optimization]
parent: dp
attach_when: 자식 DP 최적화 기법 부착 시 auto-companion. 또는 자식이 적합하지 않으나 DP 최적화 분류가 풀이의 핵심인 경우 단독 부착 가능.

[convex hull trick]
parent: dp optimization
attach_when: CHT (선형 함수 envelope으로 DP 최적화)
solved_ac: 볼록 껍질을 이용한 최적화

[divide and conquer optimization]
parent: dp optimization
attach_when: 분할 정복 DP 최적화 (monge condition)
solved_ac: 분할 정복을 사용한 최적화

[knuth optimization]
parent: dp optimization
attach_when: 크누스 DP 최적화 (interval DP O(n^3) → O(n^2))
solved_ac: 크누스 최적화

[sos dp]
parent: dp optimization
attach_when: sum over subsets DP (부분집합 합 O(2^n * n))

## 4. string (9)

[string]
attach_when: 자식 문자열 태그 부착 시 auto-companion. 또는 자식이 적합하지 않으나 문자열의 성질·구조·조작 자체가 풀이의 핵심인 경우 단독 부착 가능.
note: dp 상태값이 문자열이면 부착(3687 성냥개비 — `String[] dp`, 전이가 문자열 연결, 비교가 길이→사전순). 숫자를 문자열로 **표현만** 하는 경우는 제외 — 11005 진법 변환 2·33964 레퓨닛의 덧셈·10872/27433 팩토리얼이 `[math]` 단독인 근거. 판별법: dp/알고리즘이 문자열 위에서 도는가, 아니면 입출력 표현일 뿐인가 (2026-07-17 확정)

[palindrome]
parent: string
attach_when: 회문 성질이 풀이의 핵심인 문제 (s == reverse(s) 비교, 양 끝 두 포인터 대칭, 회문 분할 등). manacher 같은 specific 알고리즘이 있으면 그것도 함께 부착.
note: solved.ac 매핑 없음 — 관습상 `구현`/`문자열`로 분류되나 본 시스템은 problem type 단독 태그로 추가

[manacher]
parent: palindrome
attach_when: 마나허 알고리즘 (선형 시간 팰린드롬)
solved_ac: 매내처

[anagram]
parent: string
attach_when: 애너그램 판별이 풀이의 핵심인 문제 (문자 빈도 비교, 정렬 후 비교 등)
note: solved.ac 매핑 없음 — problem type 단독 태그

[kmp]
parent: string
attach_when: KMP 패턴 매칭
solved_ac: KMP

[string hashing]
parent: string
attach_when: 문자열 해싱 (라빈-카프 등 포함)
solved_ac: 해싱

[z algorithm]
parent: string
attach_when: Z 함수 / Z 알고리즘
solved_ac: Z

[aho corasick]
parent: string
attach_when: 아호-코라식 다중 패턴 매칭
solved_ac: 아호-코라식

[suffix array]
parent: string
attach_when: 접미사 배열 (LCP 포함)
solved_ac: 접미사 배열과 LCP 배열

## 5. math (24)

[math]
attach_when: 자식 수학 태그 부착 시 auto-companion. 또는 자식이 적합하지 않으나 수학 분류가 풀이의 핵심인 경우 단독 부착 가능.

[binary exponentiation]
parent: math
attach_when: 이진 거듭제곱 (modular exp, matrix exp 등)
solved_ac: 분할 정복을 이용한 거듭제곱
note: cross-cutting 기법이라 math 직속 flat (subfield 강제 X)

[number theory]
parent: math
attach_when: 자식 정수론 태그 부착 시 auto-companion. 또는 자식이 적합하지 않으나 정수론 분류가 풀이의 핵심인 경우 단독 부착 가능.
solved_ac: 정수론

[sieve of eratosthenes]
parent: number theory
attach_when: 에라토스테네스의 체
solved_ac: 에라토스테네스의 체
note: 체 계열은 flat sibling으로 확장 (linear sieve, segmented sieve 등). `sieve` umbrella를 두지 않음

[prime factorization]
parent: number theory
attach_when: 소인수분해
solved_ac: 소인수분해

[euclidean algorithm]
parent: number theory
attach_when: 유클리드 호제법 (gcd)
solved_ac: 유클리드 호제법
note: `euclidean` 단독은 euclidean distance/geometry로 읽히므로 `algorithm`을 명시. 표준 명칭도 "Euclidean algorithm"

[extended euclidean algorithm]
parent: number theory
attach_when: 확장 유클리드 (gcd 계수)
solved_ac: 확장 유클리드 호제법

[modular inverse]
parent: number theory
attach_when: 모듈러 역원 (페르마/확장 유클리드/CRT 활용)
solved_ac: 모듈로 곱셈 역원

[fermat's little theorem]
parent: number theory
attach_when: 페르마의 소정리 활용
solved_ac: 페르마의 소정리

[crt]
parent: number theory
attach_when: 중국인의 나머지 정리
solved_ac: 중국인의 나머지 정리

[euler's totient]
parent: number theory
attach_when: 오일러 피 함수
solved_ac: 오일러 피 함수

[mobius function]
parent: number theory
attach_when: 뫼비우스 함수 / 뫼비우스 반전
solved_ac: 뫼비우스 함수

[miller rabin]
parent: number theory
attach_when: 밀러-라빈 소수 판정 (큰 수)
solved_ac: 밀러–라빈 소수 판별법

[pollard rho]
parent: number theory
attach_when: 폴라드 로 인수분해 (큰 수)
solved_ac: 폴라드 로

[combinatorics]
parent: math
attach_when: 자식 조합론 태그 부착 시 auto-companion. 또는 자식이 적합하지 않으나 조합론 분류가 풀이의 핵심인 경우 단독 부착 가능.
solved_ac: 조합론

[binomial coefficient]
parent: combinatorics
attach_when: 이항 계수 (파스칼/팩토리얼/모듈러)
solved_ac: 이항 계수

[lucas' theorem]
parent: combinatorics
attach_when: 뤼카 정리 (소수 모듈러 이항 계수)
solved_ac: 뤼카 정리

[inclusion exclusion]
parent: combinatorics
attach_when: 포함-배제 원리
solved_ac: 포함과 배제

[catalan numbers]
parent: combinatorics
attach_when: 카탈란 수 (괄호 매칭, 이진 트리 카운트 등)
solved_ac: 카탈란 수

[linear algebra]
parent: math
attach_when: 자식 선형대수 태그 부착 시 auto-companion. 또는 자식이 적합하지 않으나 선형대수 분류가 풀이의 핵심인 경우 단독 부착 가능.
solved_ac: 선형대수학

[matrix exponentiation]
parent: linear algebra
attach_when: 행렬 거듭제곱 (선형 점화식 등)
solved_ac: 분할 정복을 이용한 거듭제곱

[gauss elimination]
parent: linear algebra
attach_when: 가우스 소거법 (연립방정식, rank, determinant)
solved_ac: 가우스 소거법

[polynomial]
parent: math
attach_when: 자식 다항식 태그 부착 시 auto-companion. 또는 자식이 적합하지 않으나 다항식 분류가 풀이의 핵심인 경우 단독 부착 가능.
solved_ac: 다항식

[fft]
parent: polynomial
attach_when: 고속 푸리에 변환 (다항식/큰 수 곱셈)
solved_ac: 고속 푸리에 변환

## 6. geometry (11)

[geometry]
attach_when: 자식 기하 태그 부착 시 auto-companion. 또는 자식이 적합하지 않으나 기하 분류가 풀이의 핵심인 경우 단독 부착 가능.

[ccw]
parent: geometry
attach_when: CCW (세 점 방향성 외적)
solved_ac: CCW

[convex hull]
parent: geometry
attach_when: 볼록 껍질 (Graham/Andrew)
solved_ac: 볼록 껍질

[polygon area]
parent: geometry
attach_when: 다각형 넓이 (Shoelace formula)
solved_ac: 다각형의 넓이

[point in polygon]
parent: geometry
attach_when: 점 다각형 내부 판정 (ray casting / winding)
solved_ac: 다각형의 내부에 있는 점 판별

[segment intersection]
parent: geometry
attach_when: 두 선분 교차 판정/교차점 (CCW 4회)
solved_ac: 선분 교차 판정

[closest pair of points]
parent: geometry
attach_when: 가장 가까운 두 점 (분할정복/sweep)
solved_ac: 가장 가까운 두 점

[rotating calipers]
parent: geometry
attach_when: 회전하는 캘리퍼스 (지름/너비 등)
solved_ac: 회전하는 캘리퍼스

[pick's theorem]
parent: geometry
attach_when: 픽의 정리 (격자 다각형 넓이)
solved_ac: 픽의 정리

[pythagorean theorem]
parent: geometry
attach_when: 피타고라스 정리 활용 (직각삼각형 변 관계, 두 점 거리, 대각선 길이 등)
solved_ac: 피타고라스 정리

[polar sort]
parent: geometry
attach_when: 각도 정렬 (CCW 비교 또는 atan2)
solved_ac: 각도 정렬

## 7. greedy (1)

[greedy]
attach_when: 그리디 알고리즘이 풀이의 핵심
solved_ac: 그리디 알고리즘

## 8. technique (자식 20, technique 자체는 부착 X)

[technique]
attach_when: (카테고리 only — 태그로 부착하지 않음)
auto_companion: false
note: catch-all 카테고리. 자식 부착해도 technique 자체는 부착 안 됨

[sorting]
parent: technique
attach_when: 정렬이 문제 해결의 핵심 (greedy + 정렬, 좌표 정렬 후 sweeping 등). 단순 입력 정렬 X
attach_policy: strict
solved_ac: 정렬

[divide and conquer]
parent: technique
attach_when: 분할정복 패턴
solved_ac: 분할 정복

[two pointers]
parent: technique
attach_when: 투 포인터 기법
solved_ac: 두 포인터

[sliding window]
parent: technique
attach_when: 슬라이딩 윈도우 기법
solved_ac: 슬라이딩 윈도우

[monotonic stack]
parent: technique
attach_when: 단조 스택 활용 (next greater 등)
solved_ac: 스택의 사용

[monotonic queue]
parent: technique
attach_when: 단조 큐 활용 (sliding window max 등)
solved_ac: 덱을 이용한 구간 최댓값

[prefix sum]
parent: technique
attach_when: 누적합 활용
solved_ac: 누적 합

[2d prefix sum]
parent: technique
attach_when: 2차원 누적합 활용
solved_ac: 누적 합

[difference array]
parent: technique
attach_when: 차분 배열 (range update + point query)
solved_ac: 누적 합

[bitmask]
parent: technique
attach_when: 비트 조작 기법 (DP가 아닌 일반 비트마스크)
solved_ac: 비트마스킹
note: bitmask dp는 별도 (dp 카테고리)

[coordinate compression]
parent: technique
attach_when: 좌표 압축
solved_ac: 좌표 압축

[meet in the middle]
parent: technique
attach_when: 중간에서 만나기 (절반 분할 + 결합)
solved_ac: 중간에서 만나기

[binary search]
parent: technique
attach_when: 이분 탐색 (정렬된 배열 검색)
solved_ac: 이분 탐색

[parametric search]
parent: technique
attach_when: 매개변수 탐색 (결정 문제로 환원 후 이분탐색)
solved_ac: 매개 변수 탐색

[ternary search]
parent: technique
attach_when: 삼분 탐색 (볼록/오목 함수 최적화)
solved_ac: 삼분 탐색

[backtracking]
parent: technique
attach_when: 백트래킹 (가지치기 + DFS-like 탐색)
solved_ac: 백트래킹

[offline queries]
parent: technique
attach_when: 쿼리 정렬/재배치 (오프라인 처리)
solved_ac: 오프라인 쿼리

[sweeping]
parent: technique
attach_when: 스위핑 (line sweep, event-based)
solved_ac: 스위핑

[sqrt decomposition]
parent: technique
attach_when: 평방 분할 (블록 단위 처리)
solved_ac: 제곱근 분할법

[mo's algorithm]
parent: technique
attach_when: Mo's algorithm (오프라인 쿼리 + sqrt decomposition)
solved_ac: Mo's

## 9. game theory (2)

[game theory]
attach_when: 게임 이론이 풀이의 핵심 (Nim, 최적 게임 등)
solved_ac: 게임 이론

[sprague grundy]
parent: game theory
attach_when: 스프라그-그런디 정리 (그런디 수 계산)
solved_ac: 스프라그–그런디 정리

## 10. implementation (1)

[implementation]
attach_when: 코드 구현 자체가 복잡한 문제 (엣지 케이스, 상태 관리, parsing 등)
solved_ac: 구현
note: **구현이 본체인 문제에만** 부착. 그리디·dp 등 알고리즘적 통찰이 본체면 제외 — 35296 아침 점호가 `[greedy]` 단독인 근거(엣지 케이스가 있어도 그리디가 실질). 발행본 22건의 기준선은 2480 주사위 세개·8958 OX퀴즈처럼 알고리즘 없이 규칙을 코드로 옮기는 문제. 엣지 케이스 유무로 붙이기 시작하면 거의 모든 문제에 붙어 검색 가치가 사라짐 (2026-07-17 확정)

## 11. simulation (1)

[simulation]
attach_when: 주어진 시나리오/규칙을 그대로 따라가는 문제
solved_ac: 시뮬레이션

## 12. brute force (1)

[brute force]
attach_when: 모든 가능한 경우 시도 (가지치기 없는 완전 탐색)
solved_ac: 브루트포스 알고리즘
note: backtracking(technique)과 구분 — backtracking은 가지치기 + DFS-like

## 13. ad hoc (1)

[ad hoc]
attach_when: 특정 알고리즘 없이 case-by-case 추론
solved_ac: 애드 혹
note: 수학 논증 + case 분석으로 $O(1)$ 공식을 도출하는 글은 `math`와 **함께** 부착 (28123, 33702). 공식 하나로 끝나고 case를 안 가르면 `math` 단독 (2292 벌집, 2869 달팽이).
note: **홀짝/parity 태그는 신설 보류** — 33702 비밀번호의 이분 색칠 논증(홀수칸 5 / 짝수칸 4)을 정확히 가리킬 어휘가 없어 `ad hoc`이 대신 받고 있음. 근거가 글 1개뿐이고 solved.ac에도 대응 태그가 없어 `solved_ac:` 매핑이 빈다. 같은 논증의 글이 2~3개 쌓이면 그때 `parity`(math 산하) 신설 후 `tag_migrate`로 소급 부착할 것 (2026-07-17 판단)

## 14. constructive (1)

[constructive]
attach_when: 답을 step-by-step 구성 (예시 만들기)
solved_ac: 해 구성하기

## 15. warm up (1)

[warm up]
attach_when: PS 추론이나 알고리즘 없이 프로그래밍 언어 사용법(입출력, 기초 자료형, 사칙연산, 문자열 인덱싱, 단순 출력 등) 연습 수준의 문제
note: 난이도 표시에 가까운 outlier 카테고리. 다른 algorithm 태그가 매칭되지 않는 trivial 글에만 부착. 다른 태그와 배타는 강제하지 않으나 단독 사용이 자연스러움.

---

# Change Log

- 2026-04-09: 초기 작성 (131 vocab entries = 130 attachable + 1 auto_companion=false). 태그 분류 체계 3차 갱신 후 단일 진실 소스로 codify.
- 2026-04-09: 15번째 카테고리 `warm up` 신설 (단일 태그). 알고리즘적 추론 없이 언어 사용법만 연습하는 수준의 trivial 문제용. 132 vocab entries (131 attachable + 1 auto_companion=false).
- 2026-04-09: **Umbrella 단독 부착 허용 디자인 변경**. 16개 umbrella 카테고리(data structure, graph, tree, shortest path, mst, scc, network flow, dp, dp optimization, string, math, number theory, combinatorics, linear algebra, polynomial, geometry)의 attach_when에 단독 부착 조건 추가. game theory는 이미 standalone. technique은 여전히 auto_companion=false 유지.
- 2026-04-09: `palindrome`, `anagram` 신규 태그 추가 (string 산하). `manacher`의 parent를 string → palindrome으로 이동 (semantic 정확성). 134 vocab entries (133 attachable + 1 auto_companion=false).
- 2026-04-09: `pythagorean theorem` 신규 태그 추가 (geometry 산하). 피타고라스 정리 활용. 135 vocab entries (134 attachable + 1 auto_companion=false).
- 2026-04-09: `attach warm up --post 10171` — 1 post
- 2026-04-09: `attach warm up --post 10172` — 1 post
- 2026-04-09: `attach warm up --post 23795` — 1 post
- 2026-04-09: `attach warm up --post 15964` — 1 post
- 2026-04-09: `attach warm up --post 10189` — 1 post
- 2026-04-09: `attach warm up --post 10718` — 1 post
- 2026-04-09: `attach warm up --post 11942` — 1 post
- 2026-04-09: `attach warm up --post 14645` — 1 post
- 2026-04-09: `attach warm up --post 15680` — 1 post
- 2026-04-09: `attach warm up --post 15733` — 1 post
- 2026-04-09: `attach warm up --post 31654` — 1 post
- 2026-04-09: `attach warm up --post 4101` — 1 post
- 2026-04-09: `attach warm up --post 5338` — 1 post
- 2026-04-09: `attach warm up --post 5717` — 1 post
- 2026-04-09: `attach warm up --post 9316` — 1 post
- 2026-04-09: `attach warm up --post 9653` — 1 post
- 2026-04-09: `attach warm up --post 10170` — 1 post
- 2026-04-09: `attach warm up --post 5337` — 1 post
- 2026-04-09: `attach warm up --post 5339` — 1 post
- 2026-04-09: `attach warm up --post 7891` — 1 post
- 2026-04-09: `attach warm up --post 27327` — 1 post
- 2026-04-09: `attach warm up --post 31450` — 1 post
- 2026-04-09: `attach warm up --post 31606` — 1 post
- 2026-04-09: `attach warm up --post 31614` — 1 post
- 2026-04-09: `attach warm up --post 32951` — 1 post
- 2026-04-09: `attach warm up --post 33165` — 1 post
- 2026-04-09: `attach warm up --post 2752` — 1 post
- 2026-04-09: `attach warm up --post 16170` — 1 post
- 2026-04-09: `attach warm up --post 11721` — 1 post
- 2026-04-09: `attach warm up --post 4458` — 1 post
- 2026-04-09: `attach warm up --post 2920` — 1 post
- 2026-04-09: `attach warm up --post 10797` — 1 post
- 2026-04-09: `attach warm up --post 11944` — 1 post
- 2026-04-09: `attach warm up --post 10178` — 1 post
- 2026-04-09: `attach warm up --post 10214` — 1 post
- 2026-04-09: `attach warm up --post 13136` — 1 post
- 2026-04-09: `attach warm up --post 16486` — 1 post
- 2026-04-09: `attach warm up --post 17247` — 1 post
- 2026-04-09: `attach warm up --post 3034` — 1 post
- 2026-04-09: `attach warm up --post 5598` — 1 post
- 2026-04-09: `attach warm up --post 1237` — 1 post
- 2026-04-09: `attach warm up --post 2393` — 1 post
- 2026-04-09: `attach hash set／hash map --post 1845` — 1 post
- 2026-04-09: `attach hash set／hash map --post 42576` — 1 post
- 2026-04-09: `attach hash set／hash map --post 42578` — 1 post
- 2026-04-09: `attach combinatorics --post 42578` — 1 post
- 2026-04-09: `attach sorting --post 11004` — 1 post
- 2026-04-09: `attach simulation --post 2947` — 1 post
- 2026-04-09: `attach sorting --post 2947` — 1 post
- 2026-04-09: `recompute-ancestry` — 1 posts
- 2026-04-09: `detach sorting --post 2947` — 1 post
- 2026-04-09: `detach warm up --post 16486` — 1 post
- 2026-04-09: `attach math --post 16486` — 1 post
- 2026-04-09: `attach geometry --post 16486` — 1 post
- 2026-04-09: `detach math --post 16486` — 1 post
- 2026-04-09: `detach warm up --post 3034` — 1 post
- 2026-04-09: `attach geometry --post 3034` — 1 post
- 2026-04-09: `detach geometry --post 3034` — 1 post
- 2026-04-09: `attach pythagorean theorem --post 3034` — 1 post
- 2026-04-09: `detach warm up --post 17247` — 1 post
- 2026-04-09: `attach geometry --post 17247` — 1 post
- 2026-04-09: `detach warm up --post 5598` — 1 post
- 2026-04-09: `attach string --post 5598` — 1 post
- 2026-04-09: `attach warm up --post 10430` — 1 post
- 2026-04-09: `attach warm up --post 11382` — 1 post
- 2026-04-09: `attach warm up --post 10093` — 1 post
- 2026-04-09: `attach simulation --post 10804` — 1 post
- 2026-04-09: `attach warm up --post 1267` — 1 post
- 2026-04-09: `attach warm up --post 13752` — 1 post
- 2026-04-09: `attach warm up --post 23037` — 1 post
- 2026-04-09: `attach brute force --post 2309` — 1 post
- 2026-04-09: `attach warm up --post 23825` — 1 post
- 2026-04-09: `attach warm up --post 2490` — 1 post
- 2026-04-09: `attach warm up --post 2576` — 1 post
- 2026-04-09: `attach greedy --post 5585` — 1 post
- 2026-04-09: `attach warm up --post 2083` — 1 post
- 2026-04-09: `attach warm up --post 10808` — 1 post
- 2026-04-09: `attach warm up --post 2693` — 1 post
- 2026-04-09: `attach backtracking --post 15649` — 1 post
- 2026-04-09: `attach backtracking --post 15650` — 1 post
- 2026-04-09: `attach backtracking --post 15651` — 1 post
- 2026-04-09: `attach backtracking --post 15652` — 1 post
- 2026-04-09: `attach backtracking --post 15654` — 1 post
- 2026-04-09: `attach backtracking --post 15655` — 1 post
- 2026-04-09: `attach backtracking --post 15656` — 1 post
- 2026-04-09: `attach backtracking --post 15657` — 1 post
- 2026-04-09: `attach backtracking --post 15663` — 1 post
- 2026-04-09: `attach backtracking --post 15664` — 1 post
- 2026-04-09: `attach backtracking --post 15665` — 1 post
- 2026-04-09: `attach backtracking --post 15666` — 1 post
- 2026-04-09: `attach backtracking --post 6603` — 1 post
- 2026-04-09: `attach hash set／hash map --post 10546` — 1 post
- 2026-04-09: `attach hash set／hash map --post 27964` — 1 post
- 2026-04-09: `attach warm up --post 15962` — 1 post
- 2026-04-09: `attach warm up --post 4999` — 1 post
- 2026-04-09: `attach warm up --post 15963` — 1 post
- 2026-04-09: `attach geometry --post 14681` — 1 post
- 2026-04-09: `attach warm up --post 18108` — 1 post
- 2026-04-09: `attach warm up --post 25083` — 1 post
- 2026-04-09: `attach geometry --post 27323` — 1 post
- 2026-04-09: `attach sorting --post 10989` — 1 post
- 2026-04-09: `attach sorting --post 1427` — 1 post
- 2026-04-09: `attach geometry --post 15894` — 1 post
- 2026-04-09: `attach sorting --post 2750` — 1 post
- 2026-04-09: `attach sorting --post 2751` — 1 post
- 2026-04-09: `attach sorting --post 11650` — 1 post
- 2026-04-09: `attach sorting --post 11651` — 1 post
- 2026-04-09: `attach hash set／hash map --post 1620` — 1 post
- 2026-04-09: `attach warm up --post 28113` — 1 post
- 2026-04-09: `attach geometry --post 29751` — 1 post
- 2026-04-09: `attach stack --post 10773` — 1 post
- 2026-04-09: `attach combinatorics --post 15439` — 1 post
- 2026-04-09: `attach warm up --post 31429` — 1 post
- 2026-04-09: `attach warm up --post 31610` — 1 post
- 2026-04-09: `attach warm up --post 31611` — 1 post
- 2026-04-09: `attach warm up --post 10102` — 1 post
- 2026-04-09: `attach warm up --post 10817` — 1 post
- 2026-04-09: `attach warm up --post 10886` — 1 post
- 2026-04-09: `attach warm up --post 10987` — 1 post
- 2026-04-09: `attach warm up --post 11365` — 1 post
- 2026-04-09: `attach warm up --post 3046` — 1 post
- 2026-04-09: `attach warm up --post 5543` — 1 post
- 2026-04-09: `attach warm up --post 5565` — 1 post
- 2026-04-09: `attach geometry --post 9610` — 1 post
- 2026-04-09: `attach greedy --post 26099` — 1 post
- 2026-04-09: `attach greedy --post 2839` — 1 post
- 2026-04-09: `attach sorting --post 11931` — 1 post
- 2026-04-09: `attach sorting --post 15688` — 1 post
- 2026-04-09: `attach warm up --post 10768` — 1 post
- 2026-04-09: `attach sorting --post 10867` — 1 post
- 2026-04-09: `attach math --post 2355` — 1 post
- 2026-04-09: `attach warm up --post 4470` — 1 post
- 2026-04-09: `attach constructive --post 33701` — 1 post
- 2026-04-09: `attach geometry --post 16478` — 1 post
- 2026-04-09: `attach implementation --post 2480` — 1 post
- 2026-04-09: `attach warm up --post 2739` — 1 post
- 2026-04-09: `attach geometry --post 10101` — 1 post
- 2026-04-09: `attach warm up --post 11718` — 1 post
- 2026-04-09: `attach warm up --post 2908` — 1 post
- 2026-04-09: `attach string --post 9086` — 1 post
- 2026-04-09: `attach warm up --post 10821` — 1 post
- 2026-04-09: `attach geometry --post 9063` — 1 post
- 2026-04-09: `attach greedy --post 2720` — 1 post
- 2026-04-09: `attach queue --post 1158` — 1 post
- 2026-04-09: `attach simulation --post 1158` — 1 post
- 2026-04-09: `attach queue --post 11866` — 1 post
- 2026-04-09: `attach simulation --post 11866` — 1 post
- 2026-04-09: `attach brute force --post 19532` — 1 post
- 2026-04-09: `attach hash set／hash map --post 11478` — 1 post
- 2026-04-09: `attach string --post 11478` — 1 post
- 2026-04-09: `attach math --post 24723` — 1 post
- 2026-04-09: `attach hash set／hash map --post 1269` — 1 post
- 2026-04-09: `attach tree set／tree map --post 7785` — 1 post
- 2026-04-09: `attach math --post 10872` — 1 post
- 2026-04-09: `attach warm up --post 2420` — 1 post
- 2026-04-09: `attach math --post 27433` — 1 post
- 2026-04-09: `attach math --post 16430` — 1 post
- 2026-04-09: `attach warm up --post 30030` — 1 post
- 2026-04-09: `attach warm up --post 32929` — 1 post
- 2026-04-09: `attach implementation --post 2476` — 1 post
- 2026-04-09: `attach math --post 2577` — 1 post
- 2026-04-09: `attach warm up --post 9295` — 1 post
- 2026-04-09: `attach simulation --post 10103` — 1 post
- 2026-04-09: `attach warm up --post 1264` — 1 post
- 2026-04-09: `attach warm up --post 3058` — 1 post
- 2026-04-09: `attach warm up --post 5063` — 1 post
- 2026-04-09: `attach warm up --post 5988` — 1 post
- 2026-04-09: `attach warm up --post 1271` — 1 post
- 2026-04-09: `attach warm up --post 1550` — 1 post
- 2026-04-09: `attach warm up --post 11719` — 1 post
- 2026-04-09: `attach greedy --post 10162` — 1 post
- 2026-04-09: `attach geometry --post 9366` — 1 post
- 2026-04-09: `attach anagram --post 11328` — 1 post
- 2026-04-09: `attach implementation --post 1475` — 1 post
- 2026-04-09: `attach anagram --post 1919` — 1 post
- 2026-04-10: `attach warm up --post 10869` — 1 post
- 2026-04-10: `attach warm up --post 10871` — 1 post
- 2026-04-10: `attach warm up --post 25304` — 1 post
- 2026-04-10: `attach warm up --post 25314` — 1 post
- 2026-04-10: `attach warm up --post 5597` — 1 post
- 2026-04-10: `attach warm up --post 10809` — 1 post
- 2026-04-10: `attach warm up --post 1152` — 1 post
- 2026-04-10: `attach math --post 11720` — 1 post
- 2026-04-10: `attach warm up --post 2738` — 1 post
- 2026-04-10: `attach warm up --post 2743` — 1 post
- 2026-04-10: `attach warm up --post 2745` — 1 post
- 2026-04-10: `attach math --post 11005` — 1 post
- 2026-04-10: `attach warm up --post 3052` — 1 post
- 2026-04-10: `attach warm up --post 5086` — 1 post
- 2026-04-10: `attach prefix sum --post 11441` — 1 post
- 2026-04-10: `attach prefix sum --post 11659` — 1 post
- 2026-04-10: `attach 2d prefix sum --post 11660` — 1 post
- 2026-04-10: `attach geometry --post 5073` — 1 post
- 2026-04-10: `attach meet in the middle --post 2295` — 1 post
- 2026-04-10: `attach binary search --post 2295` — 1 post
- 2026-04-10: `attach greedy --post 11047` — 1 post
- 2026-04-10: `attach sorting --post 1181` — 1 post
- 2026-04-10: `attach sorting --post 1764` — 1 post
- 2026-04-10: `attach hash set／hash map --post 1764` — 1 post
- 2026-04-10: `attach brute force --post 1436` — 1 post
- 2026-04-10: `attach warm up --post 2475` — 1 post
- 2026-04-10: `attach warm up --post 2744` — 1 post
- 2026-04-10: `attach warm up --post 2754` — 1 post
- 2026-04-10: `attach warm up --post 2530` — 1 post
- 2026-04-10: `attach warm up --post 2845` — 1 post
- 2026-04-10: `attach warm up --post 21867` — 1 post
- 2026-04-10: `attach warm up --post 33964` — 1 post
- 2026-04-10: `attach greedy --post 10610` — 1 post
- 2026-04-10: `attach math --post 10610` — 1 post
- 2026-04-10: `attach simulation --post 25594` — 1 post
- 2026-04-10: `attach constructive --post 35308` — 1 post
- 2026-04-10: `attach math --post 35308` — 1 post
- 2026-04-10: `attach stack --post 35309` — 1 post
- 2026-04-10: `attach simulation --post 35309` — 1 post
- 2026-04-10: `attach deque --post 1406` — 1 post
- 2026-04-10: `attach deque --post 5397` — 1 post
- 2026-04-10: `detach math --post 11720` — 1 post
- 2026-04-10: `attach warm up --post 11720` — 1 post
- 2026-04-10: `attach hash set／hash map --post 3052` — 1 post
- 2026-04-10: `attach hash set／hash map --post 2295` — 1 post
- 2026-04-10: `detach simulation --post 25594` — 1 post
- 2026-04-10: `attach implementation --post 25594` — 1 post
- 2026-04-10: `detach simulation --post 35309` — 1 post
- 2026-04-10: `attach greedy --post 35309` — 1 post
- 2026-04-10: `detach sorting --post 1764` — 1 post
- 2026-04-10: `attach tree set／tree map --post 1764` — 1 post
- 2026-04-10: `attach sorting --post 10610` — 1 post
- 2026-04-10: `detach math --post 35308` — 1 post
- 2026-04-10: `attach ad hoc --post 35308` — 1 post
- 2026-04-10: `attach implementation --post 35309` — 1 post
- 2026-04-10: `attach warm up --post 1330` — 1 post
- 2026-04-10: `attach warm up --post 2525` — 1 post
- 2026-04-10: `attach warm up --post 2884` — 1 post
- 2026-04-10: `attach warm up --post 2675` — 1 post
- 2026-04-10: `attach warm up --post 27866` — 1 post
- 2026-04-10: `attach pythagorean theorem --post 2756` — 1 post
- 2026-04-10: `attach implementation --post 2756` — 1 post
- 2026-04-10: `attach pythagorean theorem --post 4153` — 1 post
- 2026-04-10: `attach pythagorean theorem --post 16479` — 1 post
- 2026-04-10: `attach two pointers --post 3273` — 1 post
- 2026-04-10: `attach sorting --post 3273` — 1 post
- 2026-04-10: `attach two pointers --post 11728` — 1 post
- 2026-04-10: `attach sorting --post 11728` — 1 post
- 2026-04-10: `attach two pointers --post 7795` — 1 post
- 2026-04-10: `attach binary search --post 7795` — 1 post
- 2026-04-10: `attach sorting --post 7795` — 1 post
- 2026-04-10: `attach two pointers --post 20922` — 1 post
- 2026-04-10: `attach binomial coefficient --post 1010` — 1 post
- 2026-04-10: `attach stack --post 4949` — 1 post
- 2026-04-10: `attach stack --post 9012` — 1 post
- 2026-04-10: `attach dp --post 1932` — 1 post
- 2026-04-10: `attach dp --post 11726` — 1 post
- 2026-04-10: `attach dp --post 11727` — 1 post
- 2026-04-10: `attach greedy --post 11399` — 1 post
- 2026-04-10: `attach sorting --post 11399` — 1 post
- 2026-04-10: `attach greedy --post 13305` — 1 post
- 2026-04-10: `attach warm up --post 14910` — 1 post
- 2026-04-10: `attach greedy --post 32529` — 1 post
- 2026-04-10: `attach implementation --post 35306` — 1 post
- 2026-04-10: `attach stack --post 2504` — 1 post
- 2026-04-10: `attach stack --post 3986` — 1 post
- 2026-04-10: `attach stack --post 10799` — 1 post
- 2026-04-10: `attach greedy --post 2847` — 1 post
- 2026-04-10: `attach greedy --post 11501` — 1 post
- 2026-04-10: `attach dp --post 43105` — 1 post
- 2026-04-10: `attach dp --post 12900` — 1 post
- 2026-04-10: `attach flood fill --post 154540` — 1 post
- 2026-04-10: `attach bfs --post 154540` — 1 post
- 2026-04-10: `detach warm up --post 2693` — 1 post
- 2026-04-10: `attach sorting --post 2693` — 1 post
- 2026-04-10: `detach warm up --post 2752` — 1 post
- 2026-04-10: `attach sorting --post 2752` — 1 post
- 2026-04-10: `detach string --post 9086` — 1 post
- 2026-04-10: `attach warm up --post 9086` — 1 post
- 2026-04-10: `detach sorting --post 10867` — 1 post
- 2026-04-10: `detach simulation --post 10103` — 1 post
- 2026-04-10: `attach implementation --post 10103` — 1 post
- 2026-04-10: `attach math --post 16478` — 1 post
- 2026-04-10: `attach warm up --post 10867` — 1 post
- 2026-04-10: `detach warm up --post 33964` — 1 post
- 2026-04-10: `attach math --post 33964` — 1 post
- 2026-04-10: `detach warm up --post 10817` — 1 post
- 2026-04-10: `attach sorting --post 10817` — 1 post
- 2026-04-10: `detach warm up --post 2754` — 1 post
- 2026-04-10: `attach implementation --post 2754` — 1 post
- 2026-04-10: `detach warm up --post 5086` — 1 post
- 2026-04-10: `attach number theory --post 5086` — 1 post
- 2026-04-10: `attach warm up --post 2753` — 1 post
- 2026-04-10: `attach bfs --post 1012` — 1 post
- 2026-04-10: `attach dfs --post 1012` — 1 post
- 2026-04-10: `attach flood fill --post 1012` — 1 post
- 2026-04-10: `attach bfs --post 1260` — 1 post
- 2026-04-10: `attach dfs --post 1260` — 1 post
- 2026-04-10: `attach bfs --post 2178` — 1 post
- 2026-04-10: `attach bfs --post 2606` — 1 post
- 2026-04-10: `attach dfs --post 2606` — 1 post
- 2026-04-10: `attach bfs --post 9328` — 1 post
- 2026-04-10: `attach implementation --post 9328` — 1 post
- 2026-04-10: `attach bfs --post 6593` — 1 post
- 2026-04-10: `attach bfs --post 7562` — 1 post
- 2026-04-10: `attach bfs --post 9019` — 1 post
- 2026-04-10: `attach bfs --post 10026` — 1 post
- 2026-04-10: `attach dfs --post 10026` — 1 post
- 2026-04-10: `attach flood fill --post 10026` — 1 post
- 2026-04-10: `attach bfs --post 1926` — 1 post
- 2026-04-10: `attach dfs --post 1926` — 1 post
- 2026-04-10: `attach flood fill --post 1926` — 1 post
- 2026-04-10: `attach bfs --post 2468` — 1 post
- 2026-04-10: `attach dfs --post 2468` — 1 post
- 2026-04-10: `attach flood fill --post 2468` — 1 post
- 2026-04-10: `attach brute force --post 2468` — 1 post
- 2026-04-10: `attach bfs --post 2583` — 1 post
- 2026-04-10: `attach dfs --post 2583` — 1 post
- 2026-04-10: `attach flood fill --post 2583` — 1 post
- 2026-04-10: `attach bfs --post 2638` — 1 post
- 2026-04-10: `attach flood fill --post 2638` — 1 post
- 2026-04-10: `attach simulation --post 2638` — 1 post
- 2026-04-10: `attach bfs --post 2667` — 1 post
- 2026-04-10: `attach dfs --post 2667` — 1 post
- 2026-04-10: `attach flood fill --post 2667` — 1 post
- 2026-04-10: `attach bfs --post 4963` — 1 post
- 2026-04-10: `attach dfs --post 4963` — 1 post
- 2026-04-10: `attach flood fill --post 4963` — 1 post
- 2026-04-10: `attach bfs --post 14940` — 1 post
- 2026-04-10: `attach bfs --post 2644` — 1 post
- 2026-04-10: `attach bfs --post 4179` — 1 post
- 2026-04-10: `attach bfs --post 5014` — 1 post
- 2026-04-10: `attach bfs --post 5427` — 1 post
- 2026-04-10: `attach bfs --post 5567` — 1 post
- 2026-04-10: `attach bfs --post 7569` — 1 post
- 2026-04-10: `attach bfs --post 7576` — 1 post
- 2026-04-10: `attach bfs --post 1600` — 1 post
- 2026-04-10: `attach bfs --post 21736` — 1 post
- 2026-04-10: `attach dfs --post 21736` — 1 post
- 2026-04-10: `attach flood fill --post 21736` — 1 post
- 2026-04-10: `attach warm up --post 8393` — 1 post
- 2026-04-10: `attach math --post 8393` — 1 post
- 2026-04-10: `attach warm up --post 2588` — 1 post
- 2026-04-10: `attach warm up --post 9498` — 1 post
- 2026-04-10: `attach warm up --post 1546` — 1 post
- 2026-04-10: `attach warm up --post 2562` — 1 post
- 2026-04-10: `attach warm up --post 10807` — 1 post
- 2026-04-10: `attach warm up --post 10810` — 1 post
- 2026-04-10: `attach warm up --post 10811` — 1 post
- 2026-04-10: `attach warm up --post 10813` — 1 post
- 2026-04-10: `attach warm up --post 10818` — 1 post
- 2026-04-10: `attach warm up --post 2438` — 1 post
- 2026-04-10: `attach warm up --post 2439` — 1 post
- 2026-04-10: `attach warm up --post 2440` — 1 post
- 2026-04-10: `attach warm up --post 2441` — 1 post
- 2026-04-10: `attach warm up --post 2442` — 1 post
- 2026-04-10: `attach warm up --post 2443` — 1 post
- 2026-04-10: `attach warm up --post 2444` — 1 post
- 2026-04-10: `attach warm up --post 2445` — 1 post
- 2026-04-10: `attach warm up --post 2446` — 1 post
- 2026-04-10: `attach warm up --post 2522` — 1 post
- 2026-04-10: `attach warm up --post 2523` — 1 post
- 2026-04-10: `attach warm up --post 10990` — 1 post
- 2026-04-10: `attach warm up --post 10991` — 1 post
- 2026-04-10: `attach warm up --post 10995` — 1 post
- 2026-04-10: `attach warm up --post 10996` — 1 post
- 2026-04-10: `attach euclidean --post 1735` — 1 post
- 2026-04-10: `attach euclidean --post 1934` — 1 post
- 2026-04-10: `attach euclidean --post 2485` — 1 post
- 2026-04-10: `attach euclidean --post 2609` — 1 post
- 2026-04-10: `attach euclidean --post 5347` — 1 post
- 2026-04-10: `attach euclidean --post 9613` — 1 post
- 2026-04-10: `attach euclidean --post 13241` — 1 post
- 2026-04-10: `attach euclidean --post 17087` — 1 post
- 2026-04-10: `attach geometry --post 1085` — 1 post
- 2026-04-10: `attach divide and conquer --post 1780` — 1 post
- 2026-04-10: `attach divide and conquer --post 2630` — 1 post
- 2026-04-10: `attach divide and conquer --post 1992` — 1 post
- 2026-04-10: `attach divide and conquer --post 14956` — 1 post
- 2026-04-10: `attach divide and conquer --post 2447` — 1 post
- 2026-04-10: `attach divide and conquer --post 2448` — 1 post
- 2026-04-10: `attach game theory --post 11694` — 1 post
- 2026-04-10: `attach game theory --post 11868` — 1 post
- 2026-04-10: `attach game theory --post 11869` — 1 post
- 2026-04-10: `attach sprague grundy --post 11871` — 1 post
- 2026-04-10: `attach sprague grundy --post 16877` — 1 post
- 2026-04-10: `attach game theory --post 16895` — 1 post
- 2026-04-10: `attach sprague grundy --post 5386` — 1 post
- 2026-04-10: `attach divide and conquer --post 1074` — 1 post
- 2026-04-10: `attach divide and conquer --post 11729` — 1 post
- 2026-04-10: `attach sprague grundy --post 11872` — 1 post
- 2026-04-10: `attach sprague grundy --post 13034` — 1 post
- 2026-04-10: `attach warm up --post 17478` — 1 post
- 2026-04-10: `attach sprague grundy --post 18937` — 1 post
- 2026-04-10: `attach game theory --post 9655` — 1 post
- 2026-04-10: `attach game theory --post 9656` — 1 post
- 2026-04-10: `attach dp --post 9657` — 1 post
- 2026-04-10: `attach game theory --post 9657` — 1 post
- 2026-04-10: `attach dp --post 9658` — 1 post
- 2026-04-10: `attach game theory --post 9658` — 1 post
- 2026-04-10: `attach game theory --post 9659` — 1 post
- 2026-04-10: `attach dp --post 9660` — 1 post
- 2026-04-10: `attach game theory --post 9660` — 1 post
- 2026-04-10: `attach sprague grundy --post 11694` — 1 post
- 2026-04-10: `attach sprague grundy --post 11868` — 1 post
- 2026-04-10: `attach sprague grundy --post 11869` — 1 post
- 2026-04-10: `attach sprague grundy --post 16895` — 1 post
- 2026-04-10: `detach warm up --post 17478` — 1 post
- 2026-04-10: `attach implementation --post 17478` — 1 post
- 2026-04-10: `detach dp --post 9660` — 1 post
- 2026-07-15: `attach sorting --post 42746` — 1 post
- 2026-07-15: `attach sorting --post 42747` — 1 post
- 2026-07-15: `attach binary search --post 42747` — 1 post
- 2026-07-15: `attach sorting --post 42748` — 1 post
- 2026-07-15: `attach pythagorean theorem --post 181187` — 1 post
- 2026-07-15: `attach greedy --post 138476` — 1 post
- 2026-07-15: `attach sorting --post 138476` — 1 post
- 2026-07-15: `attach bfs --post 154538` — 1 post
- 2026-07-15: `attach dp --post 154538` — 1 post
- 2026-07-15: `attach greedy --post 42746` — 1 post
- 2026-07-16: `attach greedy --post 1422` — 1 post
- 2026-07-16: `attach sorting --post 1422` — 1 post
- 2026-07-16: `attach greedy --post 16496` — 1 post
- 2026-07-16: `attach sorting --post 16496` — 1 post
- 2026-07-16: `attach greedy --post 29119` — 1 post
- 2026-07-16: `attach sorting --post 29119` — 1 post
- 2026-07-16: `attach warm up --post 24883` — 1 post
- 2026-07-16: `attach greedy --post 14908` — 1 post
- 2026-07-16: `attach sorting --post 14908` — 1 post
- 2026-07-16: `attach warm up --post 1292` — 1 post
- 2026-07-16: `attach ad hoc --post 11943` — 1 post
- 2026-07-16: `attach constructive --post 1201` — 1 post
- 2026-07-16: `attach greedy --post 1201` — 1 post
- 2026-07-16: `detach ad hoc --post 11943` — 1 post
- 2026-07-16: `attach math --post 11943` — 1 post
- 2026-07-16: `prime factorization`의 `solved_ac` 매핑 오타 수정 (`소수 판정` → `소인수분해`). solved.ac는 `소인수분해`와 `소수 판정`을 별도 태그로 두는데 잘못 연결되어 있어 리뷰 시 소수 판정 문제에 `prime factorization`을 붙이도록 오도할 수 있었음. 어휘 자체는 변경 없음(135 entries 유지).
- 2026-07-16: `sieve` → `sieve of eratosthenes` 리네임 — 8 posts. "sieve"는 선형 체·구간 체·앳킨의 체 등과 모호해 정식 명칭으로 확정. `sieve` umbrella는 두지 않고 `number theory` 산하 flat sibling 유지(`miller rabin`·`pollard rho`와 동일 패턴) — 향후 `linear sieve`/`segmented sieve`는 형제로 추가. 어휘 수 변동 없음(135 entries).
- 2026-07-16: `attach implementation --post 1157` / `--post 25206` — 2 posts
- 2026-07-16: `attach string --post 2941` / `attach implementation --post 2941` — 1 post
- 2026-07-16: `attach geometry --post 3009` / `attach bitmask --post 3009` — 1 post
- 2026-07-16: `attach prime factorization --post 11653` / `--post 2312` — 2 posts
- 2026-07-16: `attach sieve of eratosthenes --post 1929` / `1978` / `2581` / `15965` / `2312` / `2960` / `1644` / `1963` — 8 posts
- 2026-07-16: `attach math --post 2292` / `--post 2148A` — 2 posts
- 2026-07-16: `attach brute force --post 2501` / `--post 2003` — 2 posts
- 2026-07-16: `attach pythagorean theorem --post 1064` / `attach ccw --post 1064` — 1 post
- 2026-07-16: `attach binary exponentiation --post 1629` — 1 post
- 2026-07-16: `attach sliding window --post 1522` / `1593` / `2559` — 3 posts
- 2026-07-16: `attach anagram --post 1593` — 1 post
- 2026-07-16: `attach two pointers --post 1644` / `2003` / `2230` — 3 posts
- 2026-07-16: `attach binary search --post 1654` / `attach parametric search --post 1654` — 1 post
- 2026-07-16: `attach greedy --post 1789` — 1 post
- 2026-07-16: `attach bfs --post 1963` — 1 post
- 2026-07-16: `attach prefix sum --post 2003` / `--post 2559` — 2 posts
- 2026-07-16: `attach sorting --post 2230` — 1 post
- 2026-07-16: `attach palindrome --post 9` — 1 post
- 2026-07-16: `attach implementation --post 1157` — 1 post
- 2026-07-16: `attach implementation --post 25206` — 1 post
- 2026-07-16: `attach string --post 2941` — 1 post
- 2026-07-16: `attach implementation --post 2941` — 1 post
- 2026-07-16: `attach geometry --post 3009` — 1 post
- 2026-07-16: `attach bitmask --post 3009` — 1 post
- 2026-07-16: `attach prime factorization --post 11653` — 1 post
- 2026-07-16: `attach sieve --post 1929` — 1 post
- 2026-07-16: `attach sieve --post 1978` — 1 post
- 2026-07-16: `attach math --post 2292` — 1 post
- 2026-07-16: `attach brute force --post 2501` — 1 post
- 2026-07-16: `attach sieve --post 2581` — 1 post
- 2026-07-16: `attach pythagorean theorem --post 1064` — 1 post
- 2026-07-16: `attach ccw --post 1064` — 1 post
- 2026-07-16: `attach sieve --post 15965` — 1 post
- 2026-07-16: `attach binary exponentiation --post 1629` — 1 post
- 2026-07-16: `attach prime factorization --post 2312` — 1 post
- 2026-07-16: `attach sieve --post 2312` — 1 post
- 2026-07-16: `attach sieve --post 2960` — 1 post
- 2026-07-16: `attach sliding window --post 1522` — 1 post
- 2026-07-16: `attach sliding window --post 1593` — 1 post
- 2026-07-16: `attach anagram --post 1593` — 1 post
- 2026-07-16: `attach sieve --post 1644` — 1 post
- 2026-07-16: `attach two pointers --post 1644` — 1 post
- 2026-07-16: `attach binary search --post 1654` — 1 post
- 2026-07-16: `attach parametric search --post 1654` — 1 post
- 2026-07-16: `attach greedy --post 1789` — 1 post
- 2026-07-16: `attach sieve --post 1963` — 1 post
- 2026-07-16: `attach bfs --post 1963` — 1 post
- 2026-07-16: `attach prefix sum --post 2003` — 1 post
- 2026-07-16: `attach two pointers --post 2003` — 1 post
- 2026-07-16: `attach brute force --post 2003` — 1 post
- 2026-07-16: `attach two pointers --post 2230` — 1 post
- 2026-07-16: `attach sorting --post 2230` — 1 post
- 2026-07-16: `attach prefix sum --post 2559` — 1 post
- 2026-07-16: `attach sliding window --post 2559` — 1 post
- 2026-07-16: `attach math --post 2148A` — 1 post
- 2026-07-16: `attach palindrome --post 9` — 1 post
- 2026-07-16: `rename sieve -> sieve of eratosthenes` — 8 posts
- 2026-07-16: `rename euclidean -> euclidean algorithm` — 8 posts
- 2026-07-16: `rename extended euclidean -> extended euclidean algorithm` — 0 posts
- 2026-07-17: `bfs`/`shortest path` 부착 기준 확정 — 무가중치 BFS로 최소 이동 횟수를 구하는 문제는 `shortest path`를 붙이지 않고 `bfs` 단독으로 둔다. `shortest path`는 가중치 최단경로(dijkstra/bellman ford/floyd warshall/0-1 bfs) 전용. 기존 `bfs` note가 반대로 지시("unweighted shortest path는 명시적으로 shortest path 추가")했으나 발행본 22/22가 이를 따르지 않았고(2178 미로 탐색, 14940 쉬운 최단거리, 1697 숨바꼭질, 7576 토마토 전부 `[graph, bfs]`), 붙일 경우 `shortest path` 검색 결과가 `bfs`와 거의 겹쳐 구분값이 사라지므로 실무 쪽으로 note를 정정. 발행본 소급 수정 없음(0 posts).
- 2026-07-17: `attach knapsack --post 16493` — 1 post
- 2026-07-17: `attach backtracking --post 16493` — 1 post
- 2026-07-17: `attach sieve of eratosthenes --post 17103` — 1 post
- 2026-07-17: `attach brute force --post 2231` — 1 post
- 2026-07-17: `attach monotonic queue --post 11003` — 1 post
- 2026-07-17: `attach priority queue --post 11003` — 1 post
- 2026-07-17: `attach sliding window --post 11003` — 1 post
- 2026-07-17: `attach monotonic queue --post 2433` — 1 post
- 2026-07-17: `attach priority queue --post 2433` — 1 post
- 2026-07-17: `attach sliding window --post 2433` — 1 post
- 2026-07-17: `attach binomial coefficient --post 11050` — 1 post
- 2026-07-17: `attach binomial coefficient --post 11051` — 1 post
- 2026-07-17: `attach dp --post 11051` — 1 post
- 2026-07-17: `attach binomial coefficient --post 11401` — 1 post
- 2026-07-17: `attach modular inverse --post 11401` — 1 post
- 2026-07-17: `attach fermat's little theorem --post 11401` — 1 post
- 2026-07-17: `attach binary exponentiation --post 11401` — 1 post
- 2026-07-17: `attach lucas' theorem --post 11402` — 1 post
- 2026-07-17: `attach binomial coefficient --post 11402` — 1 post
- 2026-07-17: `attach priority queue --post 11279` — 1 post
- 2026-07-17: `attach priority queue --post 1927` — 1 post
- 2026-07-17: `attach dp --post 1463` — 1 post
- 2026-07-17: `attach dp --post 2133` — 1 post
- 2026-07-17: `attach bfs --post 11724` — 1 post
- 2026-07-17: `attach dfs --post 11724` — 1 post
- 2026-07-17: `attach union find --post 11724` — 1 post
- 2026-07-17: `attach bfs --post 3197` — 1 post
- 2026-07-17: `attach flood fill --post 3197` — 1 post
- 2026-07-17: `attach parametric search --post 3197` — 1 post
- 2026-07-17: `attach binary search --post 3197` — 1 post
- 2026-07-17: `attach bfs --post 14442` — 1 post
- 2026-07-17: `attach bfs --post 16933` — 1 post
- 2026-07-17: `attach bfs --post 16946` — 1 post
- 2026-07-17: `attach flood fill --post 16946` — 1 post
- 2026-07-17: `attach bfs --post 2206` — 1 post
- 2026-07-17: `attach greedy --post 12904` — 1 post
- 2026-07-17: `attach string --post 12904` — 1 post
- 2026-07-17: `attach dp --post 3687` — 1 post
- 2026-07-17: `attach greedy --post 3687` — 1 post
- 2026-07-17: `attach brute force --post 12348` — 1 post
- 2026-07-17: `attach greedy --post 35296` — 1 post
- 2026-07-17: `attach implementation --post 35296` — 1 post
- 2026-07-17: `attach implementation --post 10469` — 1 post
- 2026-07-17: `attach lis --post 2631` — 1 post
- 2026-07-17: `attach math --post 28123` — 1 post
- 2026-07-17: `attach lis --post 7570` — 1 post
- 2026-07-17: `attach ad hoc --post 33702` — 1 post
- 2026-07-17: `attach union find --post 1717` — 1 post
- 2026-07-17: `attach backtracking --post 1799` — 1 post
- 2026-07-17: `attach union find --post 1976` — 1 post
- 2026-07-17: `attach union find --post 7511` — 1 post
- 2026-07-17: `attach string --post 3687` — 1 post
- 2026-07-17: `attach ad hoc --post 28123` — 1 post
- 2026-07-17: `attach math --post 33702` — 1 post
- 2026-07-17: `detach implementation --post 35296` — 1 post
- 2026-07-17: `string` 부착 기준 확정 — dp 상태값이 문자열이면 부착(3687), 숫자를 문자열로 표현만 하면 제외(11005·33964·10872·27433은 `[math]` 유지). 0 posts.
- 2026-07-17: `implementation` 부착 기준 확정 — 구현이 본체인 문제에만. 그리디/dp가 본체면 제외 → `detach implementation --post 35296` — 1 post.
- 2026-07-17: `parity` 태그 신설 보류 — 33702 1건뿐이라 근거 부족. 2~3건 쌓이면 재검토. 그때까지 `[ad hoc, math]`가 대신 받음. 0 posts.
- 2026-07-18: `attach sliding window --post 12847` — 1 post
- 2026-07-18: `attach prefix sum --post 12847` — 1 post
- 2026-07-18: `attach sliding window --post 12891` — 1 post
- 2026-07-18: `attach parametric search --post 16401` — 1 post
- 2026-07-18: `attach binary search --post 16401` — 1 post
- 2026-07-18: `attach two pointers --post 20366` — 1 post
- 2026-07-18: `attach sorting --post 20366` — 1 post
- 2026-07-18: `attach sliding window --post 21921` — 1 post
- 2026-07-18: `attach prefix sum --post 21921` — 1 post
- 2026-07-18: `attach sliding window --post 24499` — 1 post
- 2026-07-18: `attach parametric search --post 27436` — 1 post
- 2026-07-18: `attach binary search --post 27436` — 1 post
- 2026-07-18: `attach parametric search --post 2805` — 1 post
- 2026-07-18: `attach binary search --post 2805` — 1 post
- 2026-07-18: `attach binary search --post 1253` — 1 post
- 2026-07-18: `attach two pointers --post 1253` — 1 post
- 2026-07-18: `attach parametric search --post 12779` — 1 post
- 2026-07-18: `attach binary search --post 12779` — 1 post
- 2026-07-18: `attach euclidean algorithm --post 12779` — 1 post
- 2026-07-18: `attach sliding window --post 15565` — 1 post
- 2026-07-18: `attach two pointers --post 15565` — 1 post
- 2026-07-18: `attach two pointers --post 1806` — 1 post
- 2026-07-18: `attach binary search --post 1920` — 1 post
- 2026-07-18: `attach hash set／hash map --post 1920` — 1 post
- 2026-07-18: `attach binary search --post 2467` — 1 post
- 2026-07-18: `attach two pointers --post 2467` — 1 post
- 2026-07-18: `attach binary search --post 2470` — 1 post
- 2026-07-18: `attach two pointers --post 2470` — 1 post
- 2026-07-18: `attach binary search --post 2473` — 1 post
- 2026-07-18: `attach two pointers --post 2473` — 1 post
- 2026-07-18: `attach knapsack --post 12865` — 1 post
- 2026-07-18: `attach knapsack --post 12920` — 1 post
- 2026-07-18: `attach sliding window --post 17128` — 1 post
- 2026-07-18: `attach knapsack --post 2293` — 1 post
- 2026-07-18: `attach knapsack --post 2294` — 1 post
- 2026-07-18: `attach parametric search --post 2417` — 1 post
- 2026-07-18: `attach binary search --post 2417` — 1 post
- 2026-07-18: `attach knapsack --post 3067` — 1 post
- 2026-07-18: `attach knapsack --post 9084` — 1 post
- 2026-07-18: `attach matrix exponentiation --post 10830` — 1 post
- 2026-07-18: `attach bitmask --post 1094` — 1 post
- 2026-07-18: `attach knapsack --post 1106` — 1 post
- 2026-07-18: `attach greedy --post 13448` — 1 post
- 2026-07-18: `attach knapsack --post 13448` — 1 post
- 2026-07-18: `attach greedy --post 1541` — 1 post
- 2026-07-18: `attach parametric search --post 16434` — 1 post
- 2026-07-18: `attach binary search --post 16434` — 1 post
- 2026-07-18: `attach sliding window --post 20437` — 1 post
- 2026-07-18: `attach dp --post 2096` — 1 post
- 2026-07-18: `attach knapsack --post 2629` — 1 post
- 2026-07-18: `attach prefix sum --post 2851` — 1 post
- 2026-07-18: `attach knapsack --post 7579` — 1 post
- 2026-07-18: `attach sorting --post 13448` — 1 post
- 2026-07-18: `detach sliding window --post 17128` — 1 post
- 2026-07-18: `attach prefix sum --post 17128` — 1 post
- 2026-07-18: `attach implementation --post 17128` — 1 post
- 2026-07-20: `attach segment tree --post 11505` — 1 post
- 2026-07-20: `attach segment tree --post 1275` — 1 post
- 2026-07-20: `attach segment tree --post 12837` — 1 post
- 2026-07-20: `attach segment tree --post 14438` — 1 post
- 2026-07-20: `attach segment tree --post 18436` — 1 post
- 2026-07-20: `attach segment tree --post 2042` — 1 post
- 2026-07-20: `attach segment tree --post 2268` — 1 post
- 2026-07-20: `attach segment tree --post 5676` — 1 post
- 2026-07-20: `attach segment tree --post 10868` — 1 post
- 2026-07-20: `attach segment tree --post 2357` — 1 post
- 2026-07-20: `attach segment tree --post 1168` — 1 post
- 2026-07-20: `attach segment tree --post 12899` — 1 post
- 2026-07-20: `attach segment tree --post 2243` — 1 post
- 2026-07-20: `attach segment tree --post 14428` — 1 post
- 2026-07-20: `attach hash set／hash map --post 14425` — 1 post
- 2026-07-20: `attach knapsack --post 10982` — 1 post
- 2026-07-20: `attach knapsack --post 17528` — 1 post
- 2026-07-20: `attach sieve of eratosthenes --post 4948` — 1 post
- 2026-07-20: `attach number theory --post 4134` — 1 post
- 2026-07-20: `attach dp --post 1801` — 1 post
- 2026-07-20: `attach dp --post 19645` — 1 post
- 2026-07-20: `attach binary search --post 1300` — 1 post
- 2026-07-20: `attach parametric search --post 1300` — 1 post
- 2026-07-20: `attach stack --post 12789` — 1 post
- 2026-07-20: `attach number theory --post 1037` — 1 post
- 2026-07-20: `attach deque --post 24511` — 1 post
- 2026-07-20: `attach deque --post 2346` — 1 post
- 2026-07-20: `attach simulation --post 2346` — 1 post
- 2026-07-20: `attach implementation --post 2108` — 1 post
- 2026-07-20: `attach greedy --post 1931` — 1 post
- 2026-07-20: `attach sorting --post 1931` — 1 post
- 2026-07-20: `attach two pointers --post 30804` — 1 post
- 2026-07-20: `attach sliding window --post 30804` — 1 post
- 2026-07-20: `attach deque --post 18115` — 1 post
- 2026-07-20: `attach math --post 1059` — 1 post
- 2026-07-20: `attach sieve of eratosthenes --post 1016` — 1 post
- 2026-07-20: `attach palindrome --post 1213` — 1 post
- 2026-07-20: `attach parametric search --post 2022` — 1 post
- 2026-07-20: `attach pythagorean theorem --post 2022` — 1 post
- 2026-07-20: `attach dp --post 1230` — 1 post
- 2026-07-20: `attach greedy --post 18185` — 1 post
- 2026-07-20: `attach greedy --post 18186` — 1 post
- 2026-07-20: `attach ad hoc --post 10220` — 1 post
- 2026-07-20: `attach math --post 35307` — 1 post
- 2026-07-20: `attach trie --post 14725` — 1 post
- 2026-07-20: `attach tree set／tree map --post 14725` — 1 post
- 2026-07-20: `attach dfs --post 14725` — 1 post
- 2026-07-20: `attach trie --post 16906` — 1 post
- 2026-07-20: `attach backtracking --post 16906` — 1 post
- 2026-07-20: `attach trie --post 16934` — 1 post
- 2026-07-20: `attach trie --post 5670` — 1 post
- 2026-07-20: `attach trie --post 9202` — 1 post
- 2026-07-20: `attach backtracking --post 9202` — 1 post
- 2026-07-20: `attach trie --post 14426` — 1 post
- 2026-07-20: `attach hash set／hash map --post 14426` — 1 post
- 2026-07-20: `attach trie --post 5052` — 1 post
- 2026-07-20: `attach trie --post 13505` — 1 post
- 2026-07-20: `attach trie --post 7432` — 1 post
- 2026-07-20: `attach tree set／tree map --post 7432` — 1 post
- 2026-07-20: `attach dfs --post 7432` — 1 post
- 2026-07-20: `attach trie --post 5446` — 1 post
- 2026-07-20: `attach geometry --post 1485` — 1 post
- 2026-07-20: `attach trie --post 13504` — 1 post
- 2026-07-20: `attach prefix sum --post 13504` — 1 post
- 2026-07-20: `attach trie --post 16903` — 1 post
- 2026-07-20: `attach number theory --post 35295` — 1 post
- 2026-07-20: `attach binary search --post 12899` — 1 post
- 2026-07-20: `attach binary search --post 2243` — 1 post
- 2026-07-20: `attach knapsack --post 1801` — 1 post
- 2026-07-20: `attach knapsack --post 19645` — 1 post
- 2026-07-20: `detach simulation --post 2346` — 1 post
- 2026-07-20: `attach brute force --post 4134` — 1 post
- 2026-07-20: `attach brute force --post 1801` — 1 post
- 2026-07-20: `detach dfs --post 14725` — 1 post
- 2026-07-20: `detach dfs --post 7432` — 1 post
