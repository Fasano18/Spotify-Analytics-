import { Music, Users, TrendingUp, Clock } from 'lucide-react'
import type { TopTracksResponse, TopArtistsResponse } from '../types'

interface StatsCardsProps {
  tracksData: TopTracksResponse
  artistsData: TopArtistsResponse
}

export default function StatsCards({ tracksData, artistsData }: StatsCardsProps) {
  const totalTracks = tracksData.paginacao?.total || tracksData.itens.length
  const totalArtists = artistsData.paginacao?.total || artistsData.itens.length
  const avgPopularity = Math.round(
    tracksData.itens.reduce((sum, t) => sum + t.popularidade, 0) / tracksData.itens.length
  )
  const totalDuration = tracksData.itens.reduce((sum, t) => sum + t.duracao_ms, 0)
  const totalHours = Math.round((totalDuration / 1000 / 60 / 60) * 10) / 10

  const stats = [
    {
      label: 'Total de Músicas',
      value: totalTracks.toLocaleString('pt-BR'),
      icon: Music,
      color: 'text-spotify-green',
    },
    {
      label: 'Total de Artistas',
      value: totalArtists.toLocaleString('pt-BR'),
      icon: Users,
      color: 'text-purple-400',
    },
    {
      label: 'Popularidade Média',
      value: `${avgPopularity}%`,
      icon: TrendingUp,
      color: 'text-blue-400',
    },
    {
      label: 'Tempo Total (Top 20)',
      value: `${totalHours}h`,
      icon: Clock,
      color: 'text-pink-400',
    },
  ]

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
      {stats.map((stat) => {
        const Icon = stat.icon
        return (
          <div key={stat.label} className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-white/70 text-sm mb-1">{stat.label}</p>
                <p className="text-3xl font-bold text-white">{stat.value}</p>
              </div>
              <div className={`${stat.color} bg-white/10 p-3 rounded-full`}>
                <Icon size={24} />
              </div>
            </div>
          </div>
        )
      })}
    </div>
  )
}
