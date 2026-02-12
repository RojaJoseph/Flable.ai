'use client'

import { useState } from 'react'
import api from '@/lib/api'

export default function AuthDebugPage() {
  const [results, setResults] = useState<any>({})
  const [loading, setLoading] = useState(false)

  const runFullTest = async () => {
    setLoading(true)
    const testResults: any = {}

    try {
      // Step 1: Check backend health
      testResults.step1 = { status: 'running', title: 'Backend Health Check' }
      setResults({ ...testResults })
      
      const healthCheck = await fetch('http://localhost:8000/health')
      const healthData = await healthCheck.json()
      testResults.step1 = { 
        status: 'success', 
        title: 'Backend Health Check',
        data: healthData 
      }
      setResults({ ...testResults })

      // Step 2: Clear old tokens
      testResults.step2 = { status: 'running', title: 'Clear Old Tokens' }
      setResults({ ...testResults })
      
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      testResults.step2 = { status: 'success', title: 'Clear Old Tokens' }
      setResults({ ...testResults })

      // Step 3: Login
      testResults.step3 = { status: 'running', title: 'Attempt Login' }
      setResults({ ...testResults })
      
      const loginResponse = await api.post('/auth/login', {
        email: 'admin@flable.ai',
        password: 'admin123'
      })
      
      const { access_token, refresh_token } = loginResponse.data
      localStorage.setItem('access_token', access_token)
      localStorage.setItem('refresh_token', refresh_token)
      
      testResults.step3 = { 
        status: 'success', 
        title: 'Login',
        data: {
          access_token: access_token.substring(0, 50) + '...',
          refresh_token: refresh_token.substring(0, 50) + '...'
        }
      }
      setResults({ ...testResults })

      // Step 4: Test /auth/me
      testResults.step4 = { status: 'running', title: 'Test /auth/me' }
      setResults({ ...testResults })
      
      const meResponse = await api.get('/auth/me')
      testResults.step4 = { 
        status: 'success', 
        title: 'Auth Me Request',
        data: meResponse.data
      }
      setResults({ ...testResults })

      // Step 5: Test debug token endpoint
      testResults.step5 = { status: 'running', title: 'Debug Token Endpoint' }
      setResults({ ...testResults })
      
      const debugResponse = await api.get('/auth/debug/token')
      testResults.step5 = { 
        status: 'success', 
        title: 'Debug Token',
        data: debugResponse.data
      }
      setResults({ ...testResults })

      // Step 6: Test dashboard
      testResults.step6 = { status: 'running', title: 'Test Dashboard' }
      setResults({ ...testResults })
      
      const dashboardResponse = await api.get('/dashboard')
      testResults.step6 = { 
        status: 'success', 
        title: 'Dashboard Request',
        data: dashboardResponse.data
      }
      setResults({ ...testResults })

    } catch (error: any) {
      const failedStep = Object.keys(testResults).filter(k => testResults[k].status === 'running')[0]
      if (failedStep) {
        testResults[failedStep] = {
          ...testResults[failedStep],
          status: 'error',
          error: error.response?.data || error.message
        }
      }
      setResults({ ...testResults })
    }

    setLoading(false)
  }

  const testDirectFetch = async () => {
    const token = localStorage.getItem('access_token')
    
    if (!token) {
      alert('No token found. Run full test first.')
      return
    }

    try {
      const response = await fetch('http://localhost:8000/api/v1/dashboard', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })

      const data = await response.json()
      
      setResults({
        ...results,
        directFetch: {
          status: response.ok ? 'success' : 'error',
          title: 'Direct Fetch Test',
          statusCode: response.status,
          data: data
        }
      })
    } catch (error: any) {
      setResults({
        ...results,
        directFetch: {
          status: 'error',
          title: 'Direct Fetch Test',
          error: error.message
        }
      })
    }
  }

  const clearTokens = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    setResults({})
    alert('Tokens cleared!')
  }

  const checkTokens = () => {
    const access = localStorage.getItem('access_token')
    const refresh = localStorage.getItem('refresh_token')
    
    setResults({
      ...results,
      tokenCheck: {
        status: 'info',
        title: 'Current Tokens',
        data: {
          hasAccessToken: !!access,
          hasRefreshToken: !!refresh,
          accessPreview: access ? access.substring(0, 50) + '...' : null,
          refreshPreview: refresh ? refresh.substring(0, 50) + '...' : null
        }
      }
    })
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">🔧 Flable.ai Debug Tool</h1>

        {/* Control Buttons */}
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4">🧪 Test Controls</h2>
          <div className="flex flex-wrap gap-3">
            <button
              onClick={runFullTest}
              disabled={loading}
              className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
            >
              {loading ? 'Testing...' : '▶️ Run Full Test'}
            </button>
            
            <button
              onClick={testDirectFetch}
              className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
            >
              🎯 Test Direct Fetch
            </button>

            <button
              onClick={checkTokens}
              className="px-4 py-2 bg-purple-600 text-white rounded hover:bg-purple-700"
            >
              🔍 Check Tokens
            </button>
            
            <button
              onClick={clearTokens}
              className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
            >
              🗑️ Clear Tokens
            </button>
          </div>
        </div>

        {/* Results */}
        <div className="space-y-4">
          {Object.entries(results).map(([key, result]: [string, any]) => (
            <div
              key={key}
              className={`bg-white rounded-lg shadow p-6 border-l-4 ${
                result.status === 'success'
                  ? 'border-green-500'
                  : result.status === 'error'
                  ? 'border-red-500'
                  : result.status === 'running'
                  ? 'border-yellow-500'
                  : 'border-blue-500'
              }`}
            >
              <h3 className="text-lg font-semibold mb-2">
                {result.status === 'success' && '✅ '}
                {result.status === 'error' && '❌ '}
                {result.status === 'running' && '⏳ '}
                {result.status === 'info' && 'ℹ️ '}
                {result.title}
              </h3>

              {result.data && (
                <div className="mt-3">
                  <pre className="bg-gray-50 p-3 rounded overflow-x-auto text-sm">
                    {JSON.stringify(result.data, null, 2)}
                  </pre>
                </div>
              )}

              {result.error && (
                <div className="mt-3 p-3 bg-red-50 rounded text-red-800">
                  <strong>Error:</strong>
                  <pre className="mt-2 text-sm overflow-x-auto">
                    {JSON.stringify(result.error, null, 2)}
                  </pre>
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Instructions */}
        {Object.keys(results).length === 0 && (
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
            <h3 className="text-lg font-semibold mb-2">📖 How to use:</h3>
            <ol className="list-decimal list-inside space-y-2">
              <li>Click "Run Full Test" to test complete auth flow</li>
              <li>Check results to see where it fails</li>
              <li>Use "Test Direct Fetch" to test dashboard endpoint directly</li>
              <li>Use "Check Tokens" to see current token state</li>
              <li>Use "Clear Tokens" to reset and start fresh</li>
            </ol>
          </div>
        )}
      </div>
    </div>
  )
}
