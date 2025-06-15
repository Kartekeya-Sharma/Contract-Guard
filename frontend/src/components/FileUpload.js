import React, { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import { toast } from "react-toastify";
import axios from "axios";

const FileUpload = ({ onUploadComplete }) => {
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);

  const onDrop = useCallback(
    async (acceptedFiles) => {
      const file = acceptedFiles[0];
      if (!file) return;

      console.log(
        "File selected:",
        file.name,
        "Type:",
        file.type,
        "Size:",
        file.size
      );

      // Check file type
      const allowedTypes = [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "text/plain",
      ];
      if (!allowedTypes.includes(file.type)) {
        console.log("Invalid file type:", file.type);
        toast.error("Please upload a PDF, DOCX, or TXT file");
        return;
      }

      // Check file size (16MB limit)
      const maxSize = 16 * 1024 * 1024; // 16MB in bytes
      if (file.size > maxSize) {
        console.log("File too large:", file.size);
        toast.error("File size must be less than 16MB");
        return;
      }

      const formData = new FormData();
      formData.append("file", file);

      setIsUploading(true);
      setUploadProgress(0);

      // Create axios instance with base configuration
      const api = axios.create({
        baseURL: "http://localhost:5000",
        timeout: 120000, // 2 minute timeout
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      try {
        console.log("Starting upload to:", "http://localhost:5000/api/upload");
        const response = await api.post("/api/upload", formData, {
          onUploadProgress: (progressEvent) => {
            const percentCompleted = Math.round(
              (progressEvent.loaded * 100) / progressEvent.total
            );
            setUploadProgress(percentCompleted);
            console.log("Upload progress:", percentCompleted);
          },
        });

        console.log("Upload response:", response.data);

        if (response.data.error) {
          throw new Error(response.data.error);
        }

        toast.success("File uploaded successfully!");
        if (onUploadComplete) {
          onUploadComplete(response.data);
        }
      } catch (error) {
        console.error("Upload error details:", {
          message: error.message,
          response: error.response?.data,
          status: error.response?.status,
          headers: error.response?.headers,
          code: error.code,
          stack: error.stack,
        });

        let errorMessage = "Failed to upload file. Please try again.";

        if (error.code === "ECONNABORTED") {
          errorMessage =
            "Upload timed out. Please try again with a smaller file.";
        } else if (error.code === "ERR_NETWORK") {
          errorMessage =
            "Network error. Please check if the backend server is running.";
        } else if (error.response?.data?.error) {
          errorMessage = error.response.data.error;
        } else if (error.message) {
          errorMessage = error.message;
        }

        toast.error(errorMessage);
      } finally {
        setIsUploading(false);
        setUploadProgress(0);
      }
    },
    [onUploadComplete]
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
    disabled: isUploading,
  });

  return (
    <div className="w-full max-w-3xl mx-auto">
      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors
          ${
            isDragActive
              ? "border-blue-500 bg-blue-50"
              : "border-gray-300 hover:border-blue-400"
          }
          ${isUploading ? "opacity-50 cursor-not-allowed" : ""}`}
      >
        <input {...getInputProps()} />
        <div className="space-y-4">
          <div className="flex justify-center">
            <svg
              className={`w-12 h-12 ${
                isDragActive ? "text-blue-500" : "text-gray-400"
              }`}
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
              />
            </svg>
          </div>
          {isUploading ? (
            <div className="text-gray-600">
              <p className="font-medium">Uploading... {uploadProgress}%</p>
              <div className="w-full bg-gray-200 rounded-full h-2.5 mt-2">
                <div
                  className="bg-blue-600 h-2.5 rounded-full transition-all duration-300"
                  style={{ width: `${uploadProgress}%` }}
                ></div>
              </div>
              <p className="text-sm mt-2">
                Please wait while we process your file
              </p>
            </div>
          ) : (
            <div className="text-gray-600">
              <p className="font-medium">
                {isDragActive
                  ? "Drop the file here"
                  : "Drag and drop your contract here"}
              </p>
              <p className="text-sm">or click to select a file</p>
              <p className="text-xs mt-2">
                Supported formats: PDF, DOCX, TXT (max 16MB)
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default FileUpload;
