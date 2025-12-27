export type SessionStatus = 'active' | 'completed' | 'paused' | 'error'

export interface AgentConfig {
  id: string
  role: string
  style?: string
  model: string
  cost_used: number
  tokens_in: number
  tokens_out: number
}

export interface AgentMessage {
  agent_id: string
  agent_role: string
  content: string
  timestamp: string
  tokens_in: number
  tokens_out: number
  cost: number
}

export interface SuggestedDirection {
  option: string
  description: string
}

export interface IterationSummary {
  iteration_number: number
  summary: string
  key_disagreements?: string[]
  suggested_directions?: SuggestedDirection[]
  suggested_direction?: string  // Deprecated, kept for backwards compatibility
  total_cost: number
  timestamp: string
}

export interface Iteration {
  iteration_number: number
  messages: AgentMessage[]
  summary: IterationSummary
  user_guidance?: string
}

export interface BudgetInfo {
  total_budget: number
  used: number
  remaining: number
  warning_threshold: number
  is_warning?: boolean
  is_exceeded?: boolean
}

export interface Session {
  session_id: string
  created_at: string
  updated_at: string
  issue: string
  agents: AgentConfig[]
  iterations: Iteration[]
  budget: BudgetInfo
  status: SessionStatus
}

export interface ApiKeys {
  openai_api_key?: string
  anthropic_api_key?: string
  mistral_api_key?: string
  google_api_key?: string
  cohere_api_key?: string
}

export interface ModelInfo {
  model_id: string
  display_name: string
  provider: string
  description?: string
}

export interface SessionProposal {
  proposed_agents: AgentConfig[]
  rationale: string
  available_models: ModelInfo[]
}

export interface CreateSessionRequest {
  issue: string
  budget: number
  suggested_agents?: AgentConfig[]
  api_keys?: ApiKeys
}

export interface ContinueSessionRequest {
  session_id: string
  user_guidance?: string
  accept_suggestion: boolean
  api_keys?: ApiKeys
}

export interface SessionListItem {
  session_id: string
  created_at: string
  issue: string
  status: SessionStatus
  total_cost: number
  iteration_count: number
}

export interface ModelPricing {
  provider: string
  model: string
  model_id: string
  input_per_1m: number
  output_per_1m: number
}

