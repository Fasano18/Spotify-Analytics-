import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts'
import type { Track } from '../types'

interface TracksChartProps {
  data: Track[]
}

export default function TracksChart({ data }: TracksChartProps) {
  if (!data || data.length === 0) {
    return (
      <div className="flex items-center justify-center h-[300px] text-white/50">
        Nenhum dado disponível
      </div>
    )
  }

  // Pega top 10 e ordena por popularidade (menor para maior para visualização)
  const top10 = [...data]
    .sort((a, b) => b.popularidade - a.popularidade)
    .slice(0, 10)
    .reverse() // Inverte para mostrar do menor para o maior visualmente
  
  const chartData = top10.map((track, index) => ({
    nome: track.nome.length > 30 ? track.nome.substring(0, 30) + '...' : track.nome,
    popularidade: Number(track.popularidade) || 0,
    fullName: track.nome,
    index: index,
  }))

  const colors = [
    '#1DB954', '#1ed760', '#1DB954', '#1ed760', 
    '#1DB954', '#1ed760', '#1DB954', '#1ed760', 
    '#1DB954', '#1ed760'
  ]

  return (
    <ResponsiveContainer width="100%" height={400}>
      <BarChart 
        data={chartData} 
        layout="vertical" 
        margin={{ top: 10, right: 40, left: 20, bottom: 10 }}
        barCategoryGap="20%"
      >
        <CartesianGrid strokeDasharray="3 3" stroke="#ffffff20" />
        <XAxis 
          type="number" 
          domain={[0, 100]} 
          stroke="#ffffff80"
          tick={{ fill: '#ffffff80', fontSize: 12 }}
        />
        <YAxis 
          dataKey="nome" 
          type="category" 
          width={200} 
          stroke="#ffffff80" 
          tick={{ fill: '#ffffff', fontSize: 12 }}
        />
        <Tooltip
          contentStyle={{
            backgroundColor: 'rgba(255, 255, 255, 0.95)',
            border: '1px solid rgba(29, 185, 84, 0.3)',
            borderRadius: '8px',
            color: '#1a1a1a',
            padding: '10px 14px',
            boxShadow: '0 4px 12px rgba(0, 0, 0, 0.3)',
            fontWeight: '500',
          }}
          itemStyle={{
            color: '#1a1a1a',
            padding: '2px 0',
          }}
          labelStyle={{
            color: '#1a1a1a',
            fontWeight: '600',
            marginBottom: '4px',
          }}
          formatter={(value: number) => [`${value}%`, 'Popularidade']}
          labelFormatter={(label) => {
            const item = chartData.find(d => d.nome === label)
            return item ? item.fullName : label
          }}
        />
        <Bar 
          dataKey="popularidade" 
          radius={[0, 8, 8, 0]} 
          fill="#1DB954"
          isAnimationActive={true}
          barSize={35}
        >
          {chartData.map((entry, index) => (
            <Cell 
              key={`cell-${entry.index}`} 
              fill={colors[index % colors.length]} 
            />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  )
}
