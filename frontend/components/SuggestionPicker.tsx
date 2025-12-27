import { ArrowRight } from 'lucide-react'

interface SuggestionPickerProps {
  suggestion: string
  onSelectPart: (part: string) => void
}

export default function SuggestionPicker({ suggestion, onSelectPart }: SuggestionPickerProps) {
  // Split suggestion into selectable parts (sentences or logical breaks)
  const parts = splitIntoSelectableParts(suggestion)
  
  return (
    <div className="space-y-2">
      <p className="text-xs text-gray-500 mb-2">
        Click any part to use it as guidance:
      </p>
      {parts.map((part, idx) => (
        <button
          key={idx}
          onClick={() => onSelectPart(part.trim())}
          className="w-full text-left p-3 bg-white border-2 border-amber-200 rounded-lg hover:border-amber-400 hover:bg-amber-50 transition-all group text-sm"
        >
          <div className="flex items-start justify-between">
            <p className="text-gray-800 flex-1 pr-2">{part.trim()}</p>
            <ArrowRight className="w-4 h-4 text-amber-600 flex-shrink-0 mt-0.5 group-hover:translate-x-1 transition-transform" />
          </div>
        </button>
      ))}
    </div>
  )
}

function splitIntoSelectableParts(text: string): string[] {
  const parts: string[] = []
  
  // First, try to split by explicit markers like (a), (b), etc.
  const markerPattern = /\([a-z]\)/g
  const markers = text.match(markerPattern)
  
  if (markers && markers.length > 1) {
    // Split by markers
    const splits = text.split(markerPattern)
    for (let i = 1; i < splits.length; i++) {
      const part = `(${String.fromCharCode(96 + i)}) ${splits[i].trim()}`
      if (part.length > 10) {
        parts.push(part)
      }
    }
    // Add the intro part if substantial
    if (splits[0].trim().length > 20) {
      parts.unshift(splits[0].trim())
    }
  } else {
    // Split by sentences or natural breaks
    // Look for: period+space, colon, semicolon followed by capital letter
    const sentences = text.split(/(?<=[.;:])\s+(?=[A-Z(])|(?<=:)\s+/)
    
    for (const sentence of sentences) {
      const trimmed = sentence.trim()
      if (trimmed.length > 15) {
        parts.push(trimmed)
      }
    }
  }
  
  // If we couldn't split it well, return the whole thing
  if (parts.length === 0 || parts.length === 1 && parts[0] === text) {
    // Try splitting by major punctuation
    const majorSplits = text.split(/\.\s+(?=[A-Z])/)
    if (majorSplits.length > 1) {
      return majorSplits.map(s => s.trim() + (s.endsWith('.') ? '' : '.')).filter(s => s.length > 15)
    }
    return [text]
  }
  
  return parts
}

