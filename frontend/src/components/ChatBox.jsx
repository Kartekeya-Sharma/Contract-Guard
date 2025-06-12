import { useState } from "react";
import { FiSend } from "react-icons/fi";
import axios from "axios";
import toast from "react-hot-toast";

const ChatBox = ({ clauses }) => {
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!query.trim()) return;

    try {
      setIsLoading(true);

      const response = await axios.post("http://localhost:5000/api/query", {
        query: query.trim(),
        clauses,
      });

      setAnswer(response.data.answer);
      setQuery("");
    } catch (error) {
      toast.error(error.message || "Error getting answer");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
      <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">
        Ask About Your Contract
      </h3>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="query" className="sr-only">
            Your question
          </label>
          <div className="relative">
            <input
              type="text"
              id="query"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="e.g., What happens if I cancel early?"
              className="block w-full rounded-lg border-gray-300 dark:border-gray-600 
                bg-white dark:bg-gray-700 text-gray-900 dark:text-white
                shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm
                pr-12"
              disabled={isLoading}
            />
            <button
              type="submit"
              className="absolute inset-y-0 right-0 flex items-center pr-3
                text-gray-400 hover:text-gray-500 dark:hover:text-gray-300
                disabled:opacity-50 disabled:cursor-not-allowed"
              disabled={isLoading || !query.trim()}
            >
              <FiSend className="h-5 w-5" />
            </button>
          </div>
        </div>
      </form>

      {isLoading && (
        <div className="mt-4 text-sm text-gray-500 dark:text-gray-400">
          Thinking...
        </div>
      )}

      {answer && (
        <div className="mt-4">
          <h4 className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">
            Answer
          </h4>
          <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
            <p className="text-sm text-gray-900 dark:text-white">{answer}</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatBox;
