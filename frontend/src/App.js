import React, { useState } from "react";
import { motion } from "framer-motion";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import ContractUpload from "./components/ContractUpload";
import ContractAnalysis from "./components/ContractAnalysis";
import Dashboard from "./components/Dashboard";
import FileUpload from "./components/FileUpload";
import AnalysisResults from "./components/AnalysisResults";

function App() {
  const [darkMode, setDarkMode] = useState(false);
  const [analysisResults, setAnalysisResults] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysis, setAnalysis] = useState(null);

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
    document.documentElement.classList.toggle("dark");
  };

  const handleUploadComplete = (data) => {
    console.log("Upload complete, received data:", data);
    setIsAnalyzing(true);

    // Check if we have valid analysis results
    if (data && data.clauses && Array.isArray(data.clauses)) {
      setAnalysisResults(data);
      toast.success("Analysis complete!");
    } else {
      console.error("Invalid analysis results:", data);
      toast.error("Error processing analysis results");
    }
    setIsAnalyzing(false);
  };

  return (
    <div
      className={`min-h-screen ${darkMode ? "dark bg-gray-900" : "bg-gray-50"}`}
    >
      <ToastContainer position="top-right" />

      <header className="bg-white dark:bg-gray-800 shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            Contract Guard
          </h1>
          <button
            onClick={toggleDarkMode}
            className="p-2 rounded-lg bg-gray-200 dark:bg-gray-700"
          >
            {darkMode ? "🌞" : "🌙"}
          </button>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          {!analysisResults ? (
            <div className="space-y-8">
              <h2 className="text-xl font-semibold mb-4">Upload Contract</h2>
              <FileUpload onUploadComplete={handleUploadComplete} />
              {analysis && (
                <div className="mt-8">
                  <h3 className="text-lg font-semibold mb-4">
                    Analysis Results
                  </h3>
                  <div className="space-y-4">
                    {analysis.clauses.map((clause, index) => (
                      <div key={index} className="border rounded-lg p-4">
                        <div className="flex justify-between items-start mb-2">
                          <span className="font-medium">
                            Type: {clause.type}
                          </span>
                          <span
                            className={`px-2 py-1 rounded text-sm ${
                              clause.risk_level === "High"
                                ? "bg-red-100 text-red-800"
                                : clause.risk_level === "Medium"
                                ? "bg-yellow-100 text-yellow-800"
                                : "bg-green-100 text-green-800"
                            }`}
                          >
                            {clause.risk_level} Risk
                          </span>
                        </div>
                        <p className="text-gray-600 mb-2">{clause.text}</p>
                        <p className="text-sm text-gray-500">
                          {clause.explanation}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="space-y-8">
              <Dashboard analysisResults={analysisResults} />
              <AnalysisResults
                results={analysisResults}
                onReset={() => setAnalysisResults(null)}
              />
            </div>
          )}
        </motion.div>
      </main>
    </div>
  );
}

export default App;
