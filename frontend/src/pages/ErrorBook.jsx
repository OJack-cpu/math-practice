import { useEffect, useState } from 'react';
import { Card, List, Tag, Typography, Alert, Spin, Empty } from 'antd';
import { getErrorBook } from '../services/api';
import MathText from '../components/MathText';

const { Text } = Typography;

export default function ErrorBook() {
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getErrorBook(50)
      .then((r) => setQuestions(r.data))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <Spin size="large" style={{ display: 'block', marginTop: 100 }} />;

  return (
    <Card
      title={<span style={{ fontSize: 18 }}>📖 错题本</span>}
      extra={<Tag color="error" style={{ fontSize: 14 }}>{questions.length} 题</Tag>}
    >
      {questions.length === 0 ? (
        <Empty
          description={
            <Alert type="success" message="没有错题！" description="你还没答错过题目，去刷题吧" showIcon />
          }
        />
      ) : (
        <List
          dataSource={questions}
          renderItem={(q, i) => (
            <List.Item style={{ padding: '16px 0' }}>
              <div style={{ width: '100%' }}>
                <Text strong style={{ fontSize: 14, color: '#8b5cf6' }}>#{i + 1}</Text>
                <div style={{
                  marginTop: 10, padding: '14px 18px',
                  backgroundColor: 'rgba(255,77,79,0.05)', borderRadius: 10,
                  fontSize: 15, lineHeight: 2.2,
                }}>
                  <MathText text={q.content} />
                </div>
                <div style={{ marginTop: 10 }}>
                  <Tag color="purple">{q.knowledge_point?.category}</Tag>
                  <Tag color="blue">{q.knowledge_point?.name}</Tag>
                  <Tag color="red">待复习</Tag>
                </div>
              </div>
            </List.Item>
          )}
        />
      )}
    </Card>
  );
}
