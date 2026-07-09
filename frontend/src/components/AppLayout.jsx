import { Layout, Menu } from 'antd';
import {
  DashboardOutlined,
  EditOutlined,
  BookOutlined,
  BugOutlined,
  WarningOutlined,
} from '@ant-design/icons';
import { useNavigate, useLocation } from 'react-router-dom';

const { Header, Content } = Layout;

const menuItems = [
  { key: '/dashboard', icon: <DashboardOutlined />, label: '仪表盘' },
  { key: '/practice', icon: <EditOutlined />, label: '刷题练习' },
  { key: '/review', icon: <BookOutlined />, label: '复习计划' },
  { key: '/error-book', icon: <BugOutlined />, label: '错题本' },
  { key: '/weak-points', icon: <WarningOutlined />, label: '薄弱分析' },
];

export default function AppLayout({ children }) {
  const navigate = useNavigate();
  const location = useLocation();

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Header style={{
        display: 'flex',
        alignItems: 'center',
        borderBottom: '1px solid #1e293b',
        background: '#0f172a',
      }}>
        <div style={{
          color: '#8b5cf6',
          fontSize: 20,
          fontWeight: 'bold',
          marginRight: 40,
          whiteSpace: 'nowrap',
        }}>
          🎯 考研数学刷题
        </div>
        <Menu
          theme="dark"
          mode="horizontal"
          selectedKeys={[location.pathname]}
          items={menuItems}
          onClick={({ key }) => navigate(key)}
          style={{ flex: 1, minWidth: 0, background: 'transparent' }}
        />
      </Header>
      <Content style={{ padding: '24px', maxWidth: 1200, margin: '0 auto', width: '100%' }}>
        {children}
      </Content>
    </Layout>
  );
}
