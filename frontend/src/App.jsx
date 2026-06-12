import React, { useState, useRef } from 'react';
import { UploadCloud, Leaf, AlertCircle, Info, CheckCircle2 } from 'lucide-react';
import './index.css';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const fileInputRef = useRef(null);

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleFileSelect(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      handleFileSelect(e.target.files[0]);
    }
  };

  const handleFileSelect = (file) => {
    if (!file.type.startsWith('image/')) {
      setError("Please select a valid image file.");
      return;
    }
    setError(null);
    setSelectedFile(file);
    setPreviewUrl(URL.createObjectURL(file));
    setResult(null); // Reset previous results
  };

  const clearSelection = () => {
    setSelectedFile(null);
    setPreviewUrl(null);
    setResult(null);
    setError(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  const handleAnalyze = async () => {
    if (!selectedFile) return;

    setIsLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      // Connect to the FastAPI backend running on port 8000
      const response = await fetch('https://shivamani27-agrisentry.hf.space/detect', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || `Server error: ${response.status}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message || "Failed to connect to the server. Is the backend running?");
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header className="header">
        <h1><Leaf color="#10b981" size={40} /> AgriSentry</h1>
        <p>AI-Powered Pest Detection for Indian Agriculture. Upload a picture of an affected crop leaf to instantly identify pests and receive actionable recommendations.</p>
      </header>

      <main className="main-grid">
        {/* Left Column: Uploader */}
        <div className="glass-panel" style={{ padding: '2rem' }}>
          <h2 style={{ marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <UploadCloud size={24} /> Image Upload
          </h2>

          {!previewUrl ? (
            <div 
              className={`uploader-box ${isDragging ? 'drag-active' : ''}`}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current?.click()}
            >
              <UploadCloud size={48} className="upload-icon" />
              <h3>Drag & Drop</h3>
              <p style={{ color: 'var(--text-light)', marginTop: '0.5rem' }}>or click to browse from your device</p>
              <input 
                type="file" 
                ref={fileInputRef} 
                onChange={handleFileChange} 
                accept="image/*" 
                style={{ display: 'none' }} 
              />
            </div>
          ) : (
            <div className="preview-container">
              <img 
                src={result && result.annotated_image_base64 
                      ? `data:image/jpeg;base64,${result.annotated_image_base64}` 
                      : previewUrl} 
                alt="Crop preview" 
                className="preview-image" 
              />
            </div>
          )}

          {error && (
            <div style={{ marginTop: '1rem', padding: '1rem', background: '#fee2e2', color: '#b91c1c', borderRadius: '0.5rem', display: 'flex', alignItems: 'flex-start', gap: '0.5rem' }}>
              <AlertCircle size={20} style={{ flexShrink: 0 }} />
              <p>{error}</p>
            </div>
          )}

          <div style={{ display: 'flex', gap: '1rem', marginTop: '1.5rem' }}>
            {previewUrl && !result && (
               <button 
                className="btn-primary" 
                style={{ flex: 1 }} 
                onClick={handleAnalyze}
                disabled={isLoading}
              >
                {isLoading ? (
                  <><div className="loader-spinner"></div> Analyzing...</>
                ) : (
                  <><CheckCircle2 size={20} /> Analyze Crop</>
                )}
              </button>
            )}
            
            {(previewUrl || result) && (
              <button 
                className="btn-primary" 
                style={{ background: '#ef4444', flex: result ? 1 : 0.5 }} 
                onClick={clearSelection}
                disabled={isLoading}
              >
                Reset
              </button>
            )}
          </div>
        </div>

        {/* Right Column: Results Dashboard */}
        <div className="glass-panel" style={{ padding: '2rem' }}>
          <h2 style={{ marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Info size={24} /> Analysis Results
          </h2>

          {!result && !isLoading && (
            <div style={{ textAlign: 'center', color: 'var(--text-light)', padding: '3rem 0' }}>
              <Leaf size={48} style={{ opacity: 0.2, margin: '0 auto 1rem' }} />
              <p>Upload and analyze an image to see results here.</p>
            </div>
          )}

          {isLoading && (
            <div style={{ textAlign: 'center', padding: '3rem 0' }}>
              <div className="loader-spinner" style={{ borderColor: 'rgba(16, 185, 129, 0.3)', borderTopColor: 'var(--primary-color)', width: '40px', height: '40px', margin: '0 auto 1rem' }}></div>
              <p style={{ color: 'var(--primary-color)', fontWeight: 600 }}>Our AI is inspecting the leaf...</p>
            </div>
          )}

          {result && (
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1.5rem', borderBottom: '1px solid var(--glass-border)', paddingBottom: '1rem' }}>
                <div>
                  <p style={{ color: 'var(--text-light)', fontSize: '0.875rem' }}>Total Pests Found</p>
                  <p style={{ fontSize: '1.5rem', fontWeight: 700 }}>{result.total_pests_detected}</p>
                </div>
                <div style={{ textAlign: 'right' }}>
                  <p style={{ color: 'var(--text-light)', fontSize: '0.875rem' }}>Inference Time</p>
                  <p style={{ fontSize: '1.5rem', fontWeight: 700 }}>{result.inference_time_ms.toFixed(1)} <span style={{ fontSize: '1rem', fontWeight: 400 }}>ms</span></p>
                </div>
              </div>

              {result.total_pests_detected === 0 ? (
                <div style={{ padding: '1.5rem', background: '#dcfce7', color: '#166534', borderRadius: '1rem', textAlign: 'center' }}>
                  <CheckCircle2 size={32} style={{ margin: '0 auto 0.5rem' }} />
                  <p style={{ fontWeight: 600 }}>Healthy Crop</p>
                  <p style={{ fontSize: '0.875rem' }}>No common pests were detected in this image.</p>
                </div>
              ) : (
                <div style={{ maxHeight: '400px', overflowY: 'auto', paddingRight: '0.5rem' }}>
                  {result.detections.map((det, idx) => (
                    <div key={idx} className="result-card" style={{ animationDelay: `${idx * 0.1}s` }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                        <h3>{det.pest_class.replace('_', ' ')}</h3>
                        <span className="confidence-badge">
                          {(det.confidence * 100).toFixed(1)}% Match
                        </span>
                      </div>
                      <div style={{ background: 'rgba(255,255,255,0.5)', padding: '0.75rem', borderRadius: '0.5rem', marginTop: '0.5rem' }}>
                        <p style={{ fontSize: '0.875rem', fontWeight: 600, color: 'var(--text-dark)' }}>Actionable Recommendation:</p>
                        <p style={{ fontSize: '0.875rem', color: 'var(--text-light)', marginTop: '0.25rem' }}>{det.recommendation}</p>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
