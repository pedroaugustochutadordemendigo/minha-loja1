import { useState, useEffect } from 'react'
import { ChevronLeft, ChevronRight, Play } from 'lucide-react'
import { Button } from '@/components/ui/button'

const HeroBanner = () => {
  const [currentSlide, setCurrentSlide] = useState(0)

  const slides = [
    {
      id: 1,
      title: "Nova Coleção",
      subtitle: "Streetwear Autêntico",
      description: "Descubra as últimas tendências em moda urbana com designs exclusivos e qualidade premium.",
      cta: "Explorar Coleção",
      image: "/api/placeholder/1200/600",
      video: null
    },
    {
      id: 2,
      title: "Estilo Urbano",
      subtitle: "Para Quem Não Passa Despercebido",
      description: "Peças únicas que expressam sua personalidade e atitude nas ruas da cidade.",
      cta: "Ver Produtos",
      image: "/api/placeholder/1200/600",
      video: null
    },
    {
      id: 3,
      title: "Qualidade Premium",
      subtitle: "Feito Para Durar",
      description: "Materiais selecionados e acabamento impecável em cada peça da nossa coleção.",
      cta: "Conhecer Mais",
      image: "/api/placeholder/1200/600",
      video: null
    }
  ]

  // Auto-slide
  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentSlide((prev) => (prev + 1) % slides.length)
    }, 5000)

    return () => clearInterval(timer)
  }, [slides.length])

  const nextSlide = () => {
    setCurrentSlide((prev) => (prev + 1) % slides.length)
  }

  const prevSlide = () => {
    setCurrentSlide((prev) => (prev - 1 + slides.length) % slides.length)
  }

  const goToSlide = (index) => {
    setCurrentSlide(index)
  }

  return (
    <section className="relative h-screen flex items-center justify-center overflow-hidden">
      {/* Background Slides */}
      <div className="absolute inset-0">
        {slides.map((slide, index) => (
          <div
            key={slide.id}
            className={`absolute inset-0 transition-opacity duration-1000 ${
              index === currentSlide ? 'opacity-100' : 'opacity-0'
            }`}
          >
            {slide.video ? (
              <video
                className="w-full h-full object-cover"
                autoPlay
                muted
                loop
                playsInline
              >
                <source src={slide.video} type="video/mp4" />
              </video>
            ) : (
              <div
                className="w-full h-full bg-cover bg-center bg-no-repeat"
                style={{
                  backgroundImage: `url(${slide.image})`,
                }}
              />
            )}
            {/* Overlay */}
            <div className="absolute inset-0 bg-black/40" />
          </div>
        ))}
      </div>

      {/* Content */}
      <div className="relative z-10 container-custom text-center">
        <div className="max-w-4xl mx-auto">
          {slides.map((slide, index) => (
            <div
              key={slide.id}
              className={`transition-all duration-1000 ${
                index === currentSlide
                  ? 'opacity-100 transform translate-y-0'
                  : 'opacity-0 transform translate-y-8'
              }`}
            >
              {index === currentSlide && (
                <>
                  <h2 className="text-green-500 text-lg md:text-xl font-semibold mb-4 fade-in">
                    {slide.subtitle}
                  </h2>
                  <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold text-white mb-6 slide-up">
                    {slide.title}
                  </h1>
                  <p className="text-lg md:text-xl text-white/80 mb-8 max-w-2xl mx-auto fade-in">
                    {slide.description}
                  </p>
                  <div className="flex flex-col sm:flex-row gap-4 justify-center items-center fade-in">
                    <Button className="btn-primary text-lg px-8 py-4">
                      {slide.cta}
                    </Button>
                    <Button variant="outline" className="btn-secondary text-lg px-8 py-4">
                      <Play className="mr-2 h-5 w-5" />
                      Ver Vídeo
                    </Button>
                  </div>
                </>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Navigation Arrows */}
      <Button
        variant="ghost"
        size="icon"
        onClick={prevSlide}
        className="absolute left-4 top-1/2 transform -translate-y-1/2 z-20 text-white hover:bg-white/10 h-12 w-12"
      >
        <ChevronLeft className="h-6 w-6" />
      </Button>

      <Button
        variant="ghost"
        size="icon"
        onClick={nextSlide}
        className="absolute right-4 top-1/2 transform -translate-y-1/2 z-20 text-white hover:bg-white/10 h-12 w-12"
      >
        <ChevronRight className="h-6 w-6" />
      </Button>

      {/* Slide Indicators */}
      <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 z-20">
        <div className="flex space-x-2">
          {slides.map((_, index) => (
            <button
              key={index}
              onClick={() => goToSlide(index)}
              className={`w-3 h-3 rounded-full transition-all duration-300 ${
                index === currentSlide
                  ? 'bg-green-500 w-8'
                  : 'bg-white/50 hover:bg-white/70'
              }`}
            />
          ))}
        </div>
      </div>

      {/* Scroll Indicator */}
      <div className="absolute bottom-8 right-8 z-20 text-white/60">
        <div className="flex flex-col items-center space-y-2">
          <span className="text-sm font-medium">Scroll</span>
          <div className="w-px h-8 bg-white/30 relative">
            <div className="absolute top-0 w-px h-4 bg-green-500 animate-pulse" />
          </div>
        </div>
      </div>
    </section>
  )
}

export default HeroBanner

