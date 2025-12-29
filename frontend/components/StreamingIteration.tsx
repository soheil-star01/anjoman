'use client'

import { useState, useEffect } from 'react'
import { AgentMessage } from '@/types'
import { Loader2, MessageSquare, Sparkles, AlertTriangle } from 'lucide-react'
import ReactMarkdown from 'react-markdown'

interface StreamingIterationProps {
  messages: AgentMessage[]
  currentAgent?: { id: string; role: string }
  isSummarizing?: boolean
  totalAgents: number
}

export default function StreamingIteration({
  messages,
  currentAgent,
  isSummarizing,
  totalAgents
}: StreamingIterationProps) {
  return (
    <div className="bg-white rounded-xl shadow-lg p-6 space-y-4">
      <div className="flex items-center justify-between border-b pb-3">
        <h3 className="text-lg font-semibold text-gray-900">
          Discussion in Progress
        </h3>
        <div className="text-sm text-gray-500">
          {messages.length} / {totalAgents} agents responded
        </div>
      </div>

      {/* Messages */}
      <div className="space-y-4">
        {messages.map((message, idx) => {
          const isError = message.content.startsWith('[Error:')
          const borderColor = isError ? 'border-red-400' : 'border-blue-400'
          const bgColor = isError ? 'bg-red-50' : 'bg-blue-50'
          const iconColor = isError ? 'text-red-600' : 'text-blue-600'
          
          return (
            <div
              key={idx}
              className={`border-l-4 ${borderColor} pl-4 py-2 ${bgColor} rounded-r-lg animate-fadeIn`}
            >
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center space-x-2">
                  {isError ? (
                    <AlertTriangle className={`w-4 h-4 ${iconColor}`} />
                  ) : (
                    <MessageSquare className={`w-4 h-4 ${iconColor}`} />
                  )}
                  <span className="font-semibold text-gray-900">{message.agent_role}</span>
                  <span className="text-xs text-gray-500">({message.agent_id})</span>
                  {isError && (
                    <span className="text-xs font-semibold text-red-600 bg-red-100 px-2 py-0.5 rounded">
                      Error
                    </span>
                  )}
                </div>
                <div className="flex items-center space-x-3 text-xs text-gray-500">
                  <span className="font-semibold text-gray-700">
                    {(message.tokens_in + message.tokens_out).toLocaleString()} tokens
                  </span>
                  {message.cost > 0 && (
                    <span className="font-medium text-blue-600">
                      ≈ ${message.cost.toFixed(4)}
                    </span>
                  )}
                </div>
              </div>
              <div className="prose prose-sm max-w-none">
                <ReactMarkdown>{message.content}</ReactMarkdown>
              </div>
            </div>
          )
        })}
      </div>

      {/* Current Agent Speaking */}
      {currentAgent && !isSummarizing && (
        <div className="flex items-center space-x-3 p-4 bg-blue-50 border-2 border-blue-200 rounded-lg">
          <Loader2 className="w-5 h-5 text-blue-600 animate-spin" />
          <div>
            <p className="text-sm font-medium text-gray-900">
              {currentAgent.role} ({currentAgent.id}) is thinking...
            </p>
            <p className="text-xs text-gray-500">Generating response</p>
          </div>
        </div>
      )}

      {/* Summarizing */}
      {isSummarizing && (
        <div className="flex items-center space-x-3 p-4 bg-amber-50 border-2 border-amber-200 rounded-lg">
          <Sparkles className="w-5 h-5 text-amber-600 animate-pulse" />
          <div>
            <p className="text-sm font-medium text-gray-900">
              Dana is summarizing the discussion...
            </p>
            <p className="text-xs text-gray-500">Creating insights and suggestions</p>
          </div>
        </div>
      )}
    </div>
  )
}

