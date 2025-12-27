'use client'

import { useState, useEffect } from 'react'
import { MessageSquare, Plus, History, Key } from 'lucide-react'
import NewSessionForm from '@/components/NewSessionForm'
import SessionView from '@/components/SessionView'
import SessionList from '@/components/SessionList'
import ApiKeySettings, { ApiKeys } from '@/components/ApiKeySettings'
import CostDisclaimer from '@/components/CostDisclaimer'
import { Session, SessionListItem } from '@/types'
import { api } from '@/lib/api'

export default function Home() {
  const [view, setView] = useState<'new' | 'session' | 'list'>('new')
  const [currentSession, setCurrentSession] = useState<Session | null>(null)
  const [sessions, setSessions] = useState<SessionListItem[]>([])
  const [showApiKeys, setShowApiKeys] = useState(false)
  const [apiKeys, setApiKeys] = useState<ApiKeys>({})

  useEffect(() => {
    loadSessions()
    // Load API keys from localStorage
    const stored = localStorage.getItem('anjoman_api_keys')
    if (stored) {
      setApiKeys(JSON.parse(stored))
    } else {
      // Show API key modal on first visit
      setShowApiKeys(true)
    }
  }, [])

  const handleSaveApiKeys = (keys: ApiKeys) => {
    setApiKeys(keys)
    localStorage.setItem('anjoman_api_keys', JSON.stringify(keys))
  }

  const loadSessions = async () => {
    try {
      const data = await api.listSessions()
      setSessions(data)
    } catch (error) {
      console.error('Error loading sessions:', error)
    }
  }

  const handleNewSession = async (session: Session) => {
    setCurrentSession(session)
    setView('session')
    await loadSessions()
  }

  const handleLoadSession = async (sessionId: string) => {
    try {
      const session = await api.getSession(sessionId)
      setCurrentSession(session)
      setView('session')
    } catch (error) {
      console.error('Error loading session:', error)
    }
  }

  const handleBackToNew = () => {
    setCurrentSession(null)
    setView('new')
  }

  const handleShowList = () => {
    setView('list')
    loadSessions()
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <MessageSquare className="w-8 h-8 text-blue-600" />
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Anjoman</h1>
                <p className="text-sm text-gray-500">Structured Multi-LLM Deliberation</p>
              </div>
            </div>
            
            <div className="flex space-x-2">
              <button
                onClick={() => setShowApiKeys(true)}
                className="flex items-center space-x-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition"
              >
                <Key className="w-4 h-4" />
                <span>API Keys</span>
              </button>
              
              <button
                onClick={handleBackToNew}
                className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
              >
                <Plus className="w-4 h-4" />
                <span>New Session</span>
              </button>
              
              <button
                onClick={handleShowList}
                className="flex items-center space-x-2 px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition"
              >
                <History className="w-4 h-4" />
                <span>History</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {view === 'new' && (
          <>
            <NewSessionForm onSessionCreated={handleNewSession} apiKeys={apiKeys} />
            <div className="max-w-3xl mx-auto mt-4">
              <CostDisclaimer />
            </div>
          </>
        )}
        
        {view === 'session' && currentSession && (
          <SessionView 
            session={currentSession} 
            onSessionUpdate={setCurrentSession}
            apiKeys={apiKeys}
          />
        )}
        
        {view === 'list' && (
          <SessionList 
            sessions={sessions} 
            onSelectSession={handleLoadSession}
            onRefresh={loadSessions}
          />
        )}
      </div>

      {/* API Key Settings Modal */}
      {showApiKeys && (
        <ApiKeySettings
          currentKeys={apiKeys}
          onSave={handleSaveApiKeys}
          onClose={() => setShowApiKeys(false)}
        />
      )}
    </main>
  )
}

