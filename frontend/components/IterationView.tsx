import { useState, useEffect } from 'react'
import { Iteration } from '@/types'
import { MessageSquare, Lightbulb, ChevronDown, ChevronRight, AlertTriangle } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import DirectionPicker from './DirectionPicker'

interface IterationViewProps {
  iteration: Iteration
  onSelectSuggestion?: (suggestion: string) => void
  isLatest?: boolean
  autoCollapsed?: boolean
}

export default function IterationView({ iteration, onSelectSuggestion, isLatest = false, autoCollapsed = false }: IterationViewProps) {
  const [isExpanded, setIsExpanded] = useState(!autoCollapsed)
  
  // Collapse when autoCollapsed becomes true
  useEffect(() => {
    if (autoCollapsed) {
      setIsExpanded(false)
    }
  }, [autoCollapsed])
  
  const totalTokens = iteration.messages.reduce((sum, m) => sum + m.tokens_in + m.tokens_out, 0)
  const totalCost = iteration.summary?.total_cost || 0

  return (
    <div className={`bg-white rounded-xl shadow-lg overflow-hidden ${!isExpanded ? 'hover:shadow-xl transition-shadow' : ''}`}>
      {/* Iteration Header - Always Visible, Clickable */}
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full bg-gradient-to-r from-blue-500 to-indigo-600 px-6 py-4 flex items-center justify-between hover:from-blue-600 hover:to-indigo-700 transition-all"
      >
        <div className="flex items-center space-x-3">
          {isExpanded ? (
            <ChevronDown className="w-5 h-5 text-white" />
          ) : (
            <ChevronRight className="w-5 h-5 text-white" />
          )}
          <div className="text-left">
            <h3 className="text-xl font-bold text-white">
              Iteration {iteration.iteration_number}
            </h3>
            {!isExpanded && iteration.user_guidance && (
              <p className="text-blue-100 text-xs mt-1">
                Guidance: {iteration.user_guidance}
              </p>
            )}
          </div>
          {!isExpanded && (
            <span className="text-sm text-blue-100">
              ({iteration.messages.length} responses)
            </span>
          )}
        </div>
        
        {!isExpanded && (
          <div className="flex items-center space-x-4 text-sm text-blue-100">
            <span>{totalTokens.toLocaleString()} tokens</span>
            {totalCost > 0 && <span>≈ ${totalCost.toFixed(4)}</span>}
          </div>
        )}
      </button>
      
      {/* Collapsible Content */}
      {isExpanded && (
        <>
          {iteration.user_guidance && (
            <div className="bg-blue-50 px-6 py-3 border-b border-blue-100">
              <p className="text-sm text-gray-700">
                <span className="font-semibold">Guidance:</span> {iteration.user_guidance}
              </p>
            </div>
          )}

          {/* Messages */}
          <div className="divide-y divide-gray-200">
            {iteration.messages.map((message, idx) => {
              const isError = message.content.startsWith('[Error:')
              
              return (
                <div key={idx} className={`p-6 ${isError ? 'bg-red-50' : ''}`}>
                  <div className="flex items-start space-x-4">
                    <div className={`${isError ? 'bg-red-100' : 'bg-blue-100'} p-2 rounded-lg flex-shrink-0`}>
                      {isError ? (
                        <AlertTriangle className="w-5 h-5 text-red-600" />
                      ) : (
                        <MessageSquare className="w-5 h-5 text-blue-600" />
                      )}
                    </div>
                    
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center space-x-2">
                          <span className="font-semibold text-gray-900">
                            {message.agent_id}
                          </span>
                          <span className="text-gray-500">·</span>
                          <span className="text-gray-700">{message.agent_role}</span>
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
                      
                      <div className="prose prose-sm max-w-none text-gray-800">
                        <ReactMarkdown className="markdown-content">
                          {message.content}
                        </ReactMarkdown>
                      </div>
                    </div>
                  </div>
                </div>
              )
            })}
          </div>

          {/* Summary */}
          {iteration.summary && (
            <div className="bg-amber-50 border-t-2 border-amber-200 p-6">
              <div className="flex items-start space-x-4">
                <div className="bg-amber-100 p-2 rounded-lg flex-shrink-0">
                  <Lightbulb className="w-5 h-5 text-amber-600" />
                </div>
                
                <div className="flex-1">
                  <h4 className="font-semibold text-gray-900 mb-2">Dana&apos;s Summary</h4>
                  
                  <div className="space-y-3 text-sm">
                    <div>
                      <span className="font-medium text-gray-700">Summary:</span>
                      <p className="text-gray-800 mt-1">{iteration.summary.summary}</p>
                    </div>
                    
                    {iteration.summary.key_disagreements && iteration.summary.key_disagreements.length > 0 && (
                      <div>
                        <span className="font-medium text-gray-700">Key Disagreements:</span>
                        <ul className="list-disc list-inside mt-1 space-y-1 text-gray-800">
                          {iteration.summary.key_disagreements.map((disagreement, idx) => (
                            <li key={idx}>{disagreement}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                    
                    <div>
                      <span className="font-medium text-gray-700 block mb-2">Suggested Directions:</span>
                      {onSelectSuggestion ? (
                        iteration.summary.suggested_directions && iteration.summary.suggested_directions.length > 0 ? (
                          <DirectionPicker 
                            directions={iteration.summary.suggested_directions}
                            onSelectDirection={onSelectSuggestion}
                          />
                        ) : iteration.summary.suggested_direction ? (
                          <p className="text-gray-800 mt-1 p-3 bg-amber-50 rounded-lg border border-amber-200">
                            {iteration.summary.suggested_direction}
                          </p>
                        ) : null
                      ) : (
                        iteration.summary.suggested_direction && (
                          <p className="text-gray-800 mt-1">{iteration.summary.suggested_direction}</p>
                        )
                      )}
                    </div>
                    
                    <div className="flex items-center justify-between pt-2 border-t border-amber-200">
                      <span className="text-gray-600">Iteration Tokens:</span>
                      <span className="font-semibold text-amber-700">
                        {iteration.messages.reduce((sum, m) => sum + m.tokens_in + m.tokens_out, 0).toLocaleString()}
                      </span>
                    </div>
                    {iteration.summary.total_cost > 0 && (
                      <div className="flex items-center justify-between text-xs">
                        <span className="text-gray-600">Estimated Cost:</span>
                        <span className="font-medium text-amber-600">
                          ≈ ${iteration.summary.total_cost.toFixed(4)}
                        </span>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  )
}
