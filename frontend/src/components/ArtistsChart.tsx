import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts'
import type { Artist } from '../types'

interface ArtistsChartProps {
  data: Artist[]
}

const COLORS = [
  '#1DB954',
  '#1ed760',
  '#667eea',
  '#764ba2',
  '#f093fb',
  '#4facfe',
  '#00f2fe',
  '#43e97b',
  '#fa709a',
  '#fee140',
]

export default function ArtistsChart({ data }: ArtistsChartProps) {
  if (!data || data.length === 0) {
    return (
      <div className="flex items-center justify-center h-[300px] text-white/50">
        Nenhum dado disponível
      </div>
    )
  }

  // Pega top 10 artistas
  const top10 = data.slice(0, 10)
  
  const chartData = top10.map((artist) => ({
    nome: artist.nome,
    popularidade: Number(artist.popularidade) || 0,
    seguidores: Number(artist.seguidores) || 0,
  }))

  if (chartData.length === 0) {
    return (
      <div className="flex items-center justify-center h-[300px] text-white/50">
        Nenhum dado disponível
      </div>
    )
  }

  // Se todas as popularidades forem 0, não renderiza (mas isso não deve acontecer agora)
  const hasData = chartData.some(d => d.popularidade > 0)
  if (!hasData) {
    return (
      <div className="flex items-center justify-center h-[300px] text-white/50">
        Carregando dados de popularidade...
      </div>
    )
  }

  return (
    <ResponsiveContainer width="100%" height={300}>
      <PieChart>
        <Pie
          data={chartData}
          cx="50%"
          cy="50%"
          labelLine={false}
          label={({ percent }) => {
            if (percent < 0.05) return '' // Não mostra label se muito pequeno
            return `${(percent * 100).toFixed(0)}%`
          }}
          outerRadius={100}
          innerRadius={40}
          fill="#8884d8"
          dataKey="popularidade"
          paddingAngle={2}
          isAnimationActive={true}
        >
          {chartData.map((entry, index) => (
            <Cell key={`cell-${index}-${entry.nome}`} fill={COLORS[index % COLORS.length]} />
          ))}
        </Pie>
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
            const artist = chartData.find(d => d.nome === label)
            if (artist) {
              return `${artist.nome}${artist.seguidores > 0 ? ` (${artist.seguidores.toLocaleString('pt-BR')} seguidores)` : ''}`
            }
            return label
          }}
        />
        <Legend
          formatter={(value) => <span style={{ color: '#fff', fontSize: '12px' }}>{value}</span>}
          wrapperStyle={{ color: '#fff', fontSize: '12px' }}
          iconType="circle"
        />
      </PieChart>
    </ResponsiveContainer>
  )
}
