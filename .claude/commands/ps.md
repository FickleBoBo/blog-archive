포스트 생성 스크립트를 실행하고 결과를 보고한다.

```
python3 tools/generate_posts.py $ARGUMENTS
```

SWEA 문제 중 제목이 "TODO"인 것이 있으면 MCP puppeteer로 처리한다:

1. `https://swexpertacademy.com/main/code/problem/problemList.do` 로 이동 (브라우저 detached 시 `launchOptions: {headless: false}`)
2. 검색 입력란을 비우고 문제 번호를 입력 후 검색 클릭
3. 2초 대기 후 추출:
   - 제목: 검색 결과 텍스트에서 추출 (예: "3234. 준환이의 양팔저울" → "준환이의 양팔저울")
   - contestProbId: onclick 속성에서 추출 `fn_move_page('AWAe7XSKfUUDFAUw')` → `AWAe7XSKfUUDFAUw`
4. 문제 링크 생성: `https://swexpertacademy.com/main/code/problem/problemDetail.do?contestProbId={id}`
5. 생성된 마크다운 파일 갱신:
   - title의 `TODO`를 실제 제목으로 교체
   - 문제 링크의 `TODO`를 실제 URL로 교체
   - 파일명의 `TODO`를 실제 제목으로 변경 (파일 이름 변경)
