import { useState } from 'react'
import Header from './components/Header'
import HeroBanner from './components/HeroBanner'
import ProductGrid from './components/ProductGrid'
import Footer from './components/Footer'
import './App.css'

function App() {
  return (
    <div className="min-h-screen bg-background">
      <Header />
      <main>
        <HeroBanner />
        <ProductGrid />
      </main>
      <Footer />
    </div>
  )
}

export default App
