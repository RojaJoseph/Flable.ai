'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import api from '@/lib/api'
import toast from 'react-hot-toast'

export default function NewCampaignPage() {
    const router = useRouter()
    const [loading, setLoading] = useState(false)
    const [formData, setFormData] = useState({
        name: '',
        description: '',
        platform: 'shopify',
        daily_budget: 50,
        target_roas: 3.0,
        target_cpa: 50,
        status: 'active'
    })

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setLoading(true)

        try {
            const token = localStorage.getItem('access_token')
            if (!token) {
                router.push('/login')
                return
            }

            // Prepare payload
            const payload = {
                ...formData,
                total_budget: formData.daily_budget * 30, // Auto-calc monthly budget
                ai_enabled: true
            }

            await api.post('/campaigns/', payload, {
                headers: { Authorization: `Bearer ${token}` }
            })

            toast.success('Campaign created successfully!')
            router.push('/dashboard')
        } catch (error: any) {
            console.error('Error creating campaign:', error)
            toast.error(error.response?.data?.detail || 'Failed to create campaign')
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="min-h-screen bg-gray-50 py-8">
            <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8">
                {/* Header */}
                <div className="mb-8">
                    <Link href="/dashboard" className="text-blue-600 hover:text-blue-800 mb-2 inline-block">
                        ← Back to Dashboard
                    </Link>
                    <h1 className="text-3xl font-bold text-gray-900">Create New Campaign</h1>
                    <p className="text-gray-600 mt-2">Launch an AI-optimized marketing campaign</p>
                </div>

                {/* Form */}
                <div className="bg-white rounded-xl shadow-sm p-6 sm:p-8">
                    <form onSubmit={handleSubmit} className="space-y-6">

                        {/* Campaign Name */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">
                                Campaign Name
                            </label>
                            <input
                                type="text"
                                required
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                placeholder="e.g., Summer Sale 2024"
                                value={formData.name}
                                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                            />
                        </div>

                        {/* Platform */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">
                                Platform
                            </label>
                            <select
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                value={formData.platform}
                                onChange={(e) => setFormData({ ...formData, platform: e.target.value })}
                            >
                                <option value="shopify">Shopify</option>
                                <option value="google">Google Ads</option>
                                <option value="facebook">Facebook / Meta</option>
                                <option value="tiktok">TikTok Ads</option>
                            </select>
                        </div>

                        {/* Budget & ROAS */}
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">
                                    Daily Budget ($)
                                </label>
                                <input
                                    type="number"
                                    min="1"
                                    required
                                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                    value={formData.daily_budget}
                                    onChange={(e) => setFormData({ ...formData, daily_budget: parseFloat(e.target.value) })}
                                />
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">
                                    Target ROAS (x)
                                </label>
                                <input
                                    type="number"
                                    min="0.1"
                                    step="0.1"
                                    required
                                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                    value={formData.target_roas}
                                    onChange={(e) => setFormData({ ...formData, target_roas: parseFloat(e.target.value) })}
                                />
                            </div>
                        </div>

                        {/* Description */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">
                                Description (Optional)
                            </label>
                            <textarea
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                rows={3}
                                placeholder="Describe your campaign goals..."
                                value={formData.description}
                                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                            />
                        </div>

                        {/* AI Optimization Notice */}
                        <div className="bg-blue-50 border border-blue-100 rounded-lg p-4 flex items-start">
                            <div className="text-2xl mr-3">🤖</div>
                            <div>
                                <h4 className="font-semibold text-blue-900">AI Optimization Enabled</h4>
                                <p className="text-sm text-blue-700">
                                    Our machine learning engine will automatically optimize your budget allocation
                                    to maximize ROAS based on real-time performance data.
                                </p>
                            </div>
                        </div>

                        {/* Submit Button */}
                        <div className="pt-4">
                            <button
                                type="submit"
                                disabled={loading}
                                className={`w-full py-3 px-6 text-white font-semibold rounded-lg shadow-md transition-colors ${loading
                                    ? 'bg-blue-400 cursor-not-allowed'
                                    : 'bg-blue-600 hover:bg-blue-700'
                                    }`}
                            >
                                {loading ? 'Creating Campaign...' : 'Launch Campaign 🚀'}
                            </button>
                        </div>

                    </form>
                </div>
            </div>
        </div>
    )
}
