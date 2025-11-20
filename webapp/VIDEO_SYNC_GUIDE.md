# Video Synchronization Guide

## 🎥 How to Use Video Sync with EDA Data

### Overview
The platform now supports uploading video files alongside your EDA CSV data. The video timeline is automatically synchronized with the EDA measurements, allowing you to see exactly what was happening when physiological changes occurred.

### Supported Video Formats
- **MP4** (recommended)
- WebM
- OGG
- MOV
- AVI

### Upload Process

1. **Select CSV File** (required)
   - Click "Choose CSV File" or drag & drop
   - File name will appear with a green checkmark

2. **Select Video File** (optional)
   - Click "Choose Video (Optional)" or drag & drop
   - Supported formats: mp4, webm, ogg, mov, avi
   - Maximum size: 500MB

3. **Upload & Visualize**
   - Click the "Upload & Visualize" button
   - Both files will be uploaded together

### Video-EDA Synchronization

#### How it Works:
- The video timeline is mapped to your EDA data points
- **Click any point on the EDA chart** to jump to that moment in the video
- The video will automatically seek to the corresponding timestamp

#### Example Use Cases:
1. **Stress Response Analysis**
   - See EDA spikes correlate with specific events in the video
   - Identify stress triggers during tasks or interviews

2. **Therapy Sessions**
   - Track emotional arousal during patient discussions
   - Review specific moments that caused physiological responses

3. **User Experience Research**
   - Observe user reactions during product testing
   - Correlate confusion or frustration with EDA changes

4. **Sports Performance**
   - Analyze athlete stress during competition
   - Identify peak arousal moments

### Technical Details

**Time Mapping:**
- Video duration is linearly mapped to data point indices
- Point index / Total points = Video position ratio
- Example: Clicking point 150 of 300 jumps to 50% of video duration

**File Storage:**
- Videos are stored in `static/videos/` directory
- Files are timestamped to avoid naming conflicts
- Format: `YYYYMMDD_HHMMSS_originalname.mp4`

### Tips for Best Results

1. **Video Recording**
   - Start recording video at the same time as EDA data collection
   - Use a consistent frame rate (30fps recommended)
   - Ensure good lighting and clear view of subject

2. **File Size**
   - Compress videos before upload if needed
   - H.264 codec recommended for MP4 files
   - Consider lowering resolution for faster uploads

3. **Synchronization Accuracy**
   - For best sync, ensure EDA data collection and video start simultaneously
   - If there's an offset, note the time difference for analysis

### Browser Compatibility

**Fully Supported:**
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)

**Video Format Support:**
- All browsers: MP4 with H.264 codec
- Chrome/Edge: WebM
- Check browser-specific codec support for other formats

### ASP.NET Migration Notes

When migrating to ASP.NET Core, video handling translates to:

```csharp
[HttpPost]
public async Task<IActionResult> Upload(IFormFile file, IFormFile video)
{
    // Save CSV
    var csvPath = await SaveFileAsync(file, "uploads");
    
    // Save video if provided
    string videoUrl = null;
    if (video != null)
    {
        var videoPath = await SaveFileAsync(video, "wwwroot/videos");
        videoUrl = $"/videos/{Path.GetFileName(videoPath)}";
    }
    
    // Process and return
    var result = ProcessEdaFile(csvPath);
    return Json(new { 
        success = true, 
        videoUrl = videoUrl,
        // ... other data
    });
}
```

### Troubleshooting

**Video won't play:**
- Check file format compatibility with your browser
- Try converting to MP4 with H.264 codec
- Check browser console for errors

**Sync is off:**
- Verify video and EDA recording started at same time
- Check that video duration roughly matches data collection period
- Consider manual offset adjustment if needed

**Upload fails:**
- Check file size (max 500MB)
- Ensure stable internet connection
- Check available disk space

### Future Enhancements

Potential additions:
- Manual time offset adjustment
- Automatic peak detection with video bookmarks
- Multiple camera angles
- Annotation tools for marking events
- Export annotated timeline
