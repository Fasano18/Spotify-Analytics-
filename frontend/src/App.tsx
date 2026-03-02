import { useState, useEffect } from 'react'
import { Music, TrendingUp, Clock, LogOut, RefreshCw } from 'lucide-react'
import { api } from './api/client'
import type { TimeRange, TopTracksResponse, TopArtistsResponse, User } from './types'
import TracksChart from './components/TracksChart'
import ArtistsChart from './components/ArtistsChart'
import StatsCards from './components/StatsCards'
import TracksGrid from './components/TracksGrid'
import AuthSection from './components/AuthSection'
import WelcomePanel from './components/WelcomePanel'
import LoadingSpinner from './components/LoadingSpinner'

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null)
  const [user, setUser] = useState<User | null>(null)
  const [showAnalytics, setShowAnalytics] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [isLoadingUser, setIsLoadingUser] = useState(false)
  const [timeRange, setTimeRange] = useState<TimeRange>('medium_term')
  const [tracksData, setTracksData] = useState<TopTracksResponse | null>(null)
  const [artistsData, setArtistsData] = useState<TopArtistsResponse | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    checkAuth()
  }, [])

  useEffect(() => {
    if (isAuthenticated && !user && !isLoadingUser) {
      loadUserInfo()
    }
  }, [isAuthenticated, user, isLoadingUser])

  useEffect(() => {
    if (showAnalytics) {
      loadData()
    }
  }, [showAnalytics, timeRange])

  const checkAuth = async () => {
    try {
      const auth = await api.checkAuth()
      setIsAuthenticated(auth)
      if (!auth) {
        setUser(null)
        setShowAnalytics(false)
      }
    } catch {
      setIsAuthenticated(false)
      setUser(null)
      setShowAnalytics(false)
    }
  }

  const loadUserInfo = async () => {
    setIsLoadingUser(true)
    try {
      const userInfo = await api.getUserInfo()
      setUser(userInfo)
    } catch (err: any) {
      console.error('Erro ao carregar dados do usuário:', err)
      // Se não conseguir carregar, usa dados padrão
      setUser({
        id: 'unknown',
        nome: 'Usuário',
        email: null,
        imagem_perfil: null,
        pais: null,
        seguidores: null,
      })
    } finally {
      setIsLoadingUser(false)
    }
  }

  const loadData = async () => {
    setIsLoading(true)
    setError(null)
    try {
      const [tracks, artists] = await Promise.all([
        api.getTopTracks(timeRange, 20),
        api.getTopArtists(timeRange, 20),
      ])
      setTracksData(tracks)
      setArtistsData(artists)
    } catch (err: any) {
      console.error('Erro ao carregar dados:', err)
      const errorMessage = err.response?.data?.mensagem || 'Erro ao carregar dados'
      setError(errorMessage)
      
      // Se for erro de token expirado, desautentica e volta para tela de login
      if (err.response?.status === 401 || err.response?.data?.codigo === 'token_expired') {
        setIsAuthenticated(false)
        setShowAnalytics(false)
        setUser(null)
      }
    } finally {
      setIsLoading(false)
    }
  }

  const handleLogin = () => {
    // Abre login em nova aba
    const apiUrl = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8888'
    window.open(`${apiUrl}/auth/login`, '_blank')
    
    // Verifica se o login foi feito quando a janela volta ao foco
    const handleFocus = async () => {
      try {
        const auth = await api.checkAuth()
        if (auth) {
          setIsAuthenticated(true)
          window.removeEventListener('focus', handleFocus)
        }
      } catch {
        // Ainda não autenticado
      }
    }
    
    // Verifica quando a janela volta ao foco
    window.addEventListener('focus', handleFocus)
    
    // Também faz polling a cada 3 segundos como fallback
    const checkInterval = setInterval(async () => {
      try {
        const auth = await api.checkAuth()
        if (auth) {
          setIsAuthenticated(true)
          clearInterval(checkInterval)
          window.removeEventListener('focus', handleFocus)
        }
      } catch {
        // Ainda não autenticado
      }
    }, 3000)

    // Limpa o intervalo após 5 minutos
    setTimeout(() => {
      clearInterval(checkInterval)
      window.removeEventListener('focus', handleFocus)
    }, 300000)
  }

  const handleAnalyze = () => {
    setShowAnalytics(true)
  }

  const handleLogout = async () => {
    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8888'
      await fetch(`${apiUrl}/auth/logout`)
      setIsAuthenticated(false)
      setUser(null)
      setShowAnalytics(false)
      setTracksData(null)
      setArtistsData(null)
    } catch {
      // Ignore errors on logout
    }
  }

  if (isAuthenticated === null) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner />
      </div>
    )
  }

  if (!isAuthenticated) {
    return <AuthSection onLogin={handleLogin} />
  }

  // Mostra painel de boas-vindas se ainda não clicou em analisar
  if (!showAnalytics) {
    if (isLoadingUser) {
      return (
        <div className="min-h-screen flex items-center justify-center">
          <LoadingSpinner />
        </div>
      )
    }
    return (
      <WelcomePanel
        userName={user?.nome || 'Usuário'}
        userImage={user?.imagem_perfil || null}
        onAnalyze={handleAnalyze}
      />
    )
  }

  return (
    <div className="min-h-screen p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8">
          <div>
            <h1 className="text-4xl md:text-5xl font-bold text-white mb-2 flex items-center gap-3">
              <Music className="text-spotify-green" size={48} />
              Spotify Analytics
            </h1>
            <p className="text-white/70 text-lg">Visualize seus dados de streaming</p>
          </div>
          <div className="flex gap-3 mt-4 md:mt-0">
            <button onClick={loadData} disabled={isLoading} className="btn-secondary flex items-center gap-2">
              <RefreshCw className={isLoading ? 'animate-spin' : ''} size={20} />
              Atualizar
            </button>
            <button onClick={handleLogout} className="btn-secondary flex items-center gap-2">
              <LogOut size={20} />
              Sair
            </button>
          </div>
        </div>

        {/* Time Range Selector */}
        <div className="card mb-6">
          <div className="flex flex-wrap items-center gap-4">
            <span className="text-white font-semibold">Período:</span>
            <div className="flex gap-2">
              {(['short_term', 'medium_term', 'long_term'] as TimeRange[]).map((range) => (
                <button
                  key={range}
                  onClick={() => setTimeRange(range)}
                  className={`px-4 py-2 rounded-lg font-medium transition-all ${
                    timeRange === range
                      ? 'bg-spotify-green text-white'
                      : 'bg-white/10 text-white/70 hover:bg-white/20'
                  }`}
                >
                  {range === 'short_term' && '4 Semanas'}
                  {range === 'medium_term' && '6 Meses'}
                  {range === 'long_term' && 'Todos os Tempos'}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="card mb-6 bg-red-500/20 border-red-500/50">
            <p className="text-red-200">{error}</p>
          </div>
        )}

        {/* Loading */}
        {isLoading && (
          <div className="flex justify-center py-12">
            <LoadingSpinner />
          </div>
        )}

        {/* Content */}
        {!isLoading && tracksData && artistsData && (
          <>
            {/* Stats Cards */}
            <StatsCards tracksData={tracksData} artistsData={artistsData} />

            {/* Charts Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
              <div className="card">
                <div className="flex items-center gap-2 mb-4">
                  <TrendingUp className="text-spotify-green" size={24} />
                  <h2 className="text-2xl font-bold text-white">Top 10 Músicas</h2>
                </div>
                {tracksData.itens && tracksData.itens.length > 0 ? (
                  <TracksChart data={tracksData.itens} />
                ) : (
                  <div className="flex items-center justify-center h-[300px] text-white/50">
                    Carregando dados...
                  </div>
                )}
              </div>

              <div className="card">
                <div className="flex items-center gap-2 mb-4">
                  <Music className="text-spotify-green" size={24} />
                  <h2 className="text-2xl font-bold text-white">Top 10 Artistas</h2>
                </div>
                {artistsData.itens && artistsData.itens.length > 0 ? (
                  <ArtistsChart data={artistsData.itens} />
                ) : (
                  <div className="flex items-center justify-center h-[300px] text-white/50">
                    Carregando dados...
                  </div>
                )}
              </div>
            </div>

            {/* Tracks Grid */}
            <div className="card">
              <div className="flex items-center gap-2 mb-6">
                <Clock className="text-spotify-green" size={24} />
                <h2 className="text-2xl font-bold text-white">Top Músicas</h2>
              </div>
              <TracksGrid tracks={tracksData.itens} />
            </div>
          </>
        )}
      </div>
    </div>
  )
}

export default App
