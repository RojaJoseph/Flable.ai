'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import api from '@/lib/api'
import toast from 'react-hot-toast'
import Link from 'next/link'
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

interface AnalyticsData {
  date: string
  impressions: number
  clicks: number
  conversions: number
  cost: number
  revenue: number
  roas: number
}

export default function AnalyticsPage() {
  const router = useRouter()
  const [loading, setLoading] = useState(true)
  const [overview, setOverview] = useState<any>(null)
  const [chartData, setChartData] = useState<AnalyticsData[]>([])
  const [dateRange, setDateRange] = useState(30)

  useEffect(() => {
    fetchAnalytics()
  }, [dateRange])

  const fetchAnalytics = async () => {
    try {
      const token = localStorage.getItem('access_token')
      if (!token) {
        router.push('/login')
        return
      }

      // Fetch overview
      const overviewResponse = await api.get(`/analytics/overview?days=${dateRange}`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      setOverview(overviewResponse.data)

      // Generate sample chart data (in real app, this would come from API)
      const sampleData: AnalyticsData[] = []
      for (let i = dateRange - 1; i >= 0; i--) {
        const date = new Date()
        date.setDate(date.getDate() - i)
        sampleData.push({
          date: date.toISOString().split('T')[0],
          impressions: Math.floor(Math.random() * 10000) + 5000,
          clicks: Math.floor(Math.random() * 500) + 100,
          conversions: Math.floor(Math.random() * 50) + 10,
          cost: Math.floor(Math.random() * 1000) + 200,
          revenue: Math.floor(Math.random() * 3000) + 500,
          roas: Math.random() * 4 + 1
        })
      }
      setChartData(sampleData)

    } catch (error: any) {
      if (error.response?.status === 401) {
        router.push('/login')
      } else {
        toast.error('Failed to fetch analytics')
      }
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl text-gray-600">Loading analytics...</div>
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
                <Link href="/analytics" className="text-blue-600 px-3 py-2 rounded-md text-sm font-medium">
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
            <h1 className="text-3xl font-bold text-gray-900">Analytics</h1>
            <p className="text-gray-600 mt-1">Track and analyze campaign performance</p>
          </div>

          {/* Date Range Selector */}
          <select
            value={dateRange}
            onChange={(e) => setDateRange(Number(e.target.value))}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value={7}>Last 7 days</option>
            <option value={30}>Last 30 days</option>
            <option value={90}>Last 90 days</option>
          </select>
        </div>

        {/* Overview Stats */}
        {overview && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <div className="bg-white rounded-xl shadow-sm p-6">
              <div className="text-sm text-gray-600 mb-1">Total Spend</div>
              <div className="text-3xl font-bold text-gray-900">
                ${overview.metrics?.total_spend?.toFixed(2) || '0.00'}
              </div>
              <div className="text-xs text-gray-500 mt-2">
                {dateRange} days
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-sm p-6">
              <div className="text-sm text-gray-600 mb-1">Total Revenue</div>
              <div className="text-3xl font-bold text-green-600">
                ${overview.metrics?.total_revenue?.toFixed(2) || '0.00'}
              </div>
              <div className="text-xs text-gray-500 mt-2">
                {dateRange} days
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-sm p-6">
              <div className="text-sm text-gray-600 mb-1">Average ROAS</div>
              <div className="text-3xl font-bold text-blue-600">
                {overview.metrics?.average_roas?.toFixed(2) || '0.00'}x
              </div>
              <div className="text-xs text-gray-500 mt-2">
                Return on ad spend
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-sm p-6">
              <div className="text-sm text-gray-600 mb-1">Conversions</div>
              <div className="text-3xl font-bold text-purple-600">
                {overview.metrics?.total_conversions || 0}
              </div>
              <div className="text-xs text-gray-500 mt-2">
                {dateRange} days
              </div>
            </div>
          </div>
        )}

        {/* Charts */}
        <div className="space-y-6">
          {/* Revenue vs Cost */}
          <div className="bg-white rounded-xl shadow-sm p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Revenue vs Cost</h2>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="revenue" stroke="#10b981" strokeWidth={2} name="Revenue" />
                <Line type="monotone" dataKey="cost" stroke="#ef4444" strokeWidth={2} name="Cost" />
              </LineChart>
            </ResponsiveContainer>
          </div>

          {/* ROAS Trend */}
          <div className="bg-white rounded-xl shadow-sm p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">ROAS Trend</h2>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="roas" stroke="#3b82f6" strokeWidth={2} name="ROAS" />
              </LineChart>
            </ResponsiveContainer>
          </div>

          {/* Impressions & Clicks */}
          <div className="bg-white rounded-xl shadow-sm p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Impressions & Clicks</h2>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="impressions" fill="#8b5cf6" name="Impressions" />
                <Bar dataKey="clicks" fill="#06b6d4" name="Clicks" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Conversions */}
          <div className="bg-white rounded-xl shadow-sm p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Daily Conversions</h2>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="conversions" fill="#f59e0b" name="Conversions" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Export Section */}
        <div className="mt-8 bg-white rounded-xl shadow-sm p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Export Reports</h2>
          <div className="flex gap-4">
            <button className="px-6 py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition-colors">
              Export CSV
            </button>
            <button className="px-6 py-3 bg-green-600 text-white rounded-lg font-semibold hover:bg-green-700 transition-colors">
              Export PDF
            </button>
            <button className="px-6 py-3 bg-purple-600 text-white rounded-lg font-semibold hover:bg-purple-700 transition-colors">
              Schedule Report
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
