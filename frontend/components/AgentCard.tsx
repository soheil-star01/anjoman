import { AgentConfig } from '@/types'
import { Bot } from 'lucide-react'

interface AgentCardProps {
  agent: AgentConfig
}

export default function AgentCard({ agent }: AgentCardProps) {
  return (
    <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
      <div className="flex items-start space-x-3">
        <div className="bg-blue-100 p-2 rounded-lg">
          <Bot className="w-5 h-5 text-blue-600" />
        </div>
        
        <div className="flex-1 min-w-0">
          <div className="flex items-center space-x-2 mb-1">
            <span className="text-sm font-semibold text-gray-900">{agent.id}</span>
            <span className="text-xs text-gray-500">·</span>
            <span className="text-sm text-gray-700">{agent.role}</span>
          </div>
          
          <div className="text-xs text-gray-600 mb-2">{agent.model}</div>
          
          {agent.style && (
            <div className="text-xs text-gray-500 italic mb-2">{agent.style}</div>
          )}
          
          <div className="flex items-center justify-between text-xs">
            <span className="text-gray-600">
              {agent.tokens_in + agent.tokens_out} tokens
            </span>
            <span className="font-medium text-blue-600">
              ${agent.cost_used.toFixed(4)}
            </span>
          </div>
        </div>
      </div>
    </div>
  )
}

