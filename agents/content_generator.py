"""Content Generator Agent for brand-consistent social media content.

This agent generates creative, brand-aligned content based on trends,
audience insights, and voice guidelines.
"""

from typing import Any, Dict, Optional, List
from datetime import datetime
from .base_agent import BaseAgent
import json


class ContentGeneratorAgent(BaseAgent):
    """Agent for generating brand-consistent social media content.
    
    Attributes:
        platform: Target platform for content (twitter, tiktok, instagram)
        brand_voice: Brand personality and tone guidelines
        content_templates: Templates for content generation
    """
    
    def __init__(
        self,
        platform: str = "twitter",
        brand_voice: Optional[Dict[str, str]] = None,
        config: Optional[Dict[str, Any]] = None,
    ):
        """Initialize the Content Generator Agent.
        
        Args:
            platform: Target social media platform
            brand_voice: Dictionary with brand personality traits
            config: Optional configuration
        """
        super().__init__(
            name="ContentGenerator",
            description=f"Generates brand-consistent content for {platform}",
            config=config or {},
        )
        self.platform = platform
        self.brand_voice = brand_voice or {
            "tone": "professional",
            "style": "conversational",
            "values": "innovation, transparency, excellence",
        }
        self.content_templates = self._initialize_templates()
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate content based on input parameters.
        
        Args:
            input_data: Contains 'topic', 'tone', 'style' and optional 'hashtags'
            
        Returns:
            Generated content with metadata
        """
        topic = input_data.get("topic", "")
        tone = input_data.get("tone") or self.brand_voice.get("tone")
        style = input_data.get("style") or self.brand_voice.get("style")
        hashtags = input_data.get("hashtags", [])
        
        content = await self._generate_content(topic, tone, style)
        optimized = await self._optimize_for_platform(content)
        with_hashtags = f"{optimized}\n\n{' '.join(hashtags)}" if hashtags else optimized
        
        result = {
            "status": "success",
            "platform": self.platform,
            "content": with_hashtags,
            "topic": topic,
            "tone": tone,
            "style": style,
            "length": len(with_hashtags),
            "timestamp": datetime.now().isoformat(),
        }
        
        self.add_to_memory("assistant", json.dumps(result))
        return result
    
    async def process(self, message: str) -> str:
        """Process content generation request.
        
        Args:
            message: User request for content generation
            
        Returns:
            Generated content
        """
        self.add_to_memory("user", message)
        
        result = await self.execute({"topic": message})
        return result["content"]
    
    async def _generate_content(self, topic: str, tone: str, style: str) -> str:
        """Generate content based on topic and style.
        
        Args:
            topic: Content topic
            tone: Tone of voice
            style: Writing style
            
        Returns:
            Generated content
        """
        # Mock content generation (would use LLM in production)
        template = self.content_templates.get(style, "")
        
        content = f"""{template}

Topic: {topic}
Tone: {tone}
Brand Voice: {self.brand_voice.get('tone')}

Generated content for social media engagement."""
        
        return content
    
    async def _optimize_for_platform(self, content: str) -> str:
        """Optimize content for the target platform.
        
        Args:
            content: Original content
            
        Returns:
            Optimized content
        """
        # Platform-specific optimizations
        if self.platform == "twitter":
            # Limit to 280 characters
            content = content[:280]
        elif self.platform == "tiktok":
            # Add engaging hooks
            content = f"Hook: {content}"
        elif self.platform == "instagram":
            # Add visual descriptions
            content = f"[Visual: infographic]\n{content}"
        
        return content
    
    def _initialize_templates(self) -> Dict[str, str]:
        """Initialize content templates.
        
        Returns:
            Dictionary of content templates by style
        """
        return {
            "conversational": "Let's talk about this...",
            "educational": "Did you know?",
            "inspirational": "Here's something that caught our attention...",
            "promotional": "Check out what we've been working on...",
            "news": "Breaking: Latest updates",
        }
    
    async def generate_carousel(self, topics: List[str], style: str = "conversational") -> List[str]:
        """Generate multiple content pieces for a carousel.
        
        Args:
            topics: List of topics for carousel
            style: Content style
            
        Returns:
            List of content pieces
        """
        carousel_content = []
        for topic in topics:
            content = await self._generate_content(topic, self.brand_voice.get("tone"), style)
            carousel_content.append(content)
        
        return carousel_content
    
    def adapt_voice(self, new_voice: Dict[str, str]) -> None:
        """Adapt brand voice based on feedback.
        
        Args:
            new_voice: Updated brand voice guidelines
        """
        self.brand_voice.update(new_voice)
        self.add_to_memory("system", f"Brand voice adapted: {json.dumps(new_voice)}")
