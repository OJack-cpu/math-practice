import { useEffect, useState } from 'react';
import { Card, Button, Tag, Typography, Space, Alert, Spin, Progress, Divider } from 'antd';
import { getDueReviews } from '../services/api';
import MathText from '../components/MathText';

const { Text, Paragraph } = Typography;

const qualityLabels = ['完全忘记', '困难', '犹豫', '轻松', '完美'];
const qualityColors = ['#ff4d4f', '#ff7a45', '#faad14', '#52c41a', '#389e0d'];

export default function Review() {
  const [reviews, setReviews] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [showAnswer, setShowAnswer] = useState(false);
  const [loading, setLoading] = useState(true);
  const [completed, setCompleted] = useState(false);

  const current = reviews[currentIndex];

  useEffect(() => {
    getDueReviews(20)
      .then((r) => setReviews(r.data))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const handleQuality = (quality) => {
    if (currentIndex < reviews.length - 1) {
      setCurrentIndex(currentIndex + 1);
      setShowAnswer(false);
    } else {
      setCompleted(true);
    }
  };

  if (loading) return <Spin size="large" style={{ display: 'block', marginTop: 100 }} />;

  if (reviews.length === 0) {
    return (
      <Card>
        <Alert
          type="success"
          message="今日复习已完成！"
          description="今天没有需要复习的题目，去做些新题吧！"
          showIcon
        />
      </Card>
    );
  }

  if (completed) {
    return (
      <Card>
        <Alert
          type="success"
          message="🎉 复习完成！"
          description={`今日 ${reviews.length} 道复习题全部完成，继续保持！`}
          showIcon
        />
      </Card>
    );
  }

  return (
    <div>
      <Card style={{ marginBottom: 16 }}>
        <Space>
          <Text strong>📅 今日复习计划</Text>
          <Tag color="purple">剩余 {reviews.length - currentIndex} 题</Tag>
          <Tag>共 {reviews.length} 题</Tag>
        </Space>
        <Progress
          percent={Math.round((currentIndex / reviews.length) * 100)}
          showInfo={false}
          style={{ marginTop: 8 }}
        />
      </Card>

      <Card>
        <div style={{ fontSize: 17, lineHeight: 2.4, padding: '20px 24px',
          backgroundColor: 'rgba(139,92,246,0.06)', borderRadius: 12, marginBottom: 16 }}>
          <MathText text={current?.content} />
        </div>

        {current?.knowledge_point && (
          <Tag color="blue" style={{ marginBottom: 16 }}>
            {current.knowledge_point.name}
          </Tag>
        )}

        {!showAnswer ? (
          <Button
            type="primary"
            size="large"
            onClick={() => setShowAnswer(true)}
            block
            style={{ marginTop: 16 }}
          >
            查看答案
          </Button>
        ) : (
          <>
            <Divider />
            <Text strong style={{ fontSize: 16 }}>正确答案：</Text>
            <Text style={{ fontSize: 16 }}>{current?.review_schedule?.question_id ? '（答案已隐藏，参见原始题目）' : ''}</Text>

            <Divider />
            <Text strong>自评回忆质量：</Text>
            <div style={{ marginTop: 8 }}>
              <Space wrap>
                {qualityLabels.map((label, i) => (
                  <Button
                    key={i}
                    size="large"
                    style={{
                      borderColor: qualityColors[i],
                      color: qualityColors[i],
                    }}
                    onClick={() => handleQuality(i + 1)}
                  >
                    {label}
                  </Button>
                ))}
              </Space>
            </div>
          </>
        )}
      </Card>
    </div>
  );
}
