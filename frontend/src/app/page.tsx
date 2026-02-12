'use client'

import Link from 'next/link'

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24 bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="max-w-5xl w-full text-center">
        {/* Logo/Brand */}
        <div className="mb-8">
          <h1 className="text-6xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
            Flable.ai
          </h1>
          <p className="text-xl text-gray-600 mt-4">
            AI-Powered Marketing Platform
          </p>
        </div>

        {/* Hero Section */}
        <div className="bg-white rounded-2xl shadow-2xl p-12 mb-8">
          <h2 className="text-4xl font-bold text-gray-900 mb-6">
            Automate & Optimize Your Marketing Campaigns
          </h2>
          <p className="text-lg text-gray-600 mb-8 max-w-2xl mx-auto">
            Leverage AI to maximize your ROAS, reduce ad spend waste, and scale winning campaigns automatically.
          </p>

          {/* CTA Buttons */}
          <div className="flex gap-4 justify-center">
            <Link 
              href="/dashboard"
              className="px-8 py-4 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition-colors shadow-lg hover:shadow-xl"
            >
              Get Started
            </Link>
            <Link 
              href="/dashboard"
              className="px-8 py-4 bg-white border-2 border-blue-600 text-blue-600 rounded-lg font-semibold hover:bg-blue-50 transition-colors"
            >
              View Dashboard
            </Link>
          </div>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white p-6 rounded-xl shadow-lg">
            <div className="text-4xl mb-4">🤖</div>
            <h3 className="text-xl font-semibold mb-2">AI Optimization</h3>
            <p className="text-gray-600">
              Machine learning models continuously optimize your campaigns for maximum ROI
            </p>
          </div>
          
          <div className="bg-white p-6 rounded-xl shadow-lg">
            <div className="text-4xl mb-4">📊</div>
            <h3 className="text-xl font-semibold mb-2">Real-Time Analytics</h3>
            <p className="text-gray-600">
              Track performance metrics and get actionable insights in real-time
            </p>
          </div>
          
          <div className="bg-white p-6 rounded-xl shadow-lg">
            <div className="text-4xl mb-4">🛍️</div>
            <h3 className="text-xl font-semibold mb-2">Shopify Integration</h3>
            <p className="text-gray-600">
              Seamlessly connect your Shopify store and sync products & orders
            </p>
          </div>
        </div>

        {/* Stats */}
        <div className="bg-white rounded-xl shadow-lg p-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div>
              <div className="text-3xl font-bold text-blue-600">350%</div>
              <div className="text-gray-600">Average ROAS Increase</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-blue-600">60%</div>
              <div className="text-gray-600">Ad Spend Reduction</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-blue-600">24/7</div>
              <div className="text-gray-600">AI Monitoring</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-blue-600">10K+</div>
              <div className="text-gray-600">Campaigns Optimized</div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="mt-12 text-gray-500 text-sm">
          <p>Enterprise-grade AI marketing platform • Built with FastAPI, Next.js, and Machine Learning</p>
        </div>
      </div>
    </main>
  )
}
