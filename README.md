# AI Lead Scoring API

This project provides a Flask API for scoring sales leads using both rule-based logic and Gemini AI. Results are stored and can be exported as CSV.

## Setup

1. **Clone the repository**  
   `git clone <repo-url>`

2. **Install dependencies**  
   ```
   pip install -r requirements.txt
   ```

3. **Set up environment variables**  
   - Add your Gemini API key and MongoDB URI to `.env`:
     ```
     GEMINI_API_KEY="your-gemini-api-key"
     MONGO_URI="your-mongodb-uri"
     ```

4. **Run the server**  
   ```
   python app.py
   ```

## API Usage Examples

### 1. Set Offer

**cURL**
```sh
curl -X POST http://localhost:5000/offer \
  -H "Content-Type: application/json" \
  -d '{"name": "AI Outreach Automation", "value_props": ["24/7 outreach", "6x more meetings"], "ideal_use_cases": ["B2B SaaS mid-market", "Tech companies", "Software services"]}'
```

### 2. Upload Leads

**cURL**
```sh
curl -X POST http://localhost:5000/leads/upload \
  -F "file=@storage/leads.csv"
```

### 3. Score Leads

**cURL**
```sh
curl -X POST http://localhost:5000/score
```

### 4. Get Results

**cURL**
```sh
curl http://localhost:5000/results
```

### 5. Export Results as CSV

**cURL**
```sh
curl -O http://localhost:5000/results/export
```

## Rule Logic Explanation

- **Role relevance:**  
  - "Head", "Chief", "VP", "Director" → +20 points  
  - "Manager", "Lead" → +10 points

- **Industry match:**  
  - Exact match with offer's `ideal_use_cases` → +20 points  
  - Partial/adjacent match → +10 points

- **Data completeness:**  
  - All fields present → +10 points

## AI Prompt Explanation

The AI prompt (see [`services/prompt.txt`](services/prompt.txt)) asks Gemini to classify each lead's intent (`High`, `Medium`, `Low`) and provide a short reasoning.  
The AI's intent is mapped to a score:
- High → 50 points
- Medium → 30 points
- Low → 10 points

Final score = rule-based score + AI score.

## File Structure

- `app.py` — Flask API endpoints
- `services/service.py` — Scoring logic
- `services/gemini_helper.py` — Gemini API integration
- `services/storage_handler.py` — File storage utilities
- `storage/` — Data files (leads, offer, results)