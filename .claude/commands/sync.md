포스트의 코드 블록을 Algorithm 디렉토리의 최신 코드와 비교하고, 사용자 확인 후 갱신한다.

## 절차

1. diff 확인 스크립트를 실행한다:

```
python3 tools/sync.py $ARGUMENTS
```

- 인자 없으면 `_drafts/` 전체 대상
- 인자 있으면 해당 문제 번호만 대상 (`_drafts/` 우선, 없으면 `_posts/`)

2. 차이가 있는 파일의 diff를 사용자에게 보여준다.

3. 사용자가 적용을 승인하면 `--apply` 플래그를 추가하여 다시 실행한다:

```
python3 tools/sync.py $ARGUMENTS --apply
```
