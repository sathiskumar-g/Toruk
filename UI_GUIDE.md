# TORUKMACTO Web UI Guide

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install flask flask-cors
```

### 2. Start the Server
```bash
python api.py
```

### 3. Open Browser
Navigate to: **http://localhost:5000**

---

## 📖 How to Use

### Adding Keywords
1. Type a problem keyword in the input field (e.g., "n8n debugging is hard")
2. Click "Add Keyword" or press Enter
3. Keywords appear as tags below
4. Remove keywords by clicking the × on each tag

### Running Research
1. Set the number of posts per keyword (default: 5)
2. Click "🚀 Run Research"
3. Wait for the loading screen (searches Reddit in real-time)
4. View results once complete

### Understanding Results

#### Summary Cards
- **Keywords Searched**: Total keywords processed
- **Opportunities Found**: Total validated problems found
- **Top Score**: Highest opportunity score (max 50)

#### Keyword Summary Table
Shows results per keyword:
- Posts found
- Problems extracted
- Opportunities identified
- Top opportunity score

#### Opportunities List
Each opportunity shows:
- **Title**: Reddit post title (clickable link)
- **Score**: 5-Factor opportunity score (0-50)
- **Keyword**: Which search term found this
- **Problem Statement**: Extracted pain point
- **Engagement**: Upvotes and comments
- **Category**: Problem type
- **Detailed Scores**: Pain, Pervasiveness, Proximity, Payment, Plausibility
- **Recommendation**: Whether to pursue

### Exporting Results
Click "Export JSON" to download the full research data as a JSON file.

---

## 🎨 Features

- **Real-time Search**: Searches Reddit directly when you submit
- **Keyword Management**: Add/remove keywords easily
- **Visual Results**: Clean, card-based interface
- **Score Breakdown**: See all 5 factors for each opportunity
- **Responsive Design**: Works on desktop and mobile
- **Export Data**: Download results as JSON

---

## 🛠 Technical Details

### API Endpoints

- `GET /` - Serve web UI
- `GET /api/keywords` - Get saved keywords
- `POST /api/keywords` - Save keywords
- `POST /api/research` - Run batch research
- `GET /api/results` - Get latest results

### Files Structure

```
torukmacto/
├── api.py                 # Flask backend server
├── static/
│   ├── index.html        # Main UI page
│   ├── styles.css        # Styling
│   └── app.js            # JavaScript logic
└── data/                 # Research results saved here
```

### How It Works

1. **Frontend** (HTML/CSS/JS):
   - User interface for keyword management
   - Calls Flask API endpoints
   - Displays results visually

2. **Backend** (Flask):
   - Wraps the existing Reddit scraper
   - Runs batch research
   - Returns JSON results

3. **Data Flow**:
   ```
   User → Add Keywords → Submit → API → Reddit Scraper → Extract Problems → 
   Score Opportunities → Return JSON → Display in UI
   ```

---

## 💡 Tips

1. **Start Small**: Test with 2-3 keywords and limit=5 first
2. **Be Specific**: Better keywords = better results (e.g., "n8n debugging" vs "automation")
3. **Check Scores**: Focus on opportunities with scores > 25
4. **Read Comments**: High engagement = validated pain points
5. **Export Often**: Save your research results for later analysis

---

## 🔧 Troubleshooting

### Server won't start
- Make sure Flask is installed: `pip install flask flask-cors`
- Check if port 5000 is available
- Try a different port: Change `port=5000` in api.py

### No results showing
- Check browser console for errors (F12)
- Verify keywords are added
- Ensure Reddit is not blocking requests (add delay in scraper)

### Research takes too long
- Reduce the number of keywords
- Reduce posts per keyword limit
- Reddit rate limiting may be active

---

## 🎯 Next Steps

Once you've found good opportunities:
1. **Validate**: Read the actual Reddit threads
2. **Research More**: Use related keywords
3. **Check Competition**: Search for existing solutions
4. **Build MVP**: Start with the highest-scoring problems
5. **Test**: Validate with potential users from those threads

---

## 📝 Example Workflow

1. Add keywords related to your niche:
   - "n8n debugging is hard"
   - "Make.com automation fails"
   - "Zapier rate limit problem"

2. Set limit to 5 posts per keyword

3. Click "Run Research"

4. Review opportunities with scores > 25

5. Open Reddit links for top opportunities

6. Validate the pain points

7. Build a Micro SaaS solution!

---

**Happy Problem Hunting! 🎯**
