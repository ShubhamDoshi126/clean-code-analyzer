import { useState } from 'react';
import { FileUpload } from './components/FileUpload';
import { ResultsDisplay } from './components/ResultsDisplay';
import './App.css';

interface AnalysisResult {
  overall_score: number;
  breakdown: {
    naming: number;
    modularity: number;
    comments: number;
    formatting: number;
    reusability: number;
    best_practices: number;
  };
  recommendations: string[];
}

function App() {
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);

  const handleFileAnalyzed = (result: AnalysisResult) => {
    setAnalysisResult(result);
  };

  const handleReset = () => {
    setAnalysisResult(null);
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Code Quality Analyzer</h1>
          <p className="mt-2 text-lg text-gray-600">
            Analyze your React or FastAPI code for clean code practices
          </p>
        </div>

        <div className="mt-10">
          {analysisResult ? (
            <ResultsDisplay result={analysisResult} onReset={handleReset} />
          ) : (
            <FileUpload onFileAnalyzed={handleFileAnalyzed} />
          )}
        </div>

        <footer className="mt-16 text-center text-sm text-gray-500">
          <p>Supports JavaScript (.js), React (.jsx), and Python (.py) files</p>
        </footer>
      </div>
    </div>
  );
}

export default App;
