# EDA Visualization Web Platform

A Flask web application for uploading and visualizing Electrodermal Activity (EDA) data from CSV files.

## 🎯 Purpose

This platform allows researchers and clinicians to:
- Upload CSV files containing EDA data
- Visualize EDA levels over time with interactive charts
- View statistical summaries (mean, min, max, standard deviation)
- Analyze stress and arousal patterns

## 🏗️ Architecture (ASP.NET Ready)

This application is structured to mirror ASP.NET MVC patterns:

```
Flask Component          →  ASP.NET Equivalent
────────────────────────────────────────────────
@app.route()            →  [HttpGet]/[HttpPost] Actions
render_template()       →  return View()
Templates (Jinja2)      →  Razor Views (.cshtml)
process_eda_file()      →  Service Layer
uploads/                →  wwwroot/uploads/
static/                 →  wwwroot/static/
```

## 📁 Project Structure

```
webapp/
├── app.py                  # Main application (like Program.cs + Controllers)
├── templates/              # HTML templates (like Views/)
│   ├── index.html         # Home page
│   └── about.html         # About page
├── static/                 # Static assets (like wwwroot/)
│   └── css/
├── uploads/                # Uploaded files storage
└── requirements.txt        # Python dependencies
```

## 🚀 Installation & Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open browser to: http://127.0.0.1:5000

## 📊 CSV File Requirements

Your CSV file should contain:
- **Timestamp column**: `timestamp_iso`, `timestamp`, `time`, or `datetime`
- **EDA column**: `eda_scl_usiemens`, `eda`, `skin_conductance`, or `scl`

Example CSV format:
```csv
timestamp_iso,participant_full_id,eda_scl_usiemens,missing_value_reason
2025-11-19T13:06:00Z,2414-1-1-TESTSUBJECT,0.06,
2025-11-19T13:07:00Z,2414-1-1-TESTSUBJECT,0.07,
```

## ✨ Features

- **Drag & Drop Upload** - Easy file upload interface
- **Interactive Charts** - Zoom, pan, and explore with Plotly
- **Real-time Statistics** - Automatic calculation of key metrics
- **Responsive Design** - Works on desktop and mobile
- **Error Handling** - Clear error messages for invalid files

## 🔄 Migration to ASP.NET Core

When ready to migrate to ASP.NET:

1. **Controllers**: Convert routes to Controller actions
   ```csharp
   [HttpGet]
   public IActionResult Index() => View();
   
   [HttpPost]
   public async Task<IActionResult> Upload(IFormFile file) { ... }
   ```

2. **Views**: Convert Jinja2 templates to Razor
   ```html
   @model EdaViewModel
   <h1>@Model.ParticipantId</h1>
   ```

3. **Services**: Create EDA processing service
   ```csharp
   public class EdaService : IEdaService {
       public EdaResult ProcessFile(string filepath) { ... }
   }
   ```

4. **Database**: Add Entity Framework for data persistence
   ```csharp
   public class EdaData {
       public int Id { get; set; }
       public DateTime Timestamp { get; set; }
       public double EdaValue { get; set; }
   }
   ```

## 📝 License

This is a prototype application for educational and research purposes.
