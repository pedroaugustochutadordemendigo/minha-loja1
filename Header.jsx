import { useState } from 'react'
import { Search, User, Heart, ShoppingCart, Menu, X } from 'lucide-react'
import { Button } from '@/components/ui/button'

const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const [isSearchOpen, setIsSearchOpen] = useState(false)
  const [cartCount] = useState(0)

  const navItems = [
    { name: 'Home', href: '#' },
    { name: 'Produtos', href: '#produtos' },
    { name: 'Novidades', href: '#novidades' },
    { name: 'Coleções', href: '#colecoes' },
    { name: 'Ofertas', href: '#ofertas' }
  ]

  return (
    <header className="fixed top-0 left-0 right-0 z-50 glass-effect border-b border-white/10">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex items-center">
            <h1 className="logo-packs text-white">packs</h1>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            {navItems.map((item) => (
              <a