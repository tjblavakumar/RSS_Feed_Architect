# RSS Architect 📡

A Python web application that discovers or synthesizes RSS feeds from any website.

## Features

- **RSS Discovery**: Automatically finds existing RSS/Atom feeds on websites using multiple methods
- **Enhanced Pattern Discovery**: Tests 23+ common RSS URL patterns (like `/feed/`, `/rss/`, `/blog/feed/`)
- **Synthetic RSS Generation**: Creates RSS feeds from article links when no feeds exist
- **Paywall Detection**: Identifies paywalled content and stops processing
- **Feed Management**: Save, organize, and manage discovered feeds with custom nicknames
- **Website Nicknames**: Group feeds under memorable website names with auto-population
- **Duplicate Prevention**: Checks for existing feeds before saving with user-friendly warnings
- **SQLite Storage**: Local database for persistent feed storage
- **Two-Page Navigation**: Simple interface with "Scan Feed" and "View Feeds" pages
- **Grouped Display**: Feeds organized by website nickname in expandable sections
- **Individual Deletion**: Delete feeds one by one with confirmation
- **3D Blue Navigation**: Stylish navigation buttons with hover effects
- **Docker Support**: Complete containerized deployment

## Quick Start with Docker (Recommended)

### Prerequisites
- Docker and Docker Compose installed on your system

### 1. Clone or Download
Download all the application files to a directory.

### 2. Start with Docker
```bash
# Make the script executable (Linux/Mac)
chmod +x start.sh

# Start the application
./start.sh
```

The application will be available at `http://localhost:8501`

### 3. Stop the Application
```bash
./stop.sh
```

## Manual Installation

### Prerequisites
- Python 3.11 or higher
- pip package manager

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application

#### Option 1: Direct Streamlit (Recommended)
```bash
streamlit run app.py --server.headless true
```

#### Option 2: Using the launcher script
```bash
python run.py
```

#### Option 3: Using the shell script (Linux/Mac)
```bash
./start.sh
```

### 3. Access the Application
Open your browser to `http://localhost:8501`

## Docker Commands

### Basic Commands
```bash
# Start the application
./start.sh

# Stop the application  
./stop.sh

# View logs
docker-compose logs -f

# Restart the application
docker-compose restart

# Rebuild the container (after code changes)
docker-compose build --no-cache
docker-compose up -d
```

### Manual Docker Commands
```bash
# Build the image
docker build -t rss-architect .

# Run the container
docker run -d -p 8501:8501 -v $(pwd)/data:/app/data --name rss-architect rss-architect

# Stop and remove container
docker stop rss-architect
docker rm rss-architect
```

## Usage Guide

### Getting Started
1. Enter any website URL in the "Website URL" field
2. The "Website Nickname" will auto-populate but can be edited
3. Click "🔍 Scan for Feeds" to discover RSS feeds
4. Save individual feeds with custom nicknames
5. View and manage saved feeds in the "📚 View Feeds" section

### RSS Discovery Methods
The application uses multiple discovery methods:

1. **Traditional Method**: Searches for `<link rel="alternate">` tags in HTML
2. **Content Discovery**: Finds RSS URLs mentioned in page content  
3. **Pattern Discovery**: Tests 23+ common RSS URL patterns:
   - `/feed/`, `/rss/`, `/blog/feed/`
   - `/rss.xml`, `/feed.xml`, `/atom.xml`
   - `/feeds/`, `/news/rss/`, `/?feed=rss2`
   - And many more...

### Handling Blocked Websites
Some websites block automated requests. The application:
- Uses multiple User-Agent headers and retry strategies
- Provides helpful guidance when websites are blocked
- Suggests manual methods to find RSS feeds

## Troubleshooting

### Common Issues

**ModuleNotFoundError: No module named 'distutils'**
- Use headless mode: `streamlit run app.py --server.headless true`

**403 Forbidden Errors**
- Some websites block automated requests
- Try the suggested manual methods in the error message

**Docker Issues**
- Ensure Docker and Docker Compose are installed
- Check if port 8501 is already in use
- View logs with `docker-compose logs`

**Database Issues**
- The SQLite database is created automatically
- Database file: `feed_storage.db`
- Docker volume ensures data persistence

## User Interface

### Top Navigation
- **Scan Feed**: Main page for discovering and saving RSS feeds
- **View Feeds**: Page for viewing and managing saved feeds

### Scan Feed Page
- **Website URL**: Enter any website URL to scan
- **Website Nickname**: Auto-populated from URL, editable for custom grouping
- **Simple Table**: Clean display of discovered feeds with serial numbers
- **Save Functionality**: Individual save buttons for each discovered feed

### View Feeds Page
- **Grouped Display**: Feeds organized by website nickname in expandable sections
- **Feed Details**: Shows feed name, URL, type (Discovered/Synthetic), and save date
- **Individual Delete**: Delete specific feeds with confirmation
- **Feed Count**: Shows number of feeds per website group

## Simplified Workflow

### Scan Feed Process
1. Enter Website URL and Website Nickname
2. Click "Scan for Feeds" 
3. View existing feeds (if any) from database
4. See newly discovered feeds in simple table format
5. Save individual feeds with custom nicknames

### View Feeds Process
1. Click "View Feeds" in top navigation
2. Browse feeds grouped by website nickname
3. Expand/collapse website groups
4. Delete individual feeds as needed

## Technical Stack

- **Streamlit**: Web interface
- **SQLite**: Local database
- **BeautifulSoup4**: HTML parsing
- **Requests**: HTTP requests
- **feedgenerator**: RSS XML generation
- **validators**: URL validation