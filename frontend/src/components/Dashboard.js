import React from "react";
import { Pie, Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
} from "chart.js";

ChartJS.register(
  ArcElement,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  BarElement,
  Title
);

const Dashboard = ({ analysisResults }) => {
  // Process data for charts
  const clauseTypes = analysisResults.clauses.reduce((acc, clause) => {
    acc[clause.type] = (acc[clause.type] || 0) + 1;
    return acc;
  }, {});

  const riskLevels = analysisResults.clauses.reduce((acc, clause) => {
    acc[clause.risk_level] = (acc[clause.risk_level] || 0) + 1;
    return acc;
  }, {});

  // Prepare data for Pie Chart (Clause Types)
  const pieData = {
    labels: Object.keys(clauseTypes),
    datasets: [
      {
        data: Object.values(clauseTypes),
        backgroundColor: [
          "#8B5CF6", // Purple
          "#3B82F6", // Blue
          "#6366F1", // Indigo
          "#10B981", // Green
          "#EF4444", // Red
          "#F59E0B", // Yellow
          "#F97316", // Orange
          "#EC4899", // Pink
          "#6B7280", // Gray
        ],
        borderWidth: 1,
      },
    ],
  };

  // Prepare data for Bar Chart (Risk Levels)
  const barData = {
    labels: ["Low", "Medium", "High"],
    datasets: [
      {
        label: "Number of Clauses",
        data: [
          riskLevels.Low || 0,
          riskLevels.Medium || 0,
          riskLevels.High || 0,
        ],
        backgroundColor: [
          "#10B981", // Green
          "#F59E0B", // Yellow
          "#EF4444", // Red
        ],
      },
    ],
  };

  const barOptions = {
    responsive: true,
    plugins: {
      legend: {
        display: false,
      },
      title: {
        display: true,
        text: "Risk Level Distribution",
        color: "#6B7280",
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          stepSize: 1,
        },
      },
    },
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
      <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
        Analysis Dashboard
      </h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div>
          <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">
            Clause Types Distribution
          </h3>
          <div className="h-80">
            <Pie data={pieData} options={{ maintainAspectRatio: false }} />
          </div>
        </div>

        <div>
          <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">
            Risk Level Distribution
          </h3>
          <div className="h-80">
            <Bar
              data={barData}
              options={{ ...barOptions, maintainAspectRatio: false }}
            />
          </div>
        </div>
      </div>

      <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
          <h4 className="text-sm font-medium text-gray-500 dark:text-gray-400">
            Total Clauses
          </h4>
          <p className="text-2xl font-bold text-gray-900 dark:text-white">
            {analysisResults.clauses.length}
          </p>
        </div>

        <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
          <h4 className="text-sm font-medium text-gray-500 dark:text-gray-400">
            High Risk Clauses
          </h4>
          <p className="text-2xl font-bold text-red-600 dark:text-red-400">
            {riskLevels.High || 0}
          </p>
        </div>

        <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
          <h4 className="text-sm font-medium text-gray-500 dark:text-gray-400">
            Unique Clause Types
          </h4>
          <p className="text-2xl font-bold text-gray-900 dark:text-white">
            {Object.keys(clauseTypes).length}
          </p>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
