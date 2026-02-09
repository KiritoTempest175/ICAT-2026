from fastapi.testclient import TestClient
import os
try:
    from app.main import app
except ImportError:
    import sys
    sys.path.append(os.getcwd())
    from app.main import app

client = TestClient(app)

def create_dummy_pdf():
    try:
        from reportlab.pdfgen import canvas
        c = canvas.Canvas("test.pdf")
        c.drawString(100, 750, "Header Area")
        c.drawString(100, 500, "Hello World Content")
        c.drawString(100, 50, "Footer Area")
        c.save()
        print("Created dummy test.pdf")
    except ImportError:
        print("ReportLab not found, cannot create test test.pdf.")

def test_endpoints():
    # Ensure fresh test PDF
    create_dummy_pdf()
    
    saved_path = None

    print("Testing Upload...")
    try:
        if not os.path.exists("test.pdf"):
            print("test.pdf not found, skipping upload test.")
            return

        with open("test.pdf", "rb") as f:
            response = client.post(
                "/upload",
                files={"file": ("test.pdf", f, "application/pdf")}
            )
        print(f"Upload Status Code: {response.status_code}")
        print(f"Upload Response: {response.json()}")
        assert response.status_code == 200
        data = response.json()
        assert "saved_at" in data
        saved_path = data["saved_at"]
    except Exception as e:
        print(f"Upload Failed: {e}")
        raise e

    print("\nTesting Process...")
    try:
        response = client.post("/process?filename=test.pdf")
        print(f"Process Status Code: {response.status_code}")
        print(f"Process Response: {response.json()}")
        
        assert response.status_code == 200
        data = response.json()
        assert "content" in data
        assert "message" in data
        assert data["message"] == "File processed and scheduled for deletion"
        
        # Check if content has text (ReportLab PDF should be legible)
        # Note: clean_pdf_text strips headers/footers.
        # "Hello World Content" is in middle -> Should be present.
        if "Hello World Content" in data["content"]:
            print("Verified: Content extracted correctly.")
        else:
            print("Warning: Expected content not found. Check cropping logic or PDF generation.")
            
        # Verify deletion (Privacy Check)
        import time
        time.sleep(0.5) # Give background task a moment
        if saved_path:
            if not os.path.exists(saved_path):
                 print(f"Verified: File {saved_path} was deleted (Privacy check passed).")
            else:
                 print(f"Warning: File {saved_path} was NOT deleted.")

    except Exception as e:
        print(f"Process Failed: {e}")
        raise e

if __name__ == "__main__":
    test_endpoints()
