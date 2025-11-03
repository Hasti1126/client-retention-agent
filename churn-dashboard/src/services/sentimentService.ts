export const sentimentService = {
  analyzeSentiment: (text: string): { score: number; label: string } => {
    // Simple sentiment analysis (can integrate with real NLP API)
    const positive = ['great', 'excellent', 'good', 'happy', 'satisfied', 'love', 'perfect', 'amazing', 'wonderful'];
    const negative = ['bad', 'terrible', 'poor', 'angry', 'frustrated', 'hate', 'worst', 'awful', 'horrible'];
    
    const lowerText = text.toLowerCase();
    const positiveCount = positive.filter(word => lowerText.includes(word)).length;
    const negativeCount = negative.filter(word => lowerText.includes(word)).length;
    
    const score = (positiveCount - negativeCount) / Math.max(positiveCount + negativeCount, 1);
    const normalized = (score + 1) / 2; // Normalize to 0-1
    
    let label = 'neutral';
    if (normalized > 0.6) label = 'positive';
    if (normalized < 0.4) label = 'negative';
    
    return { score: normalized, label };
  },

  analyzeCommunicationSentiment: (communications: any[]): { trend: string; avgScore: number } => {
    if (!communications.length) return { trend: 'stable', avgScore: 0.5 };
    
    const scores = communications.map(comm => sentimentService.analyzeSentiment(comm.text).score);
    const avgScore = scores.reduce((a, b) => a + b, 0) / scores.length;
    
    const recentAvg = scores.slice(-3).reduce((a, b) => a + b, 0) / Math.min(3, scores.length);
    const trend = recentAvg > avgScore ? 'improving' : recentAvg < avgScore ? 'declining' : 'stable';
    
    return { trend, avgScore };
  },

  getSentimentEmoji: (score: number): string => {
    if (score > 0.7) return '😊';
    if (score > 0.5) return '🙂';
    if (score > 0.3) return '😐';
    if (score > 0.1) return '😕';
    return '😞';
  },

  getSentimentColor: (score: number): string => {
    if (score > 0.7) return 'text-green-600';
    if (score > 0.5) return 'text-blue-600';
    if (score > 0.3) return 'text-yellow-600';
    if (score > 0.1) return 'text-orange-600';
    return 'text-red-600';
  }
};
