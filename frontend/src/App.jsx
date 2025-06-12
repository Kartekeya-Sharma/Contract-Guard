import { useState } from "react";
import { QueryClient, QueryClientProvider } from "react-query";
import { Toaster } from "react-hot-toast";
import FileUpload from "./components/FileUpload";
import Dashboard from "./components/Dashboard";
import ChatBox from "./components/ChatBox";

// Create a client
const queryClient = new QueryClient();

function App() {
  const [analyzedClauses, setAnalyzedClauses] = useState([]);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  return (
    <QueryClientProvider client={queryClient}>
      <div className="min-h-screen bg-gray-100 dark:bg-gray-900">
        <Toaster position="top-right" />

        <header className="bg-white dark:bg-gray-800 shadow">
          <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
              Contract Guard
            </h1>
          </div>
        </header>

        <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          <div className="px-4 py-6 sm:px-0">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Left Column - File Upload */}
              <div className="lg:col-span-1">
                <FileUpload
                  onAnalysisComplete={setAnalyzedClauses}
                  isAnalyzing={isAnalyzing}
                  setIsAnalyzing={setIsAnalyzing}
                />
              </div>

              {/* Right Column - Dashboard & Chat */}
              <div className="lg:col-span-2">
                {analyzedClauses.length > 0 ? (
                  <>
                    <Dashboard clauses={analyzedClauses} />
                    <div className="mt-6">
                      <ChatBox clauses={analyzedClauses} />
                    </div>
                  </>
                ) : (
                  <div className="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
                    <p className="text-gray-500 dark:text-gray-400 text-center">
                      Upload a contract to begin analysis
                    </p>
                  </div>
                )}
              </div>
            </div>
          </div>
        </main>
      </div>
    </QueryClientProvider>
  );
}

export default App;
