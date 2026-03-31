import pymupdf
from ocr import OCRPipeline

def read_pdf(pdf_path):
    doc = pymupdf.open(pdf_path)
    ocr = OCRPipeline(languages=['en'], gpu=False)
    full_content = []

    for page_index, page in enumerate(doc):
        # 1. Try direct extraction first
        text = page.get_text().strip()
        
        if text:
            print(f"Page {page_index}: Digital text found.")
            full_content.append(text)
        else:
            print(f"Page {page_index}: No text found. Running OCR...")
            # 2. Convert page to an image (pixmap)
            pix = page.get_pixmap(dpi=300) 
            img_path = f"temp_page_{page_index}.png"
            pix.save(img_path)
            
            # 3. Use your OCRPipeline
            ocr_result = ocr.process(img_path)
            if ocr_result["success"]:
                full_content.append(ocr_result["raw_text"])
            
            # Optional: delete temp image after use
            # os.remove(img_path)

    return "\n\n--- Page Break ---\n\n".join(full_content)

    # Usage
#final_document = read_pdf("document name")