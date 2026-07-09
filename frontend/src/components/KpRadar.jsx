import {
  RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis,
  Radar, ResponsiveContainer, Tooltip,
} from 'recharts';

export default function KpRadar({ data }) {
  const chartData = data.map((d) => ({
    name: d.name.length > 6 ? d.name.slice(0, 6) + '..' : d.name,
    value: Math.round(d.accuracy * 100),
    fullName: d.name,
  }));

  if (chartData.length === 0) {
    return <div style={{ color: '#94a3b8', textAlign: 'center', paddingTop: 100 }}>暂无数据</div>;
  }

  return (
    <ResponsiveContainer width="100%" height={300}>
      <RadarChart data={chartData}>
        <PolarGrid stroke="#1e293b" />
        <PolarAngleAxis dataKey="name" stroke="#94a3b8" fontSize={12} />
        <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} />
        <Tooltip
          formatter={(value, name, props) => [`${value}%`, props.payload.fullName]}
          contentStyle={{ background: '#1e293b', border: '1px solid #334155' }}
        />
        <Radar
          name="正确率"
          dataKey="value"
          stroke="#8b5cf6"
          fill="#8b5cf6"
          fillOpacity={0.3}
        />
      </RadarChart>
    </ResponsiveContainer>
  );
}
