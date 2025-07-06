import React, { useCallback } from "react";
import { useDropzone } from "react-dropzone";
import { motion } from "framer-motion";
import axios from "axios";
import { toast } from "react-toastify";

const ContractUpload = ({ onAnalysisComplete, setIsAnalyzing }) => {
  const onDrop = useCallback(
    async (acceptedFiles) => {
      const file = acceptedFiles[0];
      if (!file) return;

      // Check file type
      const validTypes = [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "text/plain",
      ];
      if (!validTypes.includes(file.type)) {
        toast.error("Please upload a PDF, DOCX, or TXT file");
        return;
      }

      const formData = new FormData();
      formData.append("file", file);

      try {
        setIsAnalyzing(true);
        const response = await axios.post(
          "http://localhost:5001/api/upload",
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        );

        onAnalysisComplete(response.data);
        toast.success("Contract analyzed successfully!");
      } catch (error) {
        console.error("Upload error:", error);
        toast.error(error.response?.data?.error || "Error analyzing contract");
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
    multiple: false,
  });

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="max-w-2xl mx-auto"
    >
      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-lg p-12 text-center cursor-pointer transition-colors
          ${
            isDragActive
              ? "border-blue-500 bg-blue-50 dark:bg-blue-900/20"
              : "border-gray-300 dark:border-gray-600 hover:border-blue-500 dark:hover:border-blue-400"
          }`}
      >
        <input {...getInputProps()} />
        <div className="space-y-4">
          <div className="text-6xl mb-4">📄</div>
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
            {isDragActive
              ? "Drop your contract here"
              : "Drag & drop your contract here"}
          </h2>
          <p className="text-gray-500 dark:text-gray-400">
            or click to select a file
          </p>
          <p className="text-sm text-gray-400 dark:text-gray-500">
            Supported formats: PDF, DOCX, TXT
          </p>
        </div>
      </div>
    </motion.div>
  );
};

export default ContractUpload;
