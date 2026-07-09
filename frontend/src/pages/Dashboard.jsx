import { useEffect, useState } from 'react';
import { Row, Col, Card, Statistic, Spin, Alert } from 'antd';
import {
  BookOutlined, CheckCircleOutlined,
  PieChartOutlined, ClockCircleOutlined,
} from '@ant-design/icons';
import { getDashboard, getCorrectRateTrend } from '../services/api';
import AccuracyChart from '../components/AccuracyChart';
import KpRadar from '../components/KpRadar';

export default function Dashboard() {
  const [data, setData] = useState(null);
  const [trend, setTrend] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    Promise.all([getDashboard(), getCorrectRateTrend(14)])
      .then(([dash, trendRes]) => {
        setData(dash.data);
        setTrend(trendRes.data);
      })
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <Spin size="large" style={{ display: 'block', marginTop: 100 }} />;
  if (error) return <Alert type="error" message="加载失败" description={error} />;
  if (!data) return null;

  return (
    <div>
      <Row gutter={[16, 16]}>
        <Col xs={12} sm={6}>
          <Card><Statistic title="题库总数" value={data.total_questions} prefix={<BookOutlined />} /></Card>
        </Col>
        <Col xs={12} sm={6}>
          <Card><Statistic title="总答题数" value={data.total_answers} prefix={<PieChartOutlined />} /></Card>
        </Col>
        <Col xs={12} sm={6}>
          <Card>
            <Statistic
              title="总正确率"
              value={(data.overall_accuracy * 100).toFixed(0)}
              suffix="%"
              prefix={<CheckCircleOutlined />}
              valueStyle={{ color: data.overall_accuracy >= 0.6 ? '#52c41a' : '#ff4d4f' }}
            />
          </Card>
        </Col>
        <Col xs={12} sm={6}>
          <Card><Statistic title="待复习" value={data.review_due_count} prefix={<ClockCircleOutlined />} /></Card>
        </Col>
      </Row>

      <Row gutter={[16, 16]} style={{ marginTop: 16 }}>
        <Col xs={24} lg={14}>
          <Card title="正确率趋势 (近14天)">
            <AccuracyChart data={trend} />
          </Card>
        </Col>
        <Col xs={24} lg={10}>
          <Card title="知识点掌握度">
            <KpRadar data={data.knowledge_stats} />
          </Card>
        </Col>
      </Row>

      <Row gutter={[16, 16]} style={{ marginTop: 16 }}>
        <Col span={24}>
          <Card title="今日概览">
            <Row gutter={16}>
              <Col span={8}><Statistic title="今日做题" value={data.today_questions} suffix="题" /></Col>
              <Col span={8}>
                <Statistic
                  title="今日正确率"
                  value={(data.today_accuracy * 100).toFixed(0)}
                  suffix="%"
                  valueStyle={{ color: data.today_accuracy >= 0.6 ? '#52c41a' : '#ff4d4f' }}
                />
              </Col>
              <Col span={8}><Statistic title="待复习" value={data.review_due_count} suffix="题" /></Col>
            </Row>
          </Card>
        </Col>
      </Row>
    </div>
  );
}
