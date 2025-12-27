'use client'

import { useState } from 'react'
import { Key, Eye, EyeOff, Save, X } from 'lucide-react'

interface ApiKeySettingsProps {
  onSave: (keys: ApiKeys) => void
  onClose: () => void
  currentKeys?: ApiKeys
}

export interface ApiKeys {
  openai_api_key?: string
  anthropic_api_key?: string
  mistral_api_key?: string
  google_api_key?: string
  cohere_api_key?: string
}

export default function ApiKeySettings({ onSave, onClose, currentKeys }: ApiKeySettingsProps) {
  const [keys, setKeys] = useState<ApiKeys>(currentKeys || {})
  const [showKeys, setShowKeys] = useState({
    openai: false,
    anthropic: false,
    mistral: false,
    google: false,
    cohere: false,
  })

  const handleSave = () => {
    // Filter out empty keys
    const filteredKeys: ApiKeys = {}
    if (keys.openai_api_key?.trim()) filteredKeys.openai_api_key = keys.openai_api_key.trim()
    if (keys.anthropic_api_key?.trim()) filteredKeys.anthropic_api_key = keys.anthropic_api_key.trim()
    if (keys.mistral_api_key?.trim()) filteredKeys.mistral_api_key = keys.mistral_api_key.trim()
    if (keys.google_api_key?.trim()) filteredKeys.google_api_key = keys.google_api_key.trim()
    if (keys.cohere_api_key?.trim()) filteredKeys.cohere_api_key = keys.cohere_api_key.trim()
    
    onSave(filteredKeys)
    onClose()
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-xl shadow-2xl max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        <div className="bg-gradient-to-r from-blue-600 to-indigo-600 px-6 py-4 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <Key className="w-6 h-6 text-white" />
            <h2 className="text-xl font-bold text-white">API Keys</h2>
          </div>
          <button onClick={onClose} className="text-white hover:bg-white/20 p-2 rounded-lg transition">
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="p-6 space-y-6">
          <p className="text-gray-600 text-sm">
            Your API keys are sent securely to the backend and are never stored permanently. 
            <strong> Add at least one API key</strong> to use Anjoman. Dana will recommend agents based on your available keys.
          </p>

          {/* OpenAI */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              OpenAI API Key
              <span className="text-gray-500 ml-2">(GPT-4, GPT-3.5)</span>
            </label>
            <div className="relative">
              <input
                type={showKeys.openai ? 'text' : 'password'}
                value={keys.openai_api_key || ''}
                onChange={(e) => setKeys({ ...keys, openai_api_key: e.target.value })}
                placeholder="sk-..."
                className="w-full px-4 py-3 pr-12 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <button
                type="button"
                onClick={() => setShowKeys({ ...showKeys, openai: !showKeys.openai })}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
              >
                {showKeys.openai ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
              </button>
            </div>
            <a
              href="https://platform.openai.com/api-keys"
              target="_blank"
              rel="noopener noreferrer"
              className="text-xs text-blue-600 hover:underline mt-1 inline-block"
            >
              Get your OpenAI API key →
            </a>
          </div>

          {/* Anthropic */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Anthropic API Key
              <span className="text-gray-500 ml-2">(Claude)</span>
            </label>
            <div className="relative">
              <input
                type={showKeys.anthropic ? 'text' : 'password'}
                value={keys.anthropic_api_key || ''}
                onChange={(e) => setKeys({ ...keys, anthropic_api_key: e.target.value })}
                placeholder="sk-ant-..."
                className="w-full px-4 py-3 pr-12 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <button
                type="button"
                onClick={() => setShowKeys({ ...showKeys, anthropic: !showKeys.anthropic })}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
              >
                {showKeys.anthropic ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
              </button>
            </div>
            <a
              href="https://console.anthropic.com/"
              target="_blank"
              rel="noopener noreferrer"
              className="text-xs text-blue-600 hover:underline mt-1 inline-block"
            >
              Get your Anthropic API key →
            </a>
          </div>

          {/* Mistral */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Mistral API Key
              <span className="text-gray-500 ml-2">(Optional)</span>
            </label>
            <div className="relative">
              <input
                type={showKeys.mistral ? 'text' : 'password'}
                value={keys.mistral_api_key || ''}
                onChange={(e) => setKeys({ ...keys, mistral_api_key: e.target.value })}
                placeholder="..."
                className="w-full px-4 py-3 pr-12 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <button
                type="button"
                onClick={() => setShowKeys({ ...showKeys, mistral: !showKeys.mistral })}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
              >
                {showKeys.mistral ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
              </button>
            </div>
            <a
              href="https://console.mistral.ai/"
              target="_blank"
              rel="noopener noreferrer"
              className="text-xs text-blue-600 hover:underline mt-1 inline-block"
            >
              Get your Mistral API key →
            </a>
          </div>

          {/* Google/Gemini */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Google API Key
              <span className="text-gray-500 ml-2">(Gemini, Optional)</span>
            </label>
            <div className="relative">
              <input
                type={showKeys.google ? 'text' : 'password'}
                value={keys.google_api_key || ''}
                onChange={(e) => setKeys({ ...keys, google_api_key: e.target.value })}
                placeholder="..."
                className="w-full px-4 py-3 pr-12 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <button
                type="button"
                onClick={() => setShowKeys({ ...showKeys, google: !showKeys.google })}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
              >
                {showKeys.google ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
              </button>
            </div>
            <a
              href="https://makersuite.google.com/app/apikey"
              target="_blank"
              rel="noopener noreferrer"
              className="text-xs text-blue-600 hover:underline mt-1 inline-block"
            >
              Get your Google API key →
            </a>
          </div>

          {/* Cohere */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Cohere API Key
              <span className="text-gray-500 ml-2">(Optional)</span>
            </label>
            <div className="relative">
              <input
                type={showKeys.cohere ? 'text' : 'password'}
                value={keys.cohere_api_key || ''}
                onChange={(e) => setKeys({ ...keys, cohere_api_key: e.target.value })}
                placeholder="..."
                className="w-full px-4 py-3 pr-12 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <button
                type="button"
                onClick={() => setShowKeys({ ...showKeys, cohere: !showKeys.cohere })}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
              >
                {showKeys.cohere ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
              </button>
            </div>
            <a
              href="https://dashboard.cohere.com/api-keys"
              target="_blank"
              rel="noopener noreferrer"
              className="text-xs text-blue-600 hover:underline mt-1 inline-block"
            >
              Get your Cohere API key →
            </a>
          </div>

          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <p className="text-sm text-blue-800">
              <strong>Security:</strong> Your keys are only sent to your backend server and used for API calls. 
              They are never stored permanently or shared.
            </p>
          </div>

          <div className="flex space-x-3">
            <button
              onClick={handleSave}
              className="flex-1 flex items-center justify-center space-x-2 px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition"
            >
              <Save className="w-5 h-5" />
              <span>Save Keys</span>
            </button>
            <button
              onClick={onClose}
              className="px-6 py-3 bg-gray-200 text-gray-700 font-medium rounded-lg hover:bg-gray-300 transition"
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

