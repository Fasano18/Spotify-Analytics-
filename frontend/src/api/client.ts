import axios from 'axios'
import type { TopTracksResponse, TopArtistsResponse, HistoryResponse, TimeRange, User } from '../types'

// Se VITE_API_URL não estiver definida, usa caminhos relativos (proxy do Vite)
// Se estiver definida, usa a URL completa
const API_BASE_URL = import.meta.env.VITE_API_URL || ''

const client = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const api = {
  async getTopTracks(timeRange: TimeRange = 'medium_term', limit: number = 20): Promise<TopTracksResponse> {
    const response = await client.get('/top/tracks', {
      params: { time_range: timeRange, limit },
    })
    return response.data
  },

  async getTopArtists(timeRange: TimeRange = 'medium_term', limit: number = 20): Promise<TopArtistsResponse> {
    const response = await client.get('/top/artists', {
      params: { time_range: timeRange, limit },
    })
    return response.data
  },

  async getHistory(limit: number = 50): Promise<HistoryResponse> {
    const response = await client.get('/history', {
      params: { limit },
    })
    return response.data
  },

  async checkAuth(): Promise<boolean> {
    try {
      await client.get('/top/tracks', { params: { limit: 1 } })
      return true
    } catch {
      return false
    }
  },

  async getUserInfo(): Promise<User> {
    const response = await client.get('/me')
    return response.data
  },
}

export default client
