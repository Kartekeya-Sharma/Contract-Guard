import React from "react";

const AnalysisResults = ({ results }) => {
  if (!results) {
    return (
      <div className="p-4 bg-white rounded-lg shadow">
        <p className="text-gray-500">No analysis results available.</p>
      </div>
    );
  }

  if (!results.clauses || !Array.isArray(results.clauses)) {
    return (
      <div className="p-4 bg-white rounded-lg shadow">
        <p className="text-gray-500">
          No clauses found in the analysis results.
        </p>
      </div>
    );
  }

  const getRiskColor = (riskLevel) => {
    switch (riskLevel?.toLowerCase()) {
      case "high":
        return "bg-red-100 text-red-800";
      case "medium":
        return "bg-yellow-100 text-yellow-800";
      case "low":
        return "bg-green-100 text-green-800";
      default:
        return "bg-gray-100 text-gray-800";
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">
          Contract Analysis Results
        </h2>

        <div className="space-y-4">
          {results.clauses.map((clause, index) => (
            <div
              key={index}
              className="border rounded-lg p-4 hover:shadow-md transition-shadow"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-gray-900 capitalize">
                    {clause.type?.replace(/_/g, " ") || "Unknown"} Clause
                  </h3>
                  <p className="mt-1 text-sm text-gray-600">
                    {clause.text || "No text available"}
                  </p>

                  <div className="mt-3">
                    <span
                      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getRiskColor(
                        clause.risk_level
                      )}`}
                    >
                      {(clause.risk_level || "UNKNOWN").toUpperCase()} Risk
                    </span>
                  </div>

                  <div className="mt-3">
                    <h4 className="text-sm font-medium text-gray-900">
                      Risk Analysis:
                    </h4>
                    <p className="mt-1 text-sm text-gray-600">
                      {clause.explanation || "No risk analysis available"}
                    </p>
                  </div>

                  <div className="mt-3">
                    <h4 className="text-sm font-medium text-gray-900">
                      Key Concerns:
                    </h4>
                    <ul className="mt-1 list-disc list-inside text-sm text-gray-600">
                      {Array.isArray(clause.specific_concerns) &&
                      clause.specific_concerns.length > 0 ? (
                        clause.specific_concerns.map((concern, idx) => (
                          <li key={idx}>{concern}</li>
                        ))
                      ) : (
                        <li>No specific concerns identified</li>
                      )}
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default AnalysisResults;
