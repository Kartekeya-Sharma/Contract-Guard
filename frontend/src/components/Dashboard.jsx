import { useState } from "react";
import {
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { FiChevronDown, FiChevronUp } from "react-icons/fi";

const COLORS = {
  Low: "#10B981", // Green
  Medium: "#F59E0B", // Yellow
  High: "#EF4444", // Red
};

const TYPE_COLORS = [
  "#3B82F6", // Blue
  "#8B5CF6", // Purple
  "#EC4899", // Pink
  "#F97316", // Orange
  "#14B8A6", // Teal
  "#6366F1", // Indigo
];

const Dashboard = ({ clauses }) => {
  const [expandedClause, setExpandedClause] = useState(null);

  // Prepare data for charts
  const riskData = clauses.reduce((acc, clause) => {
    acc[clause.risk] = (acc[clause.risk] || 0) + 1;
    return acc;
  }, {});

  const typeData = clauses.reduce((acc, clause) => {
    acc[clause.type] = (acc[clause.type] || 0) + 1;
    return acc;
  }, {});

  const riskChartData = Object.entries(riskData).map(([name, value]) => ({
    name,
    value,
  }));

  const typeChartData = Object.entries(typeData).map(([name, value]) => ({
    name,
    value,
  }));

  return (
    <div className="space-y-6">
      {/* Charts */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Risk Distribution */}
        <div className="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
          <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">
            Risk Distribution
          </h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={riskChartData}
                  dataKey="value"
                  nameKey="name"
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
                  label
                >
                  {riskChartData.map((entry, index) => (
                    <Cell key={entry.name} fill={COLORS[entry.name]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Clause Types */}
        <div className="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
          <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">
            Clause Types
          </h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={typeChartData}>
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="value" fill="#3B82F6" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Clause Cards */}
      <div className="space-y-4">
        {clauses.map((clause, index) => (
          <div
            key={index}
            className="bg-white dark:bg-gray-800 shadow rounded-lg overflow-hidden"
          >
            <div
              className="p-4 cursor-pointer"
              onClick={() =>
                setExpandedClause(expandedClause === index ? null : index)
              }
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <span
                    className={`px-2 py-1 text-xs font-medium rounded-full
                      ${
                        clause.risk === "High"
                          ? "bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-400"
                          : clause.risk === "Medium"
                          ? "bg-yellow-100 text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-400"
                          : "bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400"
                      }
                    `}
                  >
                    {clause.risk}
                  </span>
                  <span className="text-sm font-medium text-gray-900 dark:text-white">
                    {clause.type}
                  </span>
                </div>
                {expandedClause === index ? (
                  <FiChevronUp className="h-5 w-5 text-gray-400" />
                ) : (
                  <FiChevronDown className="h-5 w-5 text-gray-400" />
                )}
              </div>

              {expandedClause === index && (
                <div className="mt-4 space-y-4">
                  <div>
                    <h4 className="text-sm font-medium text-gray-500 dark:text-gray-400">
                      Original Clause
                    </h4>
                    <p className="mt-1 text-sm text-gray-900 dark:text-white">
                      {clause.clause}
                    </p>
                  </div>
                  <div>
                    <h4 className="text-sm font-medium text-gray-500 dark:text-gray-400">
                      Plain English Explanation
                    </h4>
                    <p className="mt-1 text-sm text-gray-900 dark:text-white">
                      {clause.explanation}
                    </p>
                  </div>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Dashboard;
