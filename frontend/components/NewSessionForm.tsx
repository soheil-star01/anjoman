'use client'

import { useState } from 'react'
import { Loader2, Sparkles } from 'lucide-react'
import { api } from '@/lib/api'
import { Session, SessionProposal, AgentConfig } from '@/types'
import { ApiKeys } from './ApiKeySettings'
import AgentReview from './AgentReview'

interface NewSessionFormProps {
  onSessionCreated: (session: Session) => void
  apiKeys: ApiKeys
}

export default function NewSessionForm({ onSessionCreated, apiKeys }: NewSessionFormProps) {
  const [issue, setIssue] = useState('')
  const [budget, setBudget] = useState('5.00')
  const [numAgents, setNumAgents] = useState('')
  const [modelPreference, setModelPreference] = useState<string>('balanced')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [proposal, setProposal] = useState<SessionProposal | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    
    // Check if at least one API key is provided
    const hasApiKey = !!(apiKeys.openai_api_key || apiKeys.anthropic_api_key || 
                         apiKeys.mistral_api_key || apiKeys.google_api_key || apiKeys.cohere_api_key)
    
    if (!hasApiKey) {
      setError('Please add at least one API key in the API Keys settings')
      return
    }
    
    setLoading(true)

    try {
      // First get Dana's proposal
      const proposalData = await api.proposeAgents(
        issue, 
        parseFloat(budget), 
        numAgents ? parseInt(numAgents) : null,  // null means Dana decides
        modelPreference,
        apiKeys
      )
      setProposal(proposalData)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to get agent proposal')
    } finally {
      setLoading(false)
    }
  }

  const handleConfirmAgents = async (confirmedAgents: AgentConfig[]) => {
    setLoading(true)
    try {
      const session = await api.createSession({
        issue,
        budget: parseFloat(budget),
        suggested_agents: confirmedAgents,
        api_keys: apiKeys,
      })
      onSessionCreated(session)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create session')
      setProposal(null)
    } finally {
      setLoading(false)
    }
  }

  const handleCancelReview = () => {
    setProposal(null)
  }

  return (
    <>
      {proposal && (
        <AgentReview
          proposedAgents={proposal.proposed_agents}
          availableModels={proposal.available_models}
          rationale={proposal.rationale}
          onConfirm={handleConfirmAgents}
          onCancel={handleCancelReview}
        />
      )}
      
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

          {/* Model Preference Slider */}
          <div>
            <label htmlFor="modelPreference" className="block text-sm font-medium text-gray-700 mb-2">
              Model Selection Preference
            </label>
            <div className="space-y-2">
              <input
                id="modelPreference"
                type="range"
                min="0"
                max="2"
                step="1"
                value={modelPreference === 'budget' ? 0 : modelPreference === 'balanced' ? 1 : 2}
                onChange={(e) => {
                  const val = parseInt(e.target.value)
                  setModelPreference(val === 0 ? 'budget' : val === 1 ? 'balanced' : 'performance')
                }}
                className="w-full h-2 bg-gradient-to-r from-green-500 via-blue-500 to-purple-500 rounded-lg appearance-none cursor-pointer"
                style={{
                  WebkitAppearance: 'none',
                }}
              />
              <div className="flex justify-between text-xs text-gray-600">
                <span className={modelPreference === 'budget' ? 'font-semibold text-green-600' : ''}>
                  💰 Budget-Friendly
                </span>
                <span className={modelPreference === 'balanced' ? 'font-semibold text-blue-600' : ''}>
                  ⚖️ Balanced
                </span>
                <span className={modelPreference === 'performance' ? 'font-semibold text-purple-600' : ''}>
                  🚀 Max Performance
                </span>
              </div>
            </div>
            <p className="mt-2 text-sm text-gray-500">
              {modelPreference === 'budget' && 'Economical models (GPT-3.5, Claude Haiku, etc.)'}
              {modelPreference === 'balanced' && 'Mid-tier models (GPT-4o, Claude Sonnet, etc.)'}
              {modelPreference === 'performance' && 'Most capable models (GPT-5.1, Claude Opus 4.5, etc.)'}
            </p>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label htmlFor="numAgents" className="block text-sm font-medium text-gray-700 mb-2">
                Number of Agents (Optional)
              </label>
              <input
                id="numAgents"
                type="number"
                min="2"
                max="8"
                value={numAgents}
                onChange={(e) => setNumAgents(e.target.value)}
                placeholder="Let Dana decide"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <p className="mt-2 text-sm text-gray-500">
                Leave empty for Dana to decide
              </p>
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
                Session budget limit
              </p>
            </div>
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
    </>
  )
}

