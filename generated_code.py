import re
from typing import Dict, Optional
from PIL import Image, ImageDraw

def stage_1_extraction(user_input: str) -> Dict[str, str]:
    """
    Extract product and audience from natural language or pipe-separated input.
    Handles various prepositions and common patterns.

    Args:
        user_input (str): Input string to extract product and audience from.

    Returns:
        Dict[str, str]: Dictionary containing extracted product and audience.
        Raises ValueError if input cannot be extracted.

    """
    try:
        # Clean the input (lowercase for easier matching, but preserve original for output)
        original_input = user_input
        cleaned_input = user_input.lower()
        
        # Try pipe format first
        if '|' in user_input:
            parts = user_input.split('|')
            if len(parts) == 2:
                return {'product': parts[0].strip(), 'audience': parts[1].strip()}
        
        # More flexible pattern matching for natural language
        patterns = [
            # Pattern: "I want to sell X to Y"
            r"(?:i want to sell|sell)\s+(.+?)\s+to\s+(.+)",
            
            # Pattern: "I want to sell X for Y"
            r"(?:i want to sell|sell)\s+(.+?)\s+for\s+(.+)",
            
            # Pattern: "sell X to Y" (without "I want to")
            r"sell\s+(.+?)\s+to\s+(.+)",
            
            # Pattern: "sell X for Y"
            r"sell\s+(.+?)\s+for\s+(.+)",
            
            # Pattern: "X for Y"
            r"(.+?)\s+for\s+(.+)",
            
            # Pattern: "X to Y"
            r"(.+?)\s+to\s+(.+)",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, cleaned_input, re.IGNORECASE)
            if match:
                product = match.group(1).strip()
                audience = match.group(2).strip()
                
                # Basic validation: both fields should not be empty
                if product and audience:
                    return {'product': product, 'audience': audience}
        
        # If no pattern matches, try simple word extraction
        # Remove common phrases
        temp = cleaned_input
        for phrase in ["i want to sell ", "sell ", "please sell "]:
            temp = temp.replace(phrase, "")
        
        # Look for common prepositions as separators
        for prep in [" to ", " for ", " at ", " near "]:
            if prep in temp:
                parts = temp.split(prep)
                if len(parts) == 2:
                    product = parts[0].strip()
                    audience = parts[1].strip()
                    if product and audience:
                        return {'product': product, 'audience': audience}
        
        # Last resort: assume last word is audience, rest is product
        words = cleaned_input.split()
        if len(words) >= 2:
            # Remove common verbs and prepositions
            filtered_words = [w for w in words if w not in ['i', 'want', 'to', 'sell', 'for', 'of', 'the', 'a', 'an']]
            if len(filtered_words) >= 2:
                audience = filtered_words[-1]
                product = ' '.join(filtered_words[:-1])
                return {'product': product, 'audience': audience}
        
        # If all else fails, raise error with clear instruction
        raise ValueError(f"Invalid format. Please use one of these formats:\n"
                          f"  - 'product|audience' (e.g., 'pickle|neighbours')\n"
                          f"  - 'I want to sell X to Y' (e.g., 'I want to sell pickle to neighbours')\n"
                          f"  - 'sell X for Y' (e.g., 'sell shoes for marathon runners')\n"
                          f"  - 'I want to sell X for Y' (e.g., 'I want to sell ice cream for kids')")
    
    except Exception as e:
        print(f"Error in stage 1 extraction: {str(e)}")
        return None

def stage_2_ideation(product: str, audience: str) -> Dict[str, list[str]]:
    """
    Generate marketing ideas based on product and audience.

    Args:
        product (str): Product to generate ideas for.
        audience (str): Audience to generate ideas for.

    Returns:
        Dict[str, list[str]]: Dictionary containing marketing ideas for the product and audience.

    """
    ideas = {
        product: [
            f"Create a neighborhood tasting event for {audience}",
            f"Develop a '{product} of the month' subscription for {audience}",
            f"Design custom {product} jars with {audience} names",
            f"Offer free samples of {product} to {audience} at community gatherings",
            f"Launch a referral program for {audience} to buy {product}",
            f"Start a social media campaign targeting {audience} to promote {product}",
            f"Host a {product}-making workshop for interested {audience}",
        ]
    }
    return ideas

def stage_3_rendering(ideas: Dict[str, list[str]]) -> Optional[Image]:
    """
    Render ideas as an image using default font.

    Args:
        ideas (Dict[str, list[str]]): Dictionary containing marketing ideas for the product and audience.

    Returns:
        Optional[Image]: Rendered image or None if rendering fails.

    """
    try:
        # Create a larger image to accommodate more text
        img = Image.new('RGB', (900, 700), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        
        y_pos = 50
        line_number = 1
        
        # Draw title
        for key, value in ideas.items():
            draw.text((50, y_pos), f"📊 MARKETING IDEAS FOR: {key.upper()}", fill=(0, 0, 255))
            y_pos += 60
            
            # Draw each idea with numbering
            for i, idea in enumerate(value, 1):
                # Handle long text by breaking into multiple lines if needed
                idea_text = f"{i+1}. {idea}"
                
                # Simple text wrapping (break after ~60 characters)
                if len(idea_text) > 70:
                    # Split into multiple lines
                    words = idea_text.split()
                    lines = []
                    current_line = []
                    current_length = 0
                    
                    for word in words:
                        if current_length + len(word) + 1 <= 70:
                            current_line.append(word)
                            current_length += len(word) + 1
                        else:
                            lines.append(' '.join(current_line))
                            current_line = [word]
                            current_length = len(word)
                    
                    if current_line:
                        lines.append(' '.join(current_line))
                    
                    # Draw each line
                    for line in lines:
                        draw.text((50, y_pos), line, fill=(0, 0, 0))
                        y_pos += 30
                else:
                    draw.text((50, y_pos), idea_text, fill=(0, 0, 0))
                    y_pos += 30
                
                y_pos += 10  # Extra spacing between ideas
        
        return img
    
    except Exception as e:
        print(f"Error in image rendering: {str(e)}")
        return None

def main() -> None:
    try:
        print("\n" + "="*50)
        print("   MARKETING IDEA GENERATOR")
        print("="*50)
        print("\nExamples of valid inputs:")
        print("  • pickle|neighbours")
        print("  • I want to sell pickle to neighbours")
        print("  • sell shoes for marathon runners")
        print("  • I want to sell ice cream to kids")
        print("\n" + "-"*50)
        
        user_input = input("\nYour input: ").strip()
        
        # Extract product and audience information
        product_audience = stage_1_extraction(user_input)
        
        # Check if extraction was successful
        if product_audience:
            product = product_audience['product']
            audience = product_audience['audience']
            
            print(f"\n✅ Successfully extracted:")
            print(f"   Product: {product}")
            print(f"   Audience: {audience}")
            
            # Generate ideas
            print("\n💡 Generating marketing ideas...")
            ideas = stage_2_ideation(product, audience)
            
            # Display ideas in console
            print("\n📋 Generated Ideas:")
            for key, value in ideas.items():
                for i, idea in enumerate(value, 1):
                    print(f"   {i}. {idea}")
            
            # Render and display image
            print("\n🎨 Rendering image...")
            img = stage_3_rendering(ideas)
            
            if img:
                print("✅ Image generated successfully!")
                img.show()
                # Save the image
                filename = f"{product}_marketing_ideas.png"
                img.save(filename)
                print(f"💾 Image saved as: {filename}")
            else:
                print("❌ Failed to generate image")
        else:
            print("\n❌ Could not process your input. Please try again with a valid format.")
    
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")

# Call the main method
if __name__ == "__main__":
    main()