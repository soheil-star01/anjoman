import { SessionListItem } from '@/types'
import { Clock, DollarSign, MessageSquare, Trash2 } from 'lucide-react'
import { formatDistanceToNow } from 'date-fns'
import { api } from '@/lib/api'

interface SessionListProps {
  sessions: SessionListItem[]
  onSelectSession: (sessionId: string) => void
  onRefresh: () => void
}

export default function SessionList({ sessions, onSelectSession, onRefresh }: SessionListProps) {
  const handleDelete = async (sessionId: string, e: React.MouseEvent) => {
    e.stopPropagation()
    if (!confirm('Are you sure you want to delete this session?')) return

    try {
      await api.deleteSession(sessionId)
      onRefresh()
    } catch (error) {
      console.error('Error deleting session:', error)
    }
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-xl shadow-lg overflow-hidden">
        <div className="bg-gradient-to-r from-gray-700 to-gray-900 px-6 py-4">
          <h2 className="text-2xl font-bold text-white">Session History</h2>
          <p className="text-gray-300 text-sm mt-1">
            {sessions.length} {sessions.length === 1 ? 'session' : 'sessions'}
          </p>
        </div>

        {sessions.length === 0 ? (
          <div className="p-12 text-center">
            <MessageSquare className="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <p className="text-gray-500">No sessions yet. Start your first deliberation!</p>
          </div>
        ) : (
          <div className="divide-y divide-gray-200">
            {sessions.map((session) => (
              <div
                key={session.session_id}
                onClick={() => onSelectSession(session.session_id)}
                className="p-6 hover:bg-gray-50 cursor-pointer transition-colors"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1 min-w-0 pr-4">
                    <div className="flex items-center space-x-3 mb-2">
                      <h3 className="text-lg font-semibold text-gray-900 truncate">
                        {session.session_id}
                      </h3>
                      <StatusBadge status={session.status} />
                    </div>

                    <p className="text-gray-700 mb-3 line-clamp-2">
                      {session.issue}
                    </p>

                    <div className="flex items-center space-x-4 text-sm text-gray-500">
                      <div className="flex items-center space-x-1">
                        <Clock className="w-4 h-4" />
                        <span>
                          {formatDistanceToNow(new Date(session.created_at), { addSuffix: true })}
                        </span>
                      </div>

                      <div className="flex items-center space-x-1">
                        <MessageSquare className="w-4 h-4" />
                        <span>{session.iteration_count} iterations</span>
                      </div>

                      <div className="flex items-center space-x-1">
                        <DollarSign className="w-4 h-4" />
                        <span>${session.total_cost.toFixed(4)}</span>
                      </div>
                    </div>
                  </div>

                  <button
                    onClick={(e) => handleDelete(session.session_id, e)}
                    className="flex-shrink-0 p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition"
                  >
                    <Trash2 className="w-5 h-5" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

function StatusBadge({ status }: { status: SessionListItem['status'] }) {
  const styles = {
    active: 'bg-green-100 text-green-800',
    completed: 'bg-blue-100 text-blue-800',
    paused: 'bg-yellow-100 text-yellow-800',
    error: 'bg-red-100 text-red-800',
  }

  return (
    <span className={`px-2 py-1 rounded text-xs font-medium ${styles[status]}`}>
      {status}
    </span>
  )
}

