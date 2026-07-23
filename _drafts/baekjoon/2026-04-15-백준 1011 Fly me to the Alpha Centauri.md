---
title: "[BaekJoon] 1011번 - Fly me to the Alpha Centauri [Java]"
slug: baekjoon-1011
date: 2026-04-15
categories: [PS, BaekJoon]
tags: [Unlinked]
toc: true
math: true
---

[문제 링크](https://www.acmicpc.net/problem/1011)

---

## 1. 아이디어



---

## 2. 코드

### 1. 풀이 [Java]

```java
import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringBuilder sb = new StringBuilder();
        StringTokenizer st;

        int t = Integer.parseInt(br.readLine());
        while (t-- > 0) {
            st = new StringTokenizer(br.readLine());
            int x = Integer.parseInt(st.nextToken());
            int y = Integer.parseInt(st.nextToken());

            int diff = y - x;
            int num = 1;
            int cnt = 0;
            while (diff > 2 * num) {
                diff -= 2 * num;
                num++;
                cnt += 2;
            }
            if (diff > num) {
                cnt += 2;
            } else if (diff > 0) {
                cnt++;
            }

            sb.append(cnt).append("\n");
        }

        System.out.println(sb);
    }
}
```

---

## 3. 리뷰

없음.

---
