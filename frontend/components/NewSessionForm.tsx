'use client'

import { useState } from 'react'
import { Loader2, Sparkles } from 'lucide-react'
import { api } from '@/lib/api'
import { Session } from '@/types'

interface NewSessionFormProps {
  onSessionCreated: (session: Session) => void
}

export default function NewSessionForm({ onSessionCreated }: NewSessionFormProps) {
  const [issue, setIssue] = useState('')
  const [budget, setBudget] = useState('5.00')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const session = await api.createSession({
        issue,
        budget: parseFloat(budget),
      })
      onSessionCreated(session)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create session')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-3xl mx-auto">
      <div className="bg-white rounded-xl shadow-lg p-8">
        <div className="flex items-center space-x-3 mb-6">
          <Sparkles className="w-8 h-8 text-blue-600" />
          <h2 className="text-3xl font-bold text-gray-900">Start New Deliberation</h2>
        </div>

        <p className="text-gray-600 mb-6">
          Describe your issue or problem, and Dana will propose a council of expert agents to help you think through it.
        </p>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="issue" className="block text-sm font-medium text-gray-700 mb-2">
              Your Issue or Question
            </label>
            <textarea
              id="issue"
              value={issue}
              onChange={(e) => setIssue(e.target.value)}
              rows={6}
              required
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
              placeholder="E.g., 'Should we migrate our backend to microservices? We have a monolith with 100k LOC, 20 engineers, and tight deadlines.'"
            />
          </div>

          <div>
            <label htmlFor="budget" className="block text-sm font-medium text-gray-700 mb-2">
              Budget (USD)
            </label>
            <div className="relative">
              <span className="absolute left-4 top-3 text-gray-500">$</span>
              <input
                id="budget"
                type="number"
                step="0.01"
                min="0.50"
                max="100"
                value={budget}
                onChange={(e) => setBudget(e.target.value)}
                required
                className="w-full pl-8 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <p className="mt-2 text-sm text-gray-500">
              Set a budget for this deliberation session. You&apos;ll be warned before exceeding it.
            </p>
          </div>

          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full flex items-center justify-center space-x-2 px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition"
          >
            {loading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                <span>Creating Session...</span>
              </>
            ) : (
              <>
                <Sparkles className="w-5 h-5" />
                <span>Begin Deliberation</span>
              </>
            )}
          </button>
        </form>
      </div>

      {/* Info Card */}
      <div className="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-6">
        <h3 className="font-semibold text-blue-900 mb-2">How it works</h3>
        <ol className="space-y-2 text-sm text-blue-800">
          <li>1. Dana (the orchestrator) will propose 3-5 expert agents</li>
          <li>2. Each agent contributes their perspective in turn</li>
          <li>3. After each round, you&apos;ll see a summary and suggested direction</li>
          <li>4. You guide the next iteration or conclude the session</li>
        </ol>
      </div>
    </div>
  )
}

