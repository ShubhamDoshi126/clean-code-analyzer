import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Progress } from './ui/progress';
import { Badge } from './ui/badge';
import { Separator } from './ui/separator';

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

interface ResultsDisplayProps {
  result: AnalysisResult;
  onReset: () => void;
}

export function ResultsDisplay({ result, onReset }: ResultsDisplayProps) {
  const { overall_score, breakdown, recommendations } = result;
  
  // Calculate color based on score
  const getScoreColor = (score: number, max: number) => {
    const percentage = (score / max) * 100;
    if (percentage >= 80) return 'bg-green-500';
    if (percentage >= 60) return 'bg-yellow-500';
    return 'bg-red-500';
  };
  
  // Calculate category color
  const getCategoryColor = (score: number, max: number) => {
    const percentage = (score / max) * 100;
    if (percentage >= 80) return 'bg-green-100 text-green-800';
    if (percentage >= 60) return 'bg-yellow-100 text-yellow-800';
    return 'bg-red-100 text-red-800';
  };

  return (
    <Card className="w-full max-w-3xl mx-auto">
      <CardHeader>
        <div className="flex justify-between items-center">
          <div>
            <CardTitle>Code Analysis Results</CardTitle>
            <CardDescription>
              Detailed breakdown of code quality metrics
            </CardDescription>
          </div>
          <div className="text-center">
            <div className="text-4xl font-bold">{overall_score}</div>
            <div className="text-sm text-gray-500">Overall Score</div>
          </div>
        </div>
      </CardHeader>
      <CardContent className="space-y-6">
        <div>
          <h3 className="text-lg font-medium mb-3">Score Breakdown</h3>
          <div className="space-y-4">
            <div className="space-y-2">
              <div className="flex justify-between">
                <span>Naming Conventions</span>
                <Badge variant="outline" className={getCategoryColor(breakdown.naming, 10)}>
                  {breakdown.naming}/10
                </Badge>
              </div>
              <Progress value={(breakdown.naming / 10) * 100} className={getScoreColor(breakdown.naming, 10)} />
            </div>
            
            <div className="space-y-2">
              <div className="flex justify-between">
                <span>Function Length & Modularity</span>
                <Badge variant="outline" className={getCategoryColor(breakdown.modularity, 20)}>
                  {breakdown.modularity}/20
                </Badge>
              </div>
              <Progress value={(breakdown.modularity / 20) * 100} className={getScoreColor(breakdown.modularity, 20)} />
            </div>
            
            <div className="space-y-2">
              <div className="flex justify-between">
                <span>Comments & Documentation</span>
                <Badge variant="outline" className={getCategoryColor(breakdown.comments, 20)}>
                  {breakdown.comments}/20
                </Badge>
              </div>
              <Progress value={(breakdown.comments / 20) * 100} className={getScoreColor(breakdown.comments, 20)} />
            </div>
            
            <div className="space-y-2">
              <div className="flex justify-between">
                <span>Formatting & Indentation</span>
                <Badge variant="outline" className={getCategoryColor(breakdown.formatting, 15)}>
                  {breakdown.formatting}/15
                </Badge>
              </div>
              <Progress value={(breakdown.formatting / 15) * 100} className={getScoreColor(breakdown.formatting, 15)} />
            </div>
            
            <div className="space-y-2">
              <div className="flex justify-between">
                <span>Reusability & DRY</span>
                <Badge variant="outline" className={getCategoryColor(breakdown.reusability, 15)}>
                  {breakdown.reusability}/15
                </Badge>
              </div>
              <Progress value={(breakdown.reusability / 15) * 100} className={getScoreColor(breakdown.reusability, 15)} />
            </div>
            
            <div className="space-y-2">
              <div className="flex justify-between">
                <span>Best Practices</span>
                <Badge variant="outline" className={getCategoryColor(breakdown.best_practices, 20)}>
                  {breakdown.best_practices}/20
                </Badge>
              </div>
              <Progress value={(breakdown.best_practices / 20) * 100} className={getScoreColor(breakdown.best_practices, 20)} />
            </div>
          </div>
        </div>
        
        <Separator />
        
        <div>
          <h3 className="text-lg font-medium mb-3">Recommendations</h3>
          <ul className="space-y-2 list-disc pl-5">
            {recommendations.map((recommendation, index) => (
              <li key={index} className="text-gray-700">{recommendation}</li>
            ))}
          </ul>
        </div>
        
        <div className="pt-4">
          <button
            onClick={onReset}
            className="text-blue-600 hover:text-blue-800 font-medium"
          >
            ← Analyze another file
          </button>
        </div>
      </CardContent>
    </Card>
  );
}
