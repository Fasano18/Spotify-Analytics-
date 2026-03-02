import { Sparkles, BarChart3, Music } from 'lucide-react'

interface WelcomePanelProps {
  userName: string
  userImage: string | null
  onAnalyze: () => void
}

export default function WelcomePanel({ userName, userImage, onAnalyze }: WelcomePanelProps) {
  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="max-w-2xl w-full">
        <div className="card text-center">
          <div className="flex justify-center mb-6">
            {userImage ? (
              <img
                src={userImage}
                alt={userName}
                className="w-24 h-24 rounded-full border-4 border-spotify-green shadow-lg"
              />
            ) : (
              <div className="w-24 h-24 rounded-full bg-spotify-green flex items-center justify-center">
                <Music className="text-white" size={48} />
              </div>
            )}
          </div>
          
          <h1 className="text-4xl md:text-5xl font-bold text-white mb-4">
            Olá, {userName}! 👋
          </h1>
          
          <p className="text-white/70 text-lg mb-8">
            Descubra insights incríveis sobre seus hábitos de streaming no Spotify
          </p>

          <button
            onClick={onAnalyze}
            className="btn-primary text-lg px-8 py-4 flex items-center gap-3 mx-auto group"
          >
            <Sparkles className="group-hover:rotate-12 transition-transform" size={24} />
            <span>Analisar Meus Dados</span>
            <BarChart3 className="group-hover:scale-110 transition-transform" size={24} />
          </button>

          <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4 text-white/60 text-sm">
            <div className="flex items-center justify-center gap-2">
              <Music size={20} />
              <span>Top Músicas</span>
            </div>
            <div className="flex items-center justify-center gap-2">
              <BarChart3 size={20} />
              <span>Gráficos Interativos</span>
            </div>
            <div className="flex items-center justify-center gap-2">
              <Sparkles size={20} />
              <span>Estatísticas</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
