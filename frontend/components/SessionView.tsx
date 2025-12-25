'use client'

import { useState } from 'react'
import { Session } from '@/types'
import { Loader2, Play, CheckCircle, AlertCircle } from 'lucide-react'
import { api } from '@/lib/api'
import AgentCard from './AgentCard'
import IterationView from './IterationView'
import BudgetDisplay from './BudgetDisplay'

interface SessionViewProps {
  session: Session
  onSessionUpdate: (session: Session) => void
}

export default function SessionView({ session, onSessionUpdate }: SessionViewProps) {
  const [loading, setLoading] = useState(false)
  const [userGuidance, setUserGuidance] = useState('')
  const [error, setError] = useState('')

  const handleIterate = async () => {
    setError('')
    setLoading(true)

    try {
      const updatedSession = await api.iterateSession(session.session_id, {
        session_id: session.session_id,
        user_guidance: userGuidance || undefined,
        accept_suggestion: true,
      })
      onSessionUpdate(updatedSession)
      setUserGuidance('')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to iterate session')
    } finally {
      setLoading(false)
    }
  }

  const handleComplete = async () => {
    try {
      await api.completeSession(session.session_id)
      const updatedSession = { ...session, status: 'completed' as const }
      onSessionUpdate(updatedSession)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to complete session')
    }
  }

  const isActive = session.status === 'active'
  const isBudgetExceeded = session.budget.used >= session.budget.total_budget
  const canContinue = isActive && !isBudgetExceeded

  return (
    <div className="space-y-6">
      {/* Session Header */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <div className="flex items-start justify-between mb-4">
          <div className="flex-1">
            <div className="flex items-center space-x-3 mb-2">
              <h2 className="text-2xl font-bold text-gray-900">Session {session.session_id}</h2>
              <StatusBadge status={session.status} />
            </div>
            <p className="text-gray-700 text-lg">{session.issue}</p>
          </div>
          
          <BudgetDisplay budget={session.budget} />
        </div>

        {/* Agents */}
        <div className="border-t pt-4 mt-4">
          <h3 className="text-sm font-semibold text-gray-700 mb-3">Council Members</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            {session.agents.map((agent) => (
              <AgentCard key={agent.id} agent={agent} />
            ))}
          </div>
        </div>
      </div>

      {/* Iterations */}
      <div className="space-y-4">
        {session.iterations.map((iteration) => (
          <IterationView key={iteration.iteration_number} iteration={iteration} />
        ))}
      </div>

      {/* Continue or Complete */}
      {isActive && (
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            {session.iterations.length === 0 ? 'Start Discussion' : 'Continue Discussion'}
          </h3>

          <div className="space-y-4">
            <div>
              <label htmlFor="guidance" className="block text-sm font-medium text-gray-700 mb-2">
                Your Guidance (Optional)
              </label>
              <textarea
                id="guidance"
                value={userGuidance}
                onChange={(e) => setUserGuidance(e.target.value)}
                rows={3}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                placeholder="Provide direction, ask for clarification, or let the agents continue..."
              />
            </div>

            {error && (
              <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg flex items-start space-x-2">
                <AlertCircle className="w-5 h-5 flex-shrink-0 mt-0.5" />
                <span>{error}</span>
              </div>
            )}

            {session.budget.used >= (session.budget.total_budget * session.budget.warning_threshold) && !isBudgetExceeded && (
              <div className="bg-yellow-50 border border-yellow-200 text-yellow-800 px-4 py-3 rounded-lg flex items-start space-x-2">
                <AlertCircle className="w-5 h-5 flex-shrink-0 mt-0.5" />
                <span>
                  Budget warning: ${session.budget.used.toFixed(2)} / ${session.budget.total_budget.toFixed(2)} used
                </span>
              </div>
            )}

            <div className="flex space-x-3">
              <button
                onClick={handleIterate}
                disabled={loading || !canContinue}
                className="flex-1 flex items-center justify-center space-x-2 px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition"
              >
                {loading ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    <span>Processing...</span>
                  </>
                ) : (
                  <>
                    <Play className="w-5 h-5" />
                    <span>Next Iteration</span>
                  </>
                )}
              </button>

              <button
                onClick={handleComplete}
                disabled={loading}
                className="flex items-center space-x-2 px-6 py-3 bg-green-600 text-white font-medium rounded-lg hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition"
              >
                <CheckCircle className="w-5 h-5" />
                <span>Complete</span>
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

function StatusBadge({ status }: { status: Session['status'] }) {
  const styles = {
    active: 'bg-green-100 text-green-800',
    completed: 'bg-blue-100 text-blue-800',
    paused: 'bg-yellow-100 text-yellow-800',
    error: 'bg-red-100 text-red-800',
  }

  return (
    <span className={`px-3 py-1 rounded-full text-xs font-medium ${styles[status]}`}>
      {status.toUpperCase()}
    </span>
  )
}

