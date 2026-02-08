// frontend/src/components/TaskCard.tsx
import React from 'react';

interface TaskCardProps {
  task: {
    id: string;
    title: string;
    description?: string;
    completed: boolean;
  };
  onToggleComplete: (id: string) => void;
  onDelete: (id: string) => void;
}

const TaskCard: React.FC<TaskCardProps> = ({ task, onToggleComplete, onDelete }) => {
  return (
    <div className="bg-white shadow-md rounded-lg p-4 mb-4 flex flex-col md:flex-row justify-between items-start md:items-center">
      <div className="flex-1">
        <h3 className={`text-lg font-semibold ${task.completed ? 'line-through text-gray-500' : 'text-gray-800'}`}>
          {task.title}
        </h3>
        {task.description && (
          <p className={`text-gray-600 ${task.completed ? 'line-through' : ''}`}>
            {task.description}
          </p>
        )}
      </div>
      <div className="flex items-center space-x-2 mt-4 md:mt-0">
        <button
          onClick={() => onToggleComplete(task.id)}
          className={`px-3 py-1 rounded-full text-sm font-medium transition-colors duration-200
            ${task.completed ? 'bg-green-500 text-white hover:bg-green-600' : 'bg-yellow-400 text-gray-800 hover:bg-yellow-500'}`}
        >
          {task.completed ? 'Completed' : 'Mark Complete'}
        </button>
        <button
          onClick={() => onDelete(task.id)}
          className="px-3 py-1 rounded-full bg-red-500 text-white text-sm font-medium hover:bg-red-600 transition-colors duration-200"
        >
          Delete
        </button>
      </div>
    </div>
  );
};

export default TaskCard;
