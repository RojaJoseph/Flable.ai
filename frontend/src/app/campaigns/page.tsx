'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import api from '@/lib/api'
import toast from 'react-hot-toast'
import Link from 'next/link'

interface Campaign {
  id: number
  name: string
  description: string
  status: string
  platform: string
  daily_budget: number
  total_budget: number
  impressions: number
  clicks: number
  conversions: number
  cost: number
  revenue: number
  roas: number
  ctr: number
  cpc: number
  optimization_score: number
  created_at: string
}

export default function CampaignsPage() {
  const router = useRouter()
  const [campaigns, setCampaigns] = useState<Campaign[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchCampaigns()
  }, [])

  const fetchCampaigns = async () => {
    try {
      const token = localStorage.getItem('access_token')
      if (!token) {
        router.push('/login')
        return
      }

      const response = await api.get('/campaigns', {
        headers: { Authorization: `Bearer ${token}` }
      })
      setCampaigns(response.data)
    } catch (error: any) {
      if (error.response?.status === 401) {
        router.push('/login')
      } else {
        toast.error('Failed to fetch campaigns')
      }
    } finally {
      setLoading(false)
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'bg-green-100 text-green-800'
      case 'paused': return 'bg-yellow-100 text-yellow-800'
      case 'draft': return 'bg-gray-100 text-gray-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const toggleCampaignStatus = async (campaignId: number, currentStatus: string) => {
    try {
      const token = localStorage.getItem('access_token')
      const newStatus = currentStatus === 'active' ? 'pause' : 'activate'

      await api.post(`/campaigns/${campaignId}/${newStatus}`, {}, {
        headers: { Authorization: `Bearer ${token}` }
      })

      toast.success(`Campaign ${newStatus}d successfully`)
      fetchCampaigns()
    } catch (error) {
      toast.error(`Failed to ${currentStatus === 'active' ? 'pause' : 'activate'} campaign`)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl text-gray-600">Loading campaigns...</div>
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
                <Link href="/campaigns" className="text-blue-600 px-3 py-2 rounded-md text-sm font-medium">
                  Campaigns
                </Link>
                <Link href="/analytics" className="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium">
                  Analytics
                </Link>
                <Link href="/integrations" className="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium">
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
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Campaigns</h1>
            <p className="text-gray-600 mt-1">Manage and optimize your marketing campaigns</p>
          </div>
          <Link
            href="/campaigns/new"
            className="px-6 py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition-colors shadow-lg"
          >
            + Create Campaign
          </Link>
        </div>

        {/* Campaigns Grid */}
        {campaigns.length === 0 ? (
          <div className="bg-white rounded-xl shadow-sm p-12 text-center">
            <div className="text-6xl mb-4">📊</div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">No campaigns yet</h3>
            <p className="text-gray-600 mb-6">Create your first campaign to start optimizing with AI</p>
            <Link
              href="/campaigns/new"
              className="px-6 py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition-colors"
            >
              Create Campaign
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {campaigns.map((campaign) => (
              <div key={campaign.id} className="bg-white rounded-xl shadow-sm hover:shadow-md transition-shadow p-6">
                {/* Header */}
                <div className="flex justify-between items-start mb-4">
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold text-gray-900 mb-1">{campaign.name}</h3>
                    <p className="text-sm text-gray-600">{campaign.platform}</p>
                  </div>
                  <span className={`px-3 py-1 rounded-full text-xs font-semibold ${getStatusColor(campaign.status)}`}>
                    {campaign.status}
                  </span>
                </div>

                {/* Metrics */}
                <div className="space-y-3 mb-4">
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">ROAS</span>
                    <span className="text-sm font-semibold text-gray-900">{campaign.roas.toFixed(2)}x</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Conversions</span>
                    <span className="text-sm font-semibold text-gray-900">{campaign.conversions}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Cost</span>
                    <span className="text-sm font-semibold text-gray-900">${campaign.cost.toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Revenue</span>
                    <span className="text-sm font-semibold text-green-600">${campaign.revenue.toFixed(2)}</span>
                  </div>
                </div>

                {/* AI Optimization Score */}
                <div className="mb-4">
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-gray-600">AI Optimization</span>
                    <span className="font-semibold">{(campaign.optimization_score * 100).toFixed(0)}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-blue-600 h-2 rounded-full"
                      style={{ width: `${campaign.optimization_score * 100}%` }}
                    />
                  </div>
                </div>

                {/* Actions */}
                <div className="flex gap-2">
                  <button
                    onClick={() => router.push(`/campaigns/${campaign.id}`)}
                    className="flex-1 px-4 py-2 bg-blue-50 text-blue-600 rounded-lg text-sm font-semibold hover:bg-blue-100 transition-colors"
                  >
                    View Details
                  </button>
                  <button
                    onClick={() => toggleCampaignStatus(campaign.id, campaign.status)}
                    className={`px-4 py-2 rounded-lg text-sm font-semibold transition-colors ${campaign.status === 'active'
                      ? 'bg-yellow-50 text-yellow-600 hover:bg-yellow-100'
                      : 'bg-green-50 text-green-600 hover:bg-green-100'
                      }`}
                  >
                    {campaign.status === 'active' ? 'Pause' : 'Activate'}
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>


    </div>
  )
}
