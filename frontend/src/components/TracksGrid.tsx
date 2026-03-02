import { ExternalLink } from 'lucide-react'
import type { Track } from '../types'

interface TracksGridProps {
  tracks: Track[]
}

export default function TracksGrid({ tracks }: TracksGridProps) {
  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
      {tracks.map((track) => (
        <a
          key={track.id}
          href={track.url_externa || '#'}
          target="_blank"
          rel="noopener noreferrer"
          className="group relative bg-white/5 rounded-xl overflow-hidden hover:bg-white/10 transition-all duration-200 hover:scale-105 cursor-pointer"
        >
          <div className="aspect-square relative">
            <img
              src={track.imagem_capa || 'https://via.placeholder.com/300'}
              alt={track.nome}
              className="w-full h-full object-cover"
            />
            <div className="absolute inset-0 bg-black/0 group-hover:bg-black/40 transition-all duration-200 flex items-center justify-center">
              <ExternalLink className="text-white opacity-0 group-hover:opacity-100 transition-opacity" size={32} />
            </div>
          </div>
          <div className="p-3">
            <h3 className="text-white font-semibold text-sm mb-1 line-clamp-2">{track.nome}</h3>
            <p className="text-white/60 text-xs line-clamp-1">{track.artistas.join(', ')}</p>
            <div className="flex items-center gap-2 mt-2">
              <span className="text-xs text-white/50">{track.duracao_minutos.toFixed(2)} min</span>
              <span className="text-xs text-spotify-green">●</span>
              <span className="text-xs text-white/50">{track.popularidade}%</span>
            </div>
          </div>
        </a>
      ))}
    </div>
  )
}
