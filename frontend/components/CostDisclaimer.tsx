import { Info } from 'lucide-react'

export default function CostDisclaimer() {
  return (
    <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
      <div className="flex items-start space-x-2">
        <Info className="w-4 h-4 text-blue-600 flex-shrink-0 mt-0.5" />
        <div className="text-xs text-blue-800">
          <p className="font-semibold mb-1">About Token Costs</p>
          <p>
            Token usage is tracked accurately. Cost estimates (≈) are approximate and may not reflect latest pricing.
            Actual costs depend on your API provider&apos;s current rates.
          </p>
        </div>
      </div>
    </div>
  )
}

