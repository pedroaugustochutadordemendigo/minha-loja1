import { useState } from 'react'
import { Mail, Phone, MapPin, Instagram, Facebook, Twitter, Youtube } from 'lucide-react'
import { Button } from '@/components/ui/button'

const Footer = () => {
  const [email, setEmail] = useState('')

  const handleNewsletterSubmit = (e) => {
    e.preventDefault()
    // Handle newsletter subscription
    console.log('Newsletter subscription:', email)
    setEmail('')
  }

  const footerLinks = {
    shop: [
      { name: 'Camisetas', href: '#' },
      { name: 'Hoodies', href: '#' },
      { name: 'Jaquetas', href: '#' },
      { name: 'Calças', href: '#' },
      { name: 'Acessórios', href: '#' },
      { name: 'Calçados', href: '#' }
    ],
    company: [
      { name: 'Sobre Nós', href: '#' },
      { name: 'Nossa História', href: '#' },
      { name: 'Carreiras', href: '#' },
      { name: 'Imprensa', href: '#' },
      { name: 'Sustentabilidade', href: '#' }
    ],
    support: [
      { name: 'Central de Ajuda', href: '#' },
      { name: 'Contato', href: '#' },
      { name: 'Trocas e Devoluções', href: '#' },
      { name: 'Guia de Tamanhos', href: '#' },
      { name: 'Rastreamento', href: '#' }
    ],
    legal: [
      { name: 'Política de Privacidade', href: '#' },
      { name: 'Termos de Uso', href: '#' },
      { name: 'Política de Cookies', href: '#' },
      { name: 'Termos de Venda', href: '#' }
    ]
  }

  const socialLinks = [
    { name: 'Instagram', icon: Instagram, href: 'https://instagram.com/packs_streetwear' },
    { name: 'Facebook', icon: Facebook, href: 'https://facebook.com/packsstreetwearbr' },
    { name: 'Twitter', icon: Twitter, href: 'https://twitter.com/packs_streetwear' },
    { name: 'YouTube', icon: Youtube, href: 'https://youtube.com/packsstreetwearbr' }
  ]

  return (
    <footer className="bg-gray-900 border-t border-white/10">
      {/* Newsletter Section */}
      <div className="border-b border-white/10">
        <div className="container-custom py-12">
          <div className="max-w-4xl mx-auto text-center">
            <h3 className="text-2xl md:text-3xl font-bold text-white mb-4">
              Fique por dentro das <span className="text-gradient">novidades</span>
            </h3>
            <p className="text-white/80 mb-8">
              Receba em primeira mão nossos lançamentos, promoções exclusivas e conteúdo sobre streetwear
            </p>
            
            <form onSubmit={handleNewsletterSubmit} className="flex flex-col sm:flex-row gap-4 max-w-md mx-auto">
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Seu melhor e-mail"
                className="input-custom flex-1"
                required
              />
              <Button type="submit" className="btn-primary">
                <Mail className="mr-2 h-4 w-4" />
                Inscrever-se
              </Button>
            </form>
          </div>
        </div>
      </div>

      {/* Main Footer Content */}
      <div className="container-custom py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-8">
          {/* Brand Section */}
          <div className="lg:col-span-2">
            <h2 className="logo-packs text-white text-3xl mb-4">packs</h2>
            <p className="text-white/80 mb-6 max-w-md">
              Streetwear autêntico para quem não passa despercebido. 
              Qualidade premium, design exclusivo e atitude urbana em cada peça.
            </p>
            
            {/* Contact Info */}
            <div className="space-y-3">
              <div className="flex items-center gap-3 text-white/80">
                <MapPin className="h-4 w-4 text-green-500" />
                <span>Monte Belo, MG - Brasil</span>
              </div>
              <div className="flex items-center gap-3 text-white/80">
                <Phone className="h-4 w-4 text-green-500" />
                <span>+55 (35) 99999-9999</span>
              </div>
              <div className="flex items-center gap-3 text-white/80">
                <Mail className="h-4 w-4 text-green-500" />
                <span>packsorganization@gmail.com</span>
              </div>
            </div>

            {/* Social Links */}
            <div className="flex gap-4 mt-6">
              {socialLinks.map((social) => {
                const Icon = social.icon
                return (
                  <a
                    key={social.name}
                    href={social.href}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="w-10 h-10 bg-white/10 hover:bg-green-500 rounded-lg flex items-center justify-center transition-colors duration-300 group"
                  >
                    <Icon className="h-5 w-5 text-white group-hover:text-black" />
                  </a>
                )
              })}
            </div>
          </div>

          {/* Shop Links */}
          <div>
            <h4 className="text-white font-semibold mb-4">Loja</h4>
            <ul className="space-y-2">
              {footerLinks.shop.map((link) => (
                <li key={link.name}>
                  <a
                    href={link.href}
                    className="text-white/80 hover:text-green-500 transition-colors duration-300"
                  >
                    {link.name}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Company Links */}
          <div>
            <h4 className="text-white font-semibold mb-4">Empresa</h4>
            <ul className="space-y-2">
              {footerLinks.company.map((link) => (
                <li key={link.name}>
                  <a
                    href={link.href}
                    className="text-white/80 hover:text-green-500 transition-colors duration-300"
                  >
                    {link.name}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Support Links */}
          <div>
            <h4 className="text-white font-semibold mb-4">Suporte</h4>
            <ul className="space-y-2">
              {footerLinks.support.map((link) => (
                <li key={link.name}>
                  <a
                    href={link.href}
                    className="text-white/80 hover:text-green-500 transition-colors duration-300"
                  >
                    {link.name}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>

      {/* Bottom Bar */}
      <div className="border-t border-white/10">
        <div className="container-custom py-6">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <div className="text-white/60 text-sm">
              © 2024 PACKS Streetwear. Todos os direitos reservados.
            </div>
            
            <div className="flex flex-wrap gap-6">
              {footerLinks.legal.map((link) => (
                <a
                  key={link.name}
                  href={link.href}
                  className="text-white/60 hover:text-green-500 text-sm transition-colors duration-300"
                >
                  {link.name}
                </a>
              ))}
            </div>
          </div>
        </div>
      </div>
    </footer>
  )
}

export default Footer

