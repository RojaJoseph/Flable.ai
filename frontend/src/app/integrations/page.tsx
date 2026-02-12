'use client'

import { useState, useEffect } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import api from '@/lib/api'
import toast from 'react-hot-toast'
import Link from 'next/link'

interface Integration {
  id: number
  platform: string
  status: string
  shop_domain: string
  last_sync: string | null
  created_at: string
}

export default function IntegrationsPage() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const [integrations, setIntegrations] = useState<Integration[]>([])
  const [loading, setLoading] = useState(true)
  const [showShopifyModal, setShowShopifyModal] = useState(false)
  const [shopifyData, setShopifyData] = useState({
    shop_domain: ''
  })
  const [connecting, setConnecting] = useState(false)

  useEffect(() => {
    fetchIntegrations()

    // Check for success from OAuth callback
    if (searchParams.get('success') === 'true') {
      const shop = searchParams.get('shop')
      toast.success(`Successfully connected ${shop}!`)
      // Clean up URL
      window.history.replaceState({}, '', '/integrations')
    }
  }, [searchParams])

  const fetchIntegrations = async () => {
    try {
      const token = localStorage.getItem('access_token')
      if (!token) {
        router.push('/login')
        return
      }

      const response = await api.get('/integrations', {
        headers: { Authorization: `Bearer ${token}` }
      })
      setIntegrations(response.data)
    } catch (error: any) {
      if (error.response?.status === 401) {
        router.push('/login')
      } else {
        toast.error('Failed to fetch integrations')
      }
    } finally {
      setLoading(false)
    }
  }

  const connectShopifyOAuth = async (e: React.FormEvent) => {
    e.preventDefault()
    setConnecting(true)

    try {
      const token = localStorage.getItem('access_token')

      // Get OAuth authorization URL
      const response = await api.get(`/integrations/shopify/auth?shop=${shopifyData.shop_domain}`, {
        headers: { Authorization: `Bearer ${token}` }
      })

      // Redirect to Shopify OAuth page
      window.location.href = response.data.auth_url

    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to start Shopify connection')
      setConnecting(false)
    }
  }

  const syncIntegration = async (integrationId: number) => {
    try {
      const token = localStorage.getItem('access_token')

      await api.post(`/integrations/${integrationId}/sync`, {}, {
        headers: { Authorization: `Bearer ${token}` }
      })

      toast.success('Sync started! This may take a few minutes.')

      // Refresh integrations after a delay
      setTimeout(fetchIntegrations, 2000)
    } catch (error) {
      toast.error('Failed to start sync')
    }
  }

  const disconnectIntegration = async (integrationId: number) => {
    if (!confirm('Are you sure you want to disconnect this integration?')) return

    try {
      const token = localStorage.getItem('access_token')

      await api.delete(`/integrations/${integrationId}`, {
        headers: { Authorization: `Bearer ${token}` }
      })

      toast.success('Integration disconnected')
      fetchIntegrations()
    } catch (error) {
      toast.error('Failed to disconnect integration')
    }
  }

  const getPlatformIcon = (platform: string) => {
    switch (platform) {
      case 'shopify': return '🛍️'
      case 'google_ads': return '🔍'
      case 'facebook': return '👥'
      default: return '🔗'
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'connected': return 'bg-green-100 text-green-800'
      case 'error': return 'bg-red-100 text-red-800'
      case 'pending': return 'bg-yellow-100 text-yellow-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl text-gray-600">Loading integrations...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <Link href="/dashboard" className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                Flable.ai
              </Link>
              <div className="ml-10 flex space-x-4">
                <Link href="/dashboard" className="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium">
                  Dashboard
                </Link>
                <Link href="/campaigns" className="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium">
                  Campaigns
                </Link>
                <Link href="/analytics" className="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium">
                  Analytics
                </Link>
                <Link href="/integrations" className="text-blue-600 px-3 py-2 rounded-md text-sm font-medium">
                  Integrations
                </Link>
              </div>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Integrations</h1>
          <p className="text-gray-600 mt-1">Connect your marketing platforms and e-commerce stores</p>
        </div>

        {/* Available Integrations */}
        <div className="mb-8">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Available Integrations</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Shopify with OAuth */}
            <div className="bg-white rounded-xl shadow-sm p-6 hover:shadow-md transition-shadow">
              <div className="text-5xl mb-4">🛍️</div>
              <h3 className="text-xl font-semibold mb-2">Shopify</h3>
              <p className="text-gray-600 text-sm mb-4">
                Connect your Shopify store with secure OAuth to sync products, orders, and analytics
              </p>
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-3 mb-4">
                <p className="text-xs text-blue-800">
                  ✨ <strong>OAuth 2.0</strong> - Secure authentication
                </p>
              </div>
              <button
                onClick={() => setShowShopifyModal(true)}
                className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition-colors"
              >
                Connect Shopify
              </button>
            </div>

            {/* Google Ads - Coming Soon */}
            <div className="bg-white rounded-xl shadow-sm p-6 opacity-60">
              <div className="text-5xl mb-4">🔍</div>
              <h3 className="text-xl font-semibold mb-2">Google Ads</h3>
              <p className="text-gray-600 text-sm mb-4">
                Optimize your Google Ads campaigns with AI
              </p>
              <button
                disabled
                className="w-full px-4 py-2 bg-gray-300 text-gray-600 rounded-lg font-semibold cursor-not-allowed"
              >
                Coming Soon
              </button>
            </div>

            {/* Facebook Ads - Coming Soon */}
            <div className="bg-white rounded-xl shadow-sm p-6 opacity-60">
              <div className="text-5xl mb-4">👥</div>
              <h3 className="text-xl font-semibold mb-2">Facebook Ads</h3>
              <p className="text-gray-600 text-sm mb-4">
                Manage Facebook and Instagram ad campaigns
              </p>
              <button
                disabled
                className="w-full px-4 py-2 bg-gray-300 text-gray-600 rounded-lg font-semibold cursor-not-allowed"
              >
                Coming Soon
              </button>
            </div>
          </div>
        </div>

        {/* Connected Integrations */}
        {integrations.length > 0 && (
          <div>
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Connected Integrations</h2>
            <div className="space-y-4">
              {integrations.map((integration) => (
                <div key={integration.id} className="bg-white rounded-xl shadow-sm p-6">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-4">
                      <div className="text-4xl">{getPlatformIcon(integration.platform)}</div>
                      <div>
                        <h3 className="text-lg font-semibold capitalize">{integration.platform}</h3>
                        <p className="text-sm text-gray-600">{integration.shop_domain}</p>
                        {integration.last_sync && (
                          <p className="text-xs text-gray-500 mt-1">
                            Last synced: {new Date(integration.last_sync).toLocaleString()}
                          </p>
                        )}
                      </div>
                    </div>
                    <div className="flex items-center space-x-3">
                      <span className={`px-3 py-1 rounded-full text-xs font-semibold ${getStatusColor(integration.status)}`}>
                        {integration.status}
                      </span>
                      <button
                        onClick={() => syncIntegration(integration.id)}
                        className="px-4 py-2 bg-blue-50 text-blue-600 rounded-lg text-sm font-semibold hover:bg-blue-100 transition-colors"
                      >
                        Sync Now
                      </button>
                      <button
                        onClick={() => disconnectIntegration(integration.id)}
                        className="px-4 py-2 bg-red-50 text-red-600 rounded-lg text-sm font-semibold hover:bg-red-100 transition-colors"
                      >
                        Disconnect
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Shopify OAuth Modal */}
      {showShopifyModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-xl max-w-md w-full p-6">
            <h2 className="text-2xl font-bold mb-4">Connect Shopify Store</h2>
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-4">
              <p className="text-sm text-blue-800">
                <strong>🔒 Secure OAuth 2.0</strong><br />
                You'll be redirected to Shopify to authorize access. We never see your password.
              </p>
            </div>
            <p className="text-gray-600 text-sm mb-6">
              Enter your Shopify store domain to begin the connection process.
            </p>

            <form onSubmit={connectShopifyOAuth} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Shop Domain
                </label>
                <div className="flex items-center">
                  <input
                    type="text"
                    required
                    className="flex-1 px-4 py-3 border border-gray-300 rounded-l-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="your-store"
                    value={shopifyData.shop_domain}
                    onChange={(e) => setShopifyData({ shop_domain: e.target.value })}
                  />
                  <span className="px-4 py-3 bg-gray-100 border border-l-0 border-gray-300 rounded-r-lg text-gray-600">
                    .myshopify.com
                  </span>
                </div>
                <p className="text-xs text-gray-500 mt-1">
                  Just enter your store name, we'll add .myshopify.com
                </p>
              </div>

              <div className="bg-gray-50 rounded-lg p-4">
                <h4 className="font-semibold text-sm text-gray-900 mb-2">What happens next?</h4>
                <ol className="text-xs text-gray-600 space-y-1">
                  <li>1. You'll be redirected to Shopify</li>
                  <li>2. Review and approve permissions</li>
                  <li>3. You'll return here automatically</li>
                  <li>4. We'll sync your data!</li>
                </ol>
              </div>

              <div className="flex gap-3 pt-4">
                <button
                  type="button"
                  onClick={() => setShowShopifyModal(false)}
                  className="flex-1 px-4 py-3 bg-gray-200 text-gray-800 rounded-lg font-semibold hover:bg-gray-300 transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={connecting}
                  className="flex-1 px-4 py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  {connecting ? 'Connecting...' : 'Connect with Shopify'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}
