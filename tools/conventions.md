# PS 코드 관례 레퍼런스

이 파일은 블로그 포스팅의 코드 일관성 검수에 사용된다.
포스팅이 쌓이면서 패턴이 확인되면 아래에 추가한다.

> 마지막 스캔: 2026-03-26 / 30개 포스트 대상

---

## 변수명/상수명

- 입력 변수: 한 글자 (`a`, `b`, `n`, `m`, `k`, `x`, `y` 등) (28/30)
- 카운트 배열: `cnt` (후보, 2회)
- DP 배열: `dp` (후보, 1회)
- 결과 추적: `max`, `mx` (후보, 2회)

---

## 함수명

(아직 3회 이상 반복된 관례 없음)

<!-- 후보:
- Math.max (Java) / max() (C++): 2회
-->

---

## 알고리즘 구현 패턴

**Java I/O**
- 복수 값 입력: `BufferedReader` + `StringTokenizer` (15/30)
- 단일 값 입력: `BufferedReader` + `Integer.parseInt(br.readLine())` (8/30)
- `Scanner` 사용: 0회 (사용하지 않음)
- 출력: `System.out.println()` (대부분)
- 다중 출력: `BufferedWriter` (후보, 2회)

**C++ I/O**
- 빠른 I/O: `ios::sync_with_stdio(0);` + `cin.tie(0);` (26/30)
- 줄바꿈: `'\n'` (대부분)

**1-based 인덱싱**
- 배열 크기 `1 + n` 으로 선언하여 1-based 사용 (3회 이상)

---

## 코드 스타일

**Java**
- `main` 메서드에 `throws IOException` 선언 (I/O 사용 시 전부)
- import: `java.io.*`, `java.util.*` (필요 시)
- 변수 스코프: 전부 `main` 메서드 로컬 (26/30)

**C++**
- 헤더: `#include <bits/stdc++.h>` (29/30)
- 네임스페이스: `using namespace std;` (29/30)
- 큰 배열/DP 테이블: 전역 선언 (4/30)
- 작은 변수: `main` 함수 로컬 (26/30)
