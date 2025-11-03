#\!/usr/bin/env python3
"""
Strands Voice Agent Usage Example
British female voices for INFJ ADHD communication
"""

from strands_voice_agent import StrandsVoiceAgent

def main():
    # Initialize with your Cartesia API key
    agent = StrandsVoiceAgent("sk_car_J5wk4g3bzwyggQ6uBftGMC")
    
    # Test with strategic direction
    user_input = "I envision a system that helps creative people collaborate intuitively"
    result = agent.process_voice_command(user_input)
    
    print(f"🗣️  Response: {result['text_response']}")
    if result['audio_data']:
        print(f"🎵 Audio: {len(result['audio_data'])} bytes of British female speech")
    else:
        print("🎵 Audio: Synthesis failed (check API key)")
    print(f"🎯 Voice Style: {result['voice_style']}")

if __name__ == "__main__":
    main()