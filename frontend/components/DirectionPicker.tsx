import { ArrowRight } from 'lucide-react'

interface SuggestedDirection {
  option: string
  description: string
}

interface DirectionPickerProps {
  directions: SuggestedDirection[]
  onSelectDirection: (option: string) => void
}

export default function DirectionPicker({ directions, onSelectDirection }: DirectionPickerProps) {
  if (!directions || directions.length === 0) {
    return null
  }

  return (
    <div className="space-y-2">
      <p className="text-xs text-gray-500 mb-2">
        Click any direction to use it as guidance:
      </p>
      {directions.map((direction, idx) => (
        <button
          key={idx}
          onClick={() => onSelectDirection(direction.option)}
          className="w-full text-left p-3 bg-white border-2 border-amber-200 rounded-lg hover:border-amber-400 hover:bg-amber-50 transition-all group"
        >
          <div className="flex items-start justify-between">
            <div className="flex-1 pr-2">
              <p className="font-semibold text-gray-900 mb-1">{direction.option}</p>
              <p className="text-xs text-gray-600">{direction.description}</p>
            </div>
            <ArrowRight className="w-4 h-4 text-amber-600 flex-shrink-0 mt-1 group-hover:translate-x-1 transition-transform" />
          </div>
        </button>
      ))}
    </div>
  )
}

