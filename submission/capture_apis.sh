#!/bin/bash
echo "========== 1. 仪表盘 API =========="
curl -s http://localhost:8000/api/dashboard | python3 -m json.tool 2>/dev/null | head -25

echo ""
echo "========== 2. 知识点列表 =========="
curl -s http://localhost:8000/api/knowledge-points | python3 -c "
import json,sys
d=json.load(sys.stdin)
print(f'共 {len(d)} 个知识点')
for kp in d[:5]:
    print(f'  [{kp[\"category\"]}] {kp[\"name\"]}')
"

echo ""
echo "========== 3. 题目查询 =========="
curl -s "http://localhost:8000/api/questions?limit=3" | python3 -c "
import json,sys
for q in json.load(sys.stdin):
    print(f'  题{q[\"id\"]}: {q[\"content\"][:50]}...')
"

echo ""
echo "========== 4. 答题测试 =========="
curl -s -X POST http://localhost:8000/api/answer \
  -H 'Content-Type: application/json' \
  -d '{"question_id":1,"user_answer":"3","time_spent":20}' | python3 -c "
import json,sys
r=json.load(sys.stdin)
print(f'  判题: {\"正确\" if r[\"is_correct\"] else \"错误\"}')
print(f'  复习间隔: {r[\"review_info\"][\"interval\"]} 天')
"

echo ""
echo "========== 5. 错题本 =========="
curl -s http://localhost:8000/api/error-book | python3 -c "
import json,sys
d=json.load(sys.stdin)
print(f'错题数: {len(d)}')
"

echo ""
echo "========== 6. 复习调度 =========="
curl -s http://localhost:8000/api/review/due | python3 -c "
import json,sys
d=json.load(sys.stdin)
print(f'待复习: {len(d)} 题')
"

echo ""
echo "========== 7. 正确率趋势 =========="
curl -s http://localhost:8000/api/stats/correct-rate-trend?days=7 | python3 -c "
import json,sys
d=json.load(sys.stdin)
print(f'趋势数据: {len(d)} 天')
for item in d:
    print(f'  {item[\"date\"]}: 正确率{item[\"accuracy\"]}, 答题{item[\"total\"]}题')
"