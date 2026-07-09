import { useEffect, useState } from 'react';
import { Card, Table, Tag, Alert, Spin, Progress } from 'antd';
import { getWeakPoints } from '../services/api';

const levelColors = {
  '优秀': '#389e0d',
  '良好': '#52c41a',
  '一般': '#faad14',
  '薄弱': '#ff7a45',
  '危险': '#ff4d4f',
};

const columns = [
  {
    title: '知识点',
    dataIndex: 'name',
    key: 'name',
  },
  {
    title: '分类',
    dataIndex: 'category',
    key: 'category',
  },
  {
    title: '答题数',
    dataIndex: 'total_attempts',
    key: 'total_attempts',
    sorter: (a, b) => a.total_attempts - b.total_attempts,
  },
  {
    title: '正确率',
    dataIndex: 'accuracy',
    key: 'accuracy',
    sorter: (a, b) => a.accuracy - b.accuracy,
    render: (val) => (
      <Progress
        percent={Math.round(val * 100)}
        size="small"
        status={val >= 0.6 ? 'success' : 'exception'}
      />
    ),
  },
  {
    title: '掌握等级',
    dataIndex: 'level',
    key: 'level',
    render: (level) => (
      <Tag color={levelColors[level] || '#666'}>{level}</Tag>
    ),
  },
  {
    title: '平均耗时',
    dataIndex: 'avg_time_spent',
    key: 'avg_time_spent',
    render: (val) => `${val.toFixed(0)}s`,
  },
];

export default function WeakPoints() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getWeakPoints(1)
      .then((r) => setData(r.data))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <Spin size="large" style={{ display: 'block', marginTop: 100 }} />;

  const weakCount = data.filter((d) => d.level === '薄弱' || d.level === '危险').length;

  return (
    <Card title="📊 薄弱点分析" extra={<Tag color="error">{weakCount} 个薄弱点</Tag>}>
      {data.length === 0 ? (
        <Alert
          type="info"
          message="暂无数据"
          description="答题数据不足，继续刷题后将展示分析。"
          showIcon
        />
      ) : (
        <Table
          dataSource={data}
          columns={columns}
          rowKey="id"
          pagination={false}
          summary={() => (
            <Table.Summary.Row>
              <Table.Summary.Cell index={0} colSpan={6}>
                <Alert
                  type={weakCount > 0 ? 'warning' : 'success'}
                  message={weakCount > 0 ? `发现 ${weakCount} 个薄弱知识点，建议针对性训练` : '所有知识点掌握良好'}
                  showIcon
                />
              </Table.Summary.Cell>
            </Table.Summary.Row>
          )}
        />
      )}
    </Card>
  );
}
