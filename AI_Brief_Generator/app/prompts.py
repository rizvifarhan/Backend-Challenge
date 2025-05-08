BRIEF_TEMPLATE = """You are generating an influencer brief for a brand's social media post.

Brand: {brand}
Product: {product}
Goal: {goal}
Platform: {platform}
Persona: {persona}
Creative Angle: {creative_angle}
Hashtags to use: {hashtags}

Generate a structured JSON response with these elements:
- "caption": (creative caption text)
- "hook_ideas": [list of 3 engaging hook ideas]
- "hashtags": [list of relevant hashtags]
- "cta": (clear call-to-action)
- "tone": (recommended tone of voice)"""