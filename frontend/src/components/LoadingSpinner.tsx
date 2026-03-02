export default function LoadingSpinner() {
  return (
    <div className="flex flex-col items-center justify-center gap-4">
      <div className="w-16 h-16 border-4 border-spotify-green border-t-transparent rounded-full animate-spin"></div>
      <p className="text-white/70">Carregando dados...</p>
    </div>
  )
}
