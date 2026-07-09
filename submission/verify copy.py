import urllib.request, json

def get(path):
    r = urllib.request.urlopen('http://localhost:8000'+path)
    return json.loads(r.read())

print("="*50)
print("  考研数学刷题系统 - API 功能验证")
print("="*50)

kps = get('/api/knowledge-points')
print(f'\n1. 知识点列表: {len(kps)} 个')
for kp in kps[:3]:
    print(f'   [{kp["category"]}] {kp["name"]}')

qs = get('/api/questions?limit=50')
print(f'\n2. 题目列表: 返回 {len(qs)} 题')
print(f'   示例: {qs[0]["content"][:40]}...')

data = json.dumps({'question_id':1,'user_answer':'3','time_spent':20}).encode()
req = urllib.request.Request('http://localhost:8000/api/answer', data=data,
    headers={'Content-Type':'application/json'})
r = json.loads(urllib.request.urlopen(req).read())
print(f'\n3. 答题提交: {"正确!" if r["is_correct"] else "错误"}, 间隔{r["review_info"]["interval"]}天')

d = get('/api/dashboard')
print(f'\n4. 仪表盘: {d["total_questions"]}题, 正确率{d["overall_accuracy"]}')

eb = get('/api/error-book')
print(f'5. 错题本: {len(eb)} 题')

rv = get('/api/review/due')
print(f'6. 待复习: {len(rv)} 题')

wp = get('/api/analysis/weak-points?min_attempts=0')
print(f'7. 薄弱点: 分析 {len(wp)} 个知识点')

tr = get('/api/stats/correct-rate-trend?days=7')
print(f'8. 趋势: {len(tr)} 天')

print("\n" + "="*50)
print("  全部 API 验证通过!")
print("="*50)
