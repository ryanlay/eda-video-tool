# EDA Video Visualization Tool 🎥📊

A Flask web application for synchronizing and visualizing Electrodermal Activity (EDA) data with video recordings. Perfect for researchers studying stress, arousal, and emotional responses.

![Python](https://img.shields.io/badge/python-3.7+-brightgreen.svg)
![Flask](https://img.shields.io/badge/flask-2.2+-red.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🌟 Features

- 📈 **Interactive EDA Visualization** - Real-time plotting with Plotly
- 🎬 **Video Synchronization** - Sync EDA data with video recordings
- 📊 **Statistical Analysis** - Automatic calculation of mean, std, min, max
- ⏱️ **Timeline Scrubber** - Navigate through data and video simultaneously
- 📁 **Flexible Data Import** - Support for various CSV formats
- 🎨 **Modern UI** - Clean, responsive interface with Bootstrap 5

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ryanlay/eda-video-tool.git
   cd eda-video-tool
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment**
   - Windows:
     ```powershell
     .venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   cd webapp
   pip install -r requirements.txt
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open your browser**
   Navigate to `http://127.0.0.1:5000`

## 📁 Project Structure

```
eda-video-tool/
├── webapp/
│   ├── app.py                      # Main Flask application
│   ├── requirements.txt            # Python dependencies
│   ├── templates/                  # HTML templates
│   │   ├── index.html             # Main page
│   │   └── about.html             # About page
│   ├── static/                     # Static assets
│   │   ├── css/                   # Stylesheets
│   │   └── videos/                # Uploaded videos
│   └── uploads/                    # Uploaded CSV files
├── EDA.csv                         # Sample EDA data file
├── .gitignore                      # Git ignore rules
├── LICENSE                         # MIT License
└── README.md                       # This file
```

## 📊 Data Format

The application supports multiple CSV formats:

### Format 1: With Headers
```csv
timestamp_unix,eda_scl_usiemens,participant_full_id
1526304383000,0.840149,P001
1526304383250,1.131137,P001
```

### Format 2: Without Headers (Raw Data)
```csv
1526304383.000000
4.000000
0.000000
0.840149
1.131137
```

The first line is the UNIX timestamp, second line is the sampling rate (Hz), and subsequent lines are EDA values.

## 🎬 Video Support

Supported video formats:
- MP4 (recommended)
- WebM
- OGG
- MOV
- AVI (with conversion recommended)

See [VIDEO_COMPRESSION_GUIDE.md](webapp/VIDEO_COMPRESSION_GUIDE.md) for optimization tips.

## 📖 Documentation

- [Video Synchronization Guide](webapp/VIDEO_SYNC_GUIDE.md)
- [Timeline Scrubber Guide](webapp/TIMELINE_SCRUBBER_GUIDE.md)
- [Video Compression Guide](webapp/VIDEO_COMPRESSION_GUIDE.md)
- [AVI Playback Guide](webapp/AVI_PLAYBACK_GUIDE.md)

## 🛠️ Technology Stack

- **Backend**: Flask 2.2+
- **Data Processing**: pandas 1.3+
- **Visualization**: Plotly 5.18+
- **Frontend**: Bootstrap 5, vanilla JavaScript
- **Timezone Handling**: pytz

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

Ryan Lay - [@ryanlay](https://github.com/ryanlay)

## 🙏 Acknowledgments

- Built with Flask and Plotly
- Designed for EDA research applications
- Inspired by the need for better psychophysiological data visualization

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

Made with ❤️ for researchers studying human psychophysiology
