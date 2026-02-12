'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { dashboard, campaigns as campaignsApi } from '@/lib/api'

export default function Dashboard() {
  const [stats, setStats] = useState<any>(null)
  const [campaigns, setCampaigns] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadDashboard()
  }, [])

  const loadDashboard = async () => {
    try {
      const [dashboardRes, campaignsRes] = await Promise.all([
        dashboard.get(),
        campaignsApi.list({ limit: 10 })
      ])
      
      setStats(dashboardRes.data.stats)
      setCampaigns(campaignsRes.data)
      setLoading(false)
    } catch (error) {
      console.error('Error loading dashboard:', error)
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-2xl text-gray-600">Loading...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex justify-between items-center">
            <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
            <Link 
              href="/campaigns/new"
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              + New Campaign
            </Link>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatCard 
            title="Total Campaigns" 
            value={stats?.total_campaigns || 0}
            subtitle={`${stats?.active_campaigns || 0} active`}
            icon="📊"
          />
          <StatCard 
            title="Total Spend" 
            value={`$${(stats?.total_spend || 0).toLocaleString()}`}
            subtitle="All time"
            icon="💰"
          />
          <StatCard 
            title="Total Revenue" 
            value={`$${(stats?.total_revenue || 0).toLocaleString()}`}
            subtitle={`ROAS: ${(stats?.average_roas || 0).toFixed(2)}x`}
            icon="📈"
          />
          <StatCard 
            title="Conversions" 
            value={(stats?.total_conversions || 0).toLocaleString()}
            subtitle={`CTR: ${(stats?.average_ctr || 0).toFixed(2)}%`}
            icon="🎯"
          />
        </div>

        {/* Recent Campaigns */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-2xl font-bold mb-4">Recent Campaigns</h2>
          
          {campaigns.length === 0 ? (
            <div className="text-center py-12 text-gray-500">
              <p className="text-xl mb-4">No campaigns yet</p>
              <Link 
                href="/campaigns/new"
                className="inline-block px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                Create Your First Campaign
              </Link>
            </div>
          ) : (
            <div className="space-y-4">
              {campaigns.map((campaign) => (
                <CampaignCard key={campaign.id} campaign={campaign} />
              ))}
            </div>
          )}
        </div>
      </main>
    </div>
  )
}

function StatCard({ title, value, subtitle, icon }: any) {
  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-center justify-between mb-2">
        <div className="text-sm font-medium text-gray-600">{title}</div>
        <div className="text-2xl">{icon}</div>
      </div>
      <div className="text-3xl font-bold text-gray-900 mb-1">{value}</div>
      <div className="text-sm text-gray-500">{subtitle}</div>
    </div>
  )
}

function CampaignCard({ campaign }: any) {
  const statusColors: any = {
    active: 'bg-green-100 text-green-800',
    paused: 'bg-yellow-100 text-yellow-800',
    draft: 'bg-gray-100 text-gray-800',
  }

  return (
    <Link href={`/campaigns/${campaign.id}`}>
      <div className="border border-gray-200 rounded-lg p-4 hover:border-blue-500 hover:shadow-md transition-all cursor-pointer">
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-lg font-semibold">{campaign.name}</h3>
          <span className={`px-3 py-1 rounded-full text-sm font-medium ${statusColors[campaign.status] || 'bg-gray-100 text-gray-800'}`}>
            {campaign.status}
          </span>
        </div>
        
        <div className="grid grid-cols-4 gap-4 mt-4">
          <div>
            <div className="text-sm text-gray-600">Impressions</div>
            <div className="font-semibold">{campaign.impressions?.toLocaleString() || 0}</div>
          </div>
          <div>
            <div className="text-sm text-gray-600">Clicks</div>
            <div className="font-semibold">{campaign.clicks?.toLocaleString() || 0}</div>
          </div>
          <div>
            <div className="text-sm text-gray-600">Conversions</div>
            <div className="font-semibold">{campaign.conversions?.toLocaleString() || 0}</div>
          </div>
          <div>
            <div className="text-sm text-gray-600">ROAS</div>
            <div className="font-semibold text-blue-600">{campaign.roas?.toFixed(2) || '0.00'}x</div>
          </div>
        </div>
      </div>
    </Link>
  )
}
