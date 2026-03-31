import easyocr
import cv2
import numpy as np
import gc

class OCRPipeline:
    def __init__(self, languages=['en', 'fr', 'sw'], gpu=False):
        """Initializes the EasyOCR reader once to save memory/time."""
        self.reader = easyocr.Reader(languages, gpu=gpu)

    def preprocess(self, image_path):
        """Prepares the image for better OCR accuracy."""
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not open or find the image: {image_path}")

        # 1. Standardize Resolution
        max_dim = 1500  # Increased slightly for better detail
        h, w = image.shape[:2]
        if max(h, w) > max_dim:
            scale = max_dim / max(h, w)
            image = cv2.resize(image, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA)

        # 2. Grayscale & Denoising
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Note: We skip heavy Thresholding here because EasyOCR 
        # often performs better on grayscale than on binary black/white.
        processed = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
        
        return processed

    def extract_text(self, image):
        """Runs the actual OCR engine."""
        # Using paragraph=True groups lines together, making 'clean' easier
        return self.reader.readtext(
            image,
            detail=1,
            paragraph=True, 
            contrast_ths=0.1,
            adjust_contrast=0.5
        )

    def clean_results(self, text_blocks):
        """
        Filters and formats the raw OCR output.
        Handles both Paragraph mode (2 values) and Standard mode (3 values).
        """
        if not text_blocks:
            return ""

        # Sort blocks by their Y-coordinate (top to bottom)
        text_blocks = sorted(text_blocks, key=lambda x: x[0][0][1])

        cleaned_lines = []

        for block in text_blocks:
            # FLEXIBLE UNPACKING: Handles (bbox, text, conf) OR (bbox, text)
            if len(block) == 3:
                bbox, text, conf = block
                if conf < 0.4: continue # Filter low confidence if available
            else:
                bbox, text = block

            text = text.strip()

            # Filter out noise (single characters or purely symbols)
            if len(text) > 1 and not text.isspace():
                cleaned_lines.append(text)

        return "\n\n".join(cleaned_lines)

    def generate_ai_prompt(self, text):
        """Wraps the cleaned text in an instruction prompt for an LLM."""
        if not text:
            return "No text was extracted from the image."

        return f"""
        --- OCR CORRECTION TASK ---
        The following text was extracted from a document image. 
        Please fix any typos, restore broken words, and ensure the 
        formatting makes sense (legal/academic style).
        
        EXTRACTED TEXT:
        {text}
        
        RETURN ONLY THE CORRECTED TEXT.
        """

    def process(self, image_path):
        """Main execution flow."""
        try:
            # Step 1: Image Prep
            processed_img = self.preprocess(image_path)
            
            # Step 2: Extraction
            raw_results = self.extract_text(processed_img)
            
            # Step 3: Cleaning & Formatting
            final_text = self.clean_results(raw_results)
            ai_prompt = self.generate_ai_prompt(final_text)

            return {
                "success": True,
                "raw_text": final_text,
                "ai_prompt": ai_prompt,
                "metadata": {"blocks_found": len(raw_results)}
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
        finally:
            # Memory Management
            gc.collect()

# --- EXECUTION ---
if __name__ == "__main__":
    pipeline = OCRPipeline(gpu=False) # Set to True if you have NVIDIA/CUDA
    
    result = pipeline.process("image4.jpeg")

    if result["success"]:
        print("--- EXTRACTED CONTENT ---")
        print(result["raw_text"])
        print("\n--- AI READY PROMPT ---")
        print(result["ai_prompt"])
    else:
        print(f"Error occurred: {result['error']}")




    # 1. Initialize the pipeline (do this once)
#pipeline = OCRPipeline(languages=['en'], gpu=False)

    # 2. Process an image
#result = pipeline.process("image4.jpeg")

    # 3. Handle the output
#if result["success"]:
#    raw_text = result["raw_text"]
#    ai_prompt = result["ai_prompt"]
    
#    print(f"Extracted Text: {raw_text}")
    # You can now send 'ai_prompt' to an LLM API
#else:
#    print(f"Error: {result['error']}")