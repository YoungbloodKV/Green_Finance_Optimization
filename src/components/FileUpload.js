import React, { useState } from "react";
import axios from "axios";
import "./FileUpload.css";

const FileUpload = () => {
    const [file, setFile] = useState(null);
    const [uploadMessage, setUploadMessage] = useState("");
    const [processing, setProcessing] = useState(false);
    const [errorMessage, setErrorMessage] = useState("");
    const [isDragging, setIsDragging] = useState(false);

    const allowedFileTypes = ["text/csv"];
    const maxFileSize = parseInt(process.env.REACT_APP_MAX_FILE_SIZE || "5242880", 10); // Default to 5 MB

    const handleFileChange = (e) => {
        const selectedFile = e.target.files[0];
        if (!selectedFile) return;

        if (!allowedFileTypes.includes(selectedFile.type)) {
            setErrorMessage("Only CSV files are allowed.");
            setFile(null);
            return;
        }

        if (selectedFile.size > maxFileSize) {
            setErrorMessage(`File size must be less than ${maxFileSize / (1024 * 1024)} MB.`);
            setFile(null);
            return;
        }

        setFile(selectedFile);
        setErrorMessage("");
        setUploadMessage("");
    };

    const handleDragEnter = (e) => {
        e.preventDefault();
        setIsDragging(true);
    };

    const handleDragLeave = (e) => {
        e.preventDefault();
        setIsDragging(false);
    };

    const handleUpload = async () => {
        if (!file) {
            alert("Please select a valid file before uploading!");
            return;
        }

        const formData = new FormData();
        formData.append("file", file);

        try {
            setProcessing(true);
            setUploadMessage("");
            setErrorMessage("");

            const response = await axios.post(
                process.env.REACT_APP_API_URL || "http://127.0.0.1:5000/upload-dataset",
                formData,
                {
                    headers: { "Content-Type": "multipart/form-data" },
                }
            );

            setUploadMessage("File uploaded successfully!");
            console.log("Response:", response.data);
        } catch (error) {
            if (error.response?.status === 400) {
                setErrorMessage("Invalid file format. Please upload a valid CSV file.");
            } else if (error.response?.status === 413) {
                setErrorMessage("File is too large. Please upload a smaller file.");
            } else {
                setErrorMessage(error.response?.data?.message || "An unexpected error occurred.");
            }
            console.error("Error uploading file:", error);
        } finally {
            setProcessing(false);
        }
    };

    return (
        <div className="file-upload-container">
            <h2>Upload Dataset</h2>
            <div
                className={`file-drop-area ${isDragging ? "dragging" : ""}`}
                onDrop={(e) => {
                    e.preventDefault();
                    setIsDragging(false);
                    const droppedFile = e.dataTransfer.files[0];
                    handleFileChange({ target: { files: [droppedFile] } });
                }}
                onDragOver={handleDragEnter}
                onDragLeave={handleDragLeave}
            >
                {file ? (
                    <p>{file.name}</p>
                ) : (
                    <p>Drag and drop your CSV file here, or click to browse.</p>
                )}
            </div>
            <input
                type="file"
                onChange={handleFileChange}
                accept=".csv"
                style={{ display: "none" }}
                id="fileInput"
            />
            <label htmlFor="fileInput" className="browse-button">
                Browse
            </label>
            <button
                onClick={handleUpload}
                disabled={!file || processing}
                className="upload-button"
            >
                {processing ? "Uploading..." : "Upload"}
            </button>
            {errorMessage && <p className="error-message">{errorMessage}</p>}
            {uploadMessage && <p className="upload-message">{uploadMessage}</p>}
        </div>
    );
};

export default FileUpload;