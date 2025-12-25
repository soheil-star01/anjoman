import { Iteration } from '@/types'
import { MessageSquare, Lightbulb } from 'lucide-react'
import ReactMarkdown from 'react-markdown'

interface IterationViewProps {
  iteration: Iteration
}

export default function IterationView({ iteration }: IterationViewProps) {
  return (
    <div className="bg-white rounded-xl shadow-lg overflow-hidden">
      {/* Iteration Header */}
      <div className="bg-gradient-to-r from-blue-500 to-indigo-600 px-6 py-4">
        <h3 className="text-xl font-bold text-white">
          Iteration {iteration.iteration_number}
        </h3>
        {iteration.user_guidance && (
          <p className="text-blue-100 text-sm mt-1">
            Guidance: {iteration.user_guidance}
          </p>
        )}
      </div>

      {/* Messages */}
      <div className="divide-y divide-gray-200">
        {iteration.messages.map((message, idx) => (
          <div key={idx} className="p-6">
            <div className="flex items-start space-x-4">
              <div className="bg-blue-100 p-2 rounded-lg flex-shrink-0">
                <MessageSquare className="w-5 h-5 text-blue-600" />
              </div>
              
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center space-x-2">
                    <span className="font-semibold text-gray-900">
                      {message.agent_id}
                    </span>
                    <span className="text-gray-500">·</span>
                    <span className="text-gray-700">{message.agent_role}</span>
                  </div>
                  
                  <div className="flex items-center space-x-3 text-xs text-gray-500">
                    <span>{message.tokens_in + message.tokens_out} tokens</span>
                    <span className="font-medium text-blue-600">
                      ${message.cost.toFixed(4)}
                    </span>
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
        ))}
      </div>

      {/* Summary */}
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
                <span className="font-medium text-gray-700">Suggested Direction:</span>
                <p className="text-gray-800 mt-1">{iteration.summary.suggested_direction}</p>
              </div>
              
              <div className="flex items-center justify-between pt-2 border-t border-amber-200">
                <span className="text-gray-600">Iteration Cost:</span>
                <span className="font-semibold text-amber-700">
                  ${iteration.summary.total_cost.toFixed(4)}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

