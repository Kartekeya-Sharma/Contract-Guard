import React from "react";
import { motion } from "framer-motion";

const RiskBadge = ({ level }) => {
  const colors = {
    Low: "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300",
    Medium:
      "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300",
    High: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300",
  };

  return (
    <span
      className={`px-2 py-1 rounded-full text-xs font-medium ${colors[level]}`}
    >
      {level} Risk
    </span>
  );
};

const TypeBadge = ({ type }) => {
  const colors = {
    IP: "bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300",
    Termination:
      "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300",
    Confidentiality:
      "bg-indigo-100 text-indigo-800 dark:bg-indigo-900 dark:text-indigo-300",
    Payment:
      "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300",
    Liability: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300",
    Warranty:
      "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300",
    Indemnification:
      "bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-300",
    "Force Majeure":
      "bg-pink-100 text-pink-800 dark:bg-pink-900 dark:text-pink-300",
    "Governing Law":
      "bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300",
    Other: "bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300",
  };

  return (
    <span
      className={`px-2 py-1 rounded-full text-xs font-medium ${
        colors[type] || colors.Other
      }`}
    >
      {type}
    </span>
  );
};

const ContractAnalysis = ({ results, onReset }) => {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
          Contract Analysis
        </h2>
        <button
          onClick={onReset}
          className="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-md hover:bg-gray-50 dark:hover:bg-gray-700"
        >
          Analyze Another Contract
        </button>
      </div>

      <div className="grid gap-6">
        {results.clauses.map((clause, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className="bg-white dark:bg-gray-800 rounded-lg shadow p-6"
          >
            <div className="flex flex-wrap gap-2 mb-4">
              <TypeBadge type={clause.type} />
              <RiskBadge level={clause.risk_level} />
            </div>

            <div className="space-y-4">
              <div>
                <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">
                  Original Text
                </h3>
                <p className="text-gray-900 dark:text-white text-sm">
                  {clause.text}
                </p>
              </div>

              <div>
                <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">
                  Plain English Explanation
                </h3>
                <p className="text-gray-900 dark:text-white text-sm">
                  {clause.explanation}
                </p>
              </div>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
};

export default ContractAnalysis;
