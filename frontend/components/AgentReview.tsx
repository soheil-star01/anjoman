'use client'

import { useState } from 'react'
import { Bot, Check, Edit2, X } from 'lucide-react'
import { AgentConfig, ModelInfo } from '@/types'

interface AgentReviewProps {
  proposedAgents: AgentConfig[]
  availableModels: ModelInfo[]
  rationale: string
  onConfirm: (agents: AgentConfig[]) => void
  onCancel: () => void
}

export default function AgentReview({
  proposedAgents,
  availableModels,
  rationale,
  onConfirm,
  onCancel,
}: AgentReviewProps) {
  const [agents, setAgents] = useState<AgentConfig[]>(proposedAgents)
  const [editingIndex, setEditingIndex] = useState<number | null>(null)

  const handleModelChange = (index: number, newModel: string) => {
    const updated = [...agents]
    updated[index] = { ...updated[index], model: newModel }
    setAgents(updated)
  }

  const handleRoleChange = (index: number, newRole: string) => {
    const updated = [...agents]
    updated[index] = { ...updated[index], role: newRole }
    setAgents(updated)
  }

  const handleStyleChange = (index: number, newStyle: string) => {
    const updated = [...agents]
    updated[index] = { ...updated[index], style: newStyle }
    setAgents(updated)
  }

  const getModelInfo = (modelId: string) => {
    return availableModels.find(m => m.model_id === modelId)
  }

  // Group models by provider for dropdown
  const modelsByProvider = availableModels.reduce((acc, model) => {
    if (!acc[model.provider]) {
      acc[model.provider] = []
    }
    acc[model.provider].push(model)
    return acc
  }, {} as Record<string, ModelInfo[]>)

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-xl shadow-2xl max-w-4xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="bg-gradient-to-r from-purple-600 to-indigo-600 px-6 py-4">
          <h2 className="text-2xl font-bold text-white">Review Agent Configuration</h2>
          <p className="text-purple-100 text-sm mt-1">
            Review and customize your deliberation council before starting
          </p>
        </div>

        {/* Rationale */}
        <div className="p-6 border-b bg-blue-50">
          <h3 className="font-semibold text-gray-900 mb-2">Dana&apos;s Rationale</h3>
          <p className="text-gray-700">{rationale}</p>
        </div>

        {/* Agents */}
        <div className="p-6 space-y-4">
          <h3 className="font-semibold text-gray-900 mb-4">Proposed Agents</h3>
          
          {agents.map((agent, index) => {
            const modelInfo = getModelInfo(agent.model)
            const isEditing = editingIndex === index

            return (
              <div key={agent.id} className="border border-gray-200 rounded-lg p-4 hover:border-blue-300 transition">
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center space-x-3">
                    <div className="bg-blue-100 p-2 rounded-lg">
                      <Bot className="w-6 h-6 text-blue-600" />
                    </div>
                    <div>
                      {isEditing ? (
                        <input
                          type="text"
                          value={agent.role}
                          onChange={(e) => handleRoleChange(index, e.target.value)}
                          className="text-lg font-semibold border-b-2 border-blue-500 focus:outline-none"
                        />
                      ) : (
                        <h4 className="text-lg font-semibold text-gray-900">{agent.role}</h4>
                      )}
                      <p className="text-sm text-gray-500">{agent.id}</p>
                    </div>
                  </div>
                  
                  <button
                    onClick={() => setEditingIndex(isEditing ? null : index)}
                    className="p-2 hover:bg-gray-100 rounded-lg transition"
                  >
                    {isEditing ? (
                      <Check className="w-5 h-5 text-green-600" />
                    ) : (
                      <Edit2 className="w-5 h-5 text-gray-600" />
                    )}
                  </button>
                </div>

                {/* Style */}
                {agent.style && (
                  <div className="mb-3">
                    <label className="text-xs font-medium text-gray-600 block mb-1">Style</label>
                    {isEditing ? (
                      <input
                        type="text"
                        value={agent.style}
                        onChange={(e) => handleStyleChange(index, e.target.value)}
                        className="w-full px-3 py-1 text-sm border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        placeholder="e.g., data-driven, skeptical, creative"
                      />
                    ) : (
                      <p className="text-sm text-gray-700 italic">{agent.style}</p>
                    )}
                  </div>
                )}

                {/* Model Selection */}
                <div>
                  <label className="text-xs font-medium text-gray-600 block mb-1">Model</label>
                  {isEditing ? (
                    <select
                      value={agent.model}
                      onChange={(e) => handleModelChange(index, e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    >
                      {Object.entries(modelsByProvider).map(([provider, models]) => (
                        <optgroup key={provider} label={provider.toUpperCase()}>
                          {models.map((model) => (
                            <option key={model.model_id} value={model.model_id}>
                              {model.display_name} {model.description && `- ${model.description}`}
                            </option>
                          ))}
                        </optgroup>
                      ))}
                    </select>
                  ) : (
                    <div className="bg-gray-50 px-3 py-2 rounded-lg">
                      <p className="font-medium text-gray-900">{modelInfo?.display_name || agent.model}</p>
                      {modelInfo?.description && (
                        <p className="text-xs text-gray-600 mt-1">{modelInfo.description}</p>
                      )}
                      <p className="text-xs text-gray-500 mt-1">Provider: {modelInfo?.provider || 'Unknown'}</p>
                    </div>
                  )}
                </div>
              </div>
            )
          })}
        </div>

        {/* Actions */}
        <div className="border-t bg-gray-50 px-6 py-4 flex justify-between items-center">
          <p className="text-sm text-gray-600">
            {agents.length} {agents.length === 1 ? 'agent' : 'agents'} configured
          </p>
          <div className="flex space-x-3">
            <button
              onClick={onCancel}
              className="flex items-center space-x-2 px-6 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition"
            >
              <X className="w-4 h-4" />
              <span>Cancel</span>
            </button>
            <button
              onClick={() => onConfirm(agents)}
              className="flex items-center space-x-2 px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition"
            >
              <Check className="w-5 h-5" />
              <span>Start Deliberation</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

