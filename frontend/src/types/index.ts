export type TimeRange = 'short_term' | 'medium_term' | 'long_term'

export interface Track {
  id: string
  nome: string
  artistas: string[]
  album: string
  popularidade: number
  duracao_ms: number
  duracao_minutos: number
  preview_url: string | null
  url_externa: string | null
  imagem_capa: string | null
}

export interface Artist {
  id: string
  nome: string
  generos: string[]
  popularidade: number
  seguidores: number
  url_externa: string | null
  imagem_perfil: string | null
}

export interface RecentlyPlayedItem extends Track {
  reproduzida_em: string
}

export interface Pagination {
  limite: number
  offset: number
  total: number | null
}

export interface TopTracksResponse {
  itens: Track[]
  paginacao: Pagination
}

export interface TopArtistsResponse {
  itens: Artist[]
  paginacao: Pagination
}

export interface HistoryResponse {
  itens: RecentlyPlayedItem[]
  paginacao: Pagination
}

export interface User {
  id: string
  nome: string
  email: string | null
  imagem_perfil: string | null
  pais: string | null
  seguidores: number | null
}
