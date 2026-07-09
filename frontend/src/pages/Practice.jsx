import { useEffect, useState } from 'react';
import {
  Card, Button, Radio, Input, Tag, Typography, Space,
  Select, Alert, Spin, Progress, Divider,
} from 'antd';
import { getQuestions, getKnowledgePoints, submitAnswer } from '../services/api';
import MathText from '../components/MathText';

const { Title, Text, Paragraph } = Typography;
const { TextArea } = Input;

export default function Practice() {
  const [kps, setKps] = useState([]);
  const [questions, setQuestions] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [userAnswer, setUserAnswer] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [mode, setMode] = useState('sequence');
  const [selectedKp, setSelectedKp] = useState(undefined);
  const [flipping, setFlipping] = useState(false);
  const [correctCount, setCorrectCount] = useState(0);

  const current = questions[currentIndex];

  useEffect(() => {
    getKnowledgePoints().then((r) => setKps(r.data));
    loadQuestions();
  }, []);

  const loadQuestions = async (kp) => {
    setLoading(true);
    try {
      const params = { limit: 50 };
      if (kp) params.knowledge_point_id = kp;
      const r = await getQuestions(params);
      setQuestions(r.data);
      setCurrentIndex(0);
      setResult(null);
      setUserAnswer('');
      setCorrectCount(0);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async () => {
    if (!current || !userAnswer.trim()) return;
    setFlipping(true);
    try {
      const r = await submitAnswer({
        question_id: current.id,
        user_answer: userAnswer.trim(),
        time_spent: 30,
      });
      setTimeout(() => {
        setResult(r.data);
        setFlipping(false);
        if (r.data.is_correct) setCorrectCount((c) => c + 1);
      }, 400);
    } catch (e) {
      setError(e.message);
      setFlipping(false);
    }
  };

  const handleNext = () => {
    if (currentIndex < questions.length - 1) {
      setCurrentIndex(currentIndex + 1);
      setResult(null);
      setUserAnswer('');
    }
  };

  const handleKpChange = (value) => {
    setSelectedKp(value);
    loadQuestions(value);
  };

  if (loading) return <Spin size="large" style={{ display: 'block', marginTop: 100 }} />;
  if (error) return <Alert type="error" message={error} />;

  return (
    <div>
      <Card style={{ marginBottom: 16 }}>
        <Space wrap>
          <Select
            placeholder="筛选知识点"
            allowClear
            style={{ width: 220 }}
            value={selectedKp}
            onChange={handleKpChange}
            options={kps.map((kp) => ({ label: `[${kp.category}] ${kp.name}`, value: kp.id }))}
          />
          <Text type="secondary">
            共 {questions.length} 题 · 当前第 {currentIndex + 1} 题
            {correctCount > 0 && <span style={{ color: '#52c41a', marginLeft: 8 }}>✓ {correctCount}</span>}
          </Text>
        </Space>
      </Card>

      {current && (
        <Card className={flipping ? 'card-flip' : ''}>
          <Progress
            percent={Math.round(((currentIndex + 1) / questions.length) * 100)}
            strokeColor={{ from: '#8b5cf6', to: '#52c41a' }}
            showInfo={false}
            style={{ marginBottom: 20 }}
          />

          <div style={{ marginBottom: 16 }}>
            <Space wrap>
              <Tag color="purple">{current.knowledge_point?.category || ''}</Tag>
              <Tag color="blue">{current.knowledge_point?.name || '未分类'}</Tag>
              <Tag color={current.difficulty <= 2 ? 'green' : current.difficulty <= 4 ? 'orange' : 'red'}>
                难度 {'★'.repeat(current.difficulty)}{'☆'.repeat(5 - current.difficulty)}
              </Tag>
              <Tag>{current.question_type === 'fill_blank' ? '填空题' : '选择题'}</Tag>
            </Space>
          </div>

          {/* 题目内容 - 使用 MathText 渲染 LaTeX */}
          <div style={{
            fontSize: 17, lineHeight: 2.4, padding: '20px 24px',
            backgroundColor: 'rgba(139,92,246,0.06)', borderRadius: 12,
            marginBottom: 20, minHeight: 60,
          }}>
            <MathText text={current.content} />
          </div>

          {current.options && (
            <Radio.Group
              value={userAnswer}
              onChange={(e) => setUserAnswer(e.target.value)}
              disabled={!!result}
              style={{ display: 'flex', flexDirection: 'column', gap: 12, marginBottom: 20 }}
            >
              {current.options.map((opt) => (
                <Radio key={opt} value={opt.charAt(0)} style={{
                  lineHeight: '36px', padding: '8px 16px',
                  borderRadius: 8, border: '1px solid rgba(255,255,255,0.1)',
                  width: '100%', transition: 'all 0.2s',
                }}>
                  <MathText text={opt} />
                </Radio>
              ))}
            </Radio.Group>
          )}

          {!current.options && (
            <TextArea
              value={userAnswer}
              onChange={(e) => setUserAnswer(e.target.value)}
              disabled={!!result}
              placeholder="输入你的答案..."
              rows={3}
              style={{ marginBottom: 20, fontSize: 15 }}
            />
          )}

          <Space>
            <Button
              type="primary"
              size="large"
              onClick={handleSubmit}
              disabled={!userAnswer.trim() || !!result}
              loading={flipping}
            >
              {result ? '已提交' : '提交答案'}
            </Button>
            {result && (
              <Button size="large" onClick={handleNext} disabled={currentIndex >= questions.length - 1}>
                下一题 →
              </Button>
            )}
          </Space>

          {result && (
            <div className="answer-reveal" style={{ marginTop: 20, animation: 'slideIn 0.4s ease' }}>
              <Divider />
              <Alert
                type={result.is_correct ? 'success' : 'error'}
                message={
                  <span style={{ fontSize: 16 }}>
                    {result.is_correct ? '✓ 回答正确！' : '✗ 回答错误'}
                  </span>
                }
                description={
                  <div style={{ fontSize: 15 }}>
                    <div style={{ marginBottom: 8 }}>
                      <Text strong>正确答案：</Text>
                      <MathText text={result.correct_answer} />
                    </div>
                    {result.explanation && (
                      <div style={{ marginTop: 8 }}>
                        <Text strong>📝 解析：</Text>
                        <MathText text={result.explanation} />
                      </div>
                    )}
                  </div>
                }
              />
              <div style={{ marginTop: 12 }}>
                <Space wrap>
                  <Tag color="purple">📅 {result.review_info.interval} 天后复习</Tag>
                  <Tag color="geekblue">已复习 {result.review_info.repetitions} 次</Tag>
                  <Tag color="cyan">EF: {result.review_info.easiness_factor}</Tag>
                </Space>
              </div>
            </div>
          )}
        </Card>
      )}

      {!current && questions.length === 0 && (
        <Card>
          <Alert type="info" message="暂无题目" description="当前筛选条件下没有题目，请调整筛选条件。" />
        </Card>
      )}
    </div>
  );
}
