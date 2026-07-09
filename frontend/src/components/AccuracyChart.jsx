import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function AccuracyChart({ data }) {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
        <XAxis dataKey="date" stroke="#94a3b8" fontSize={12} />
        <YAxis domain={[0, 1]} tickFormatter={(v) => `${(v * 100).toFixed(0)}%`} stroke="#94a3b8" />
        <Tooltip
          formatter={(value) => `${(value * 100).toFixed(1)}%`}
          contentStyle={{ background: '#1e293b', border: '1px solid #334155' }}
        />
        <Line
          type="monotone"
          dataKey="accuracy"
          stroke="#8b5cf6"
          strokeWidth={2}
          dot={{ r: 4, fill: '#8b5cf6' }}
          activeDot={{ r: 6 }}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}
