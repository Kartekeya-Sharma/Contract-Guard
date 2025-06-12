import { useCallback } from "react";
import { useDropzone } from "react-dropzone";
import { FiUpload } from "react-icons/fi";
import toast from "react-hot-toast";
import axios from "axios";

const FileUpload = ({ onAnalysisComplete, isAnalyzing, setIsAnalyzing }) => {
  const onDrop = useCallback(
    async (acceptedFiles) => {
      const file = acceptedFiles[0];

      if (!file) return;

      // Validate file type
      const validTypes = [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "text/plain",
      ];
      if (!validTypes.includes(file.type)) {
        toast.error("Please upload a PDF, DOCX, or TXT file");
        return;
      }

      // Validate file size (5MB)
      if (file.size > 5 * 1024 * 1024) {
        toast.error("File size must be less than 5MB");
        return;
      }

      try {
        setIsAnalyzing(true);

        const formData = new FormData();
        formData.append("file", file);

        const response = await axios.post(
          "http://localhost:5000/api/analyze",
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        );

        if (response.data.status === "success") {
          onAnalysisComplete(response.data.clauses);
          toast.success("Contract analyzed successfully!");
        } else {
          throw new Error(response.data.error || "Analysis failed");
        }
      } catch (error) {
        toast.error(error.message || "Error analyzing contract");
      } finally {
        setIsAnalyzing(false);
      }
    },
    [onAnalysisComplete, setIsAnalyzing]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "application/pdf": [".pdf"],
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        [".docx"],
      "text/plain": [".txt"],
    },
    maxFiles: 1,
    disabled: isAnalyzing,
  });

  return (
    <div className="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-lg p-6 text-center cursor-pointer transition-colors
          ${
            isDragActive
              ? "border-blue-500 bg-blue-50 dark:bg-blue-900/20"
              : "border-gray-300 dark:border-gray-600 hover:border-blue-500 dark:hover:border-blue-400"
          }
          ${isAnalyzing ? "opacity-50 cursor-not-allowed" : ""}
        `}
      >
        <input {...getInputProps()} />
        <FiUpload className="mx-auto h-12 w-12 text-gray-400" />
        <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
          {isAnalyzing
            ? "Analyzing contract..."
            : isDragActive
            ? "Drop the file here"
            : "Drag and drop a contract file here, or click to select"}
        </p>
        <p className="mt-1 text-xs text-gray-500 dark:text-gray-500">
          PDF, DOCX, or TXT (max 5MB)
        </p>
      </div>
    </div>
  );
};

export default FileUpload;
