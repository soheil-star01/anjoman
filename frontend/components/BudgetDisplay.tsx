import { BudgetInfo } from '@/types'
import { DollarSign, AlertTriangle } from 'lucide-react'

interface BudgetDisplayProps {
  budget: BudgetInfo
}

export default function BudgetDisplay({ budget }: BudgetDisplayProps) {
  const percentUsed = (budget.used / budget.total_budget) * 100
  const isWarning = percentUsed >= budget.warning_threshold * 100
  const isExceeded = percentUsed >= 100

  return (
    <div className="bg-gray-50 border border-gray-200 rounded-lg p-4 min-w-[200px]">
      <div className="flex items-center space-x-2 mb-2">
        <DollarSign className="w-4 h-4 text-gray-600" />
        <span className="text-sm font-semibold text-gray-700">Budget Tracker</span>
      </div>

      <div className="space-y-2">
        {budget.used > 0 ? (
          <>
            <div className="flex items-center justify-between text-sm">
              <span className="text-gray-600">Used:</span>
              <span className={`font-medium ${isExceeded ? 'text-red-600' : isWarning ? 'text-yellow-600' : 'text-green-600'}`}>
                ≈ ${budget.used.toFixed(4)}
              </span>
            </div>

            <div className="flex items-center justify-between text-sm">
              <span className="text-gray-600">Limit:</span>
              <span className="font-medium text-gray-900">
                ${budget.total_budget.toFixed(2)}
              </span>
            </div>
          </>
        ) : (
          <div className="text-xs text-gray-500 italic">
            Cost tracking in progress...
          </div>
        )}

        {/* Progress bar */}
        <div className="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
          <div
            className={`h-full transition-all ${
              isExceeded ? 'bg-red-500' : isWarning ? 'bg-yellow-500' : 'bg-green-500'
            }`}
            style={{ width: `${Math.min(percentUsed, 100)}%` }}
          />
        </div>

        <div className="text-xs text-gray-500 text-center">
          {percentUsed.toFixed(1)}% used
        </div>

        {isWarning && (
          <div className={`flex items-center space-x-1 text-xs ${isExceeded ? 'text-red-600' : 'text-yellow-600'}`}>
            <AlertTriangle className="w-3 h-3" />
            <span>{isExceeded ? 'Budget exceeded!' : 'Budget warning'}</span>
          </div>
        )}
      </div>
    </div>
  )
}

