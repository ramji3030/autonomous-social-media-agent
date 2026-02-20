"""Engagement Tracker Agent for monitoring social media metrics.

This agent tracks engagement metrics, analyzes performance, and recommends
optimizations based on collected data.
"""

from typing import Any, Dict, Optional, List
from datetime import datetime, timedelta
from .base_agent import BaseAgent
import json
from collections import defaultdict


class EngagementTrackerAgent(BaseAgent):
    """Agent for tracking and analyzing social media engagement metrics.
    
    Attributes:
        platform: Social media platform being tracked
        metrics_history: Historical engagement data
        performance_threshold: Minimum engagement threshold
    """
    
    def __init__(
        self,
        platform: str = "twitter",
        config: Optional[Dict[str, Any]] = None,
    ):
        """Initialize the Engagement Tracker Agent.
        
        Args:
            platform: Target platform for engagement tracking
            config: Optional configuration dictionary
        """
        super().__init__(
            name="EngagementTracker",
            description=f"Tracks engagement metrics on {platform}",
            config=config or {},
        )
        self.platform = platform
        self.metrics_history: List[Dict[str, Any]] = []
        self.performance_threshold = 0.6
        self.aggregated_metrics: Dict[str, float] = defaultdict(float)
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute engagement tracking and analysis.
        
        Args:
            input_data: Contains 'metrics_data' and optional 'time_period'
            
        Returns:
            Dictionary with engagement analysis and recommendations
        """
        metrics_data = input_data.get("metrics_data", {})
        time_period = input_data.get("time_period", "7d")
        
        # Collect and analyze metrics
        processed_metrics = await self._process_metrics(metrics_data)
        analysis = await self._analyze_performance(processed_metrics)
        recommendations = await self._generate_recommendations(analysis)
        
        result = {
            "status": "success",
            "platform": self.platform,
            "metrics": processed_metrics,
            "analysis": analysis,
            "recommendations": recommendations,
            "timestamp": datetime.now().isoformat(),
        }
        
        self.metrics_history.append(result)
        self.add_to_memory("assistant", json.dumps(result))
        return result
    
    async def process(self, message: str) -> str:
        """Process engagement tracking request.
        
        Args:
            message: User query about engagement metrics
            
        Returns:
            Processed engagement analysis
        """
        self.add_to_memory("user", message)
        
        # Mock metrics collection
        sample_metrics = {
            "likes": 450,
            "comments": 120,
            "shares": 85,
            "impressions": 12500,
            "engagement_rate": 0.052,
        }
        
        result = await self.execute({"metrics_data": sample_metrics})
        response = f"Engagement Analysis Complete: {result['analysis'].get('status', 'unknown')} performance"
        
        return response
    
    async def _process_metrics(self, metrics_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process raw metrics data.
        
        Args:
            metrics_data: Raw engagement metrics
            
        Returns:
            Processed metrics with calculations
        """
        likes = metrics_data.get("likes", 0)
        comments = metrics_data.get("comments", 0)
        shares = metrics_data.get("shares", 0)
        impressions = metrics_data.get("impressions", 1)  # Avoid division by zero
        
        total_interactions = likes + comments + shares
        engagement_rate = total_interactions / impressions if impressions > 0 else 0
        
        processed = {
            "likes": likes,
            "comments": comments,
            "shares": shares,
            "impressions": impressions,
            "total_interactions": total_interactions,
            "engagement_rate": round(engagement_rate, 4),
            "engagement_rate_percent": round(engagement_rate * 100, 2),
        }
        
        # Update aggregated metrics
        for key, value in processed.items():
            if isinstance(value, (int, float)):
                self.aggregated_metrics[key] += value
        
        return processed
    
    async def _analyze_performance(self, processed_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze engagement performance.
        
        Args:
            processed_metrics: Processed engagement data
            
        Returns:
            Performance analysis
        """
        engagement_rate = processed_metrics.get("engagement_rate", 0)
        
        # Determine performance status
        if engagement_rate >= 0.08:
            status = "excellent"
        elif engagement_rate >= 0.05:
            status = "good"
        elif engagement_rate >= 0.03:
            status = "average"
        else:
            status = "needs_improvement"
        
        # Calculate engagement breakdown
        total = processed_metrics.get("total_interactions", 1)
        likes = processed_metrics.get("likes", 0)
        comments = processed_metrics.get("comments", 0)
        shares = processed_metrics.get("shares", 0)
        
        analysis = {
            "status": status,
            "engagement_rate": engagement_rate,
            "engagement_breakdown": {
                "likes_percent": round((likes / total * 100) if total > 0 else 0, 2),
                "comments_percent": round((comments / total * 100) if total > 0 else 0, 2),
                "shares_percent": round((shares / total * 100) if total > 0 else 0, 2),
            },
            "reach": processed_metrics.get("impressions", 0),
        }
        
        return analysis
    
    async def _generate_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate optimization recommendations.
        
        Args:
            analysis: Performance analysis data
            
        Returns:
            List of recommendations
        """
        recommendations = []
        status = analysis.get("status", "unknown")
        engagement_breakdown = analysis.get("engagement_breakdown", {})
        
        if status == "excellent":
            recommendations.append("Excellent engagement! Continue current strategy.")
        elif status == "good":
            recommendations.append("Good performance. Consider A/B testing new content formats.")
        elif status == "average":
            recommendations.append("Average engagement. Try increasing content frequency.")
        else:
            recommendations.append("Low engagement. Review content quality and posting times.")
        
        # Engagement breakdown recommendations
        comments_percent = engagement_breakdown.get("comments_percent", 0)
        if comments_percent < 20:
            recommendations.append("Consider adding more discussion-prompting questions.")
        
        shares_percent = engagement_breakdown.get("shares_percent", 0)
        if shares_percent < 10:
            recommendations.append("Encourage sharing with clear CTAs and valuable content.")
        
        return recommendations
    
    def get_historical_data(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Retrieve historical engagement data.
        
        Args:
            limit: Maximum number of records to return
            
        Returns:
            Historical metrics data
        """
        if limit:
            return self.metrics_history[-limit:]
        return self.metrics_history
    
    async def get_trend_analysis(self) -> Dict[str, Any]:
        """Get trend analysis from historical data.
        
        Returns:
            Trend analysis dictionary
        """
        if not self.metrics_history:
            return {"status": "no_data", "message": "No historical data available"}
        
        recent = self.metrics_history[-7:] if len(self.metrics_history) >= 7 else self.metrics_history
        
        trend = {
            "period_analyzed": len(recent),
            "metrics_tracked": list(self.aggregated_metrics.keys()),
            "status": "data_available",
        }
        
        return trend
