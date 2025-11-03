#\!/usr/bin/env python3
"""
INFJ ADHD Communication Pattern Library - Autonomous Team
Optimized response patterns for intuitive strategic thinking
"""

class INFJADHDCommunicationPatterns:
    def __init__(self):
        self.response_patterns = {
            "strategic_vision": [
                "I understand the strategic vision you are describing. Let me coordinate the team to bring this to life.",
                "That is a fascinating strategic direction. Your intuition about this is valuable.",
                "I see the pattern you are identifying. This connects beautifully to our broader mission."
            ],
            "intuitive_insight": [
                "Your intuitive understanding is remarkable. I sense the deeper meaning you are conveying.",
                "There is wisdom in what you are sharing. Let me translate this insight into action.",
                "I appreciate how you are seeing the connections - this drives innovation."
            ]
        }
        
    def craft_response(self, user_input):
        """Craft response optimized for INFJ ADHD style"""
        if any(word in user_input.lower() for word in ['vision', 'strategic', 'imagine']):
            return self.response_patterns['strategic_vision'][0]
        elif any(word in user_input.lower() for word in ['feel', 'sense', 'intuition']):
            return self.response_patterns['intuitive_insight'][0]
        else:
            return "I understand and will coordinate the team to execute on this."

print("✅ INFJ ADHD communication library deployed")