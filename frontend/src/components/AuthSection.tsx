import { Music } from 'lucide-react'

interface AuthSectionProps {
  onLogin: () => void
}

export default function AuthSection({ onLogin }: AuthSectionProps) {
  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="card max-w-md w-full text-center">
        <div className="flex justify-center mb-6">
          <div className="w-20 h-20 bg-spotify-green rounded-full flex items-center justify-center">
            <Music className="text-white" size={48} />
          </div>
        </div>
        <h2 className="text-3xl font-bold text-white mb-4">Bem-vindo ao Spotify Analytics</h2>
        <p className="text-white/70 mb-8">
          Faça login com sua conta do Spotify para visualizar seus dados de streaming de forma
          profissional.
        </p>
        <button onClick={onLogin} className="btn-primary w-full">
          Fazer Login com Spotify
        </button>
      </div>
    </div>
  )
}
