# Video Compression Guide for EDA Platform

## Why Compress Videos?

Large video files (>500MB) can take a long time to upload and process. Compressing your videos before upload provides:

- ⚡ **Faster uploads** - Reduced file size means quicker transfer
- 💾 **Less storage** - Saves disk space on server
- 🚀 **Better performance** - Faster loading and playback
- ✅ **Same quality** - Minimal visual difference with proper settings

## Recommended Settings

For best results, use these settings when compressing:

- **Codec**: H.264 (most compatible)
- **Resolution**: 720p (1280x720) or 480p (854x480)
- **Frame Rate**: 30 fps
- **Bitrate**: 1-2 Mbps for 720p, 0.5-1 Mbps for 480p
- **Target Size**: Under 200MB ideal, 500MB maximum

## Tools & Methods

### Option 1: HandBrake (Free, Easy)

**Best for:** Beginners, one-time compression

1. Download HandBrake: https://handbrake.fr/
2. Open your video file
3. Select "Fast 720p30" or "Fast 480p30" preset
4. Click "Start Encode"

**Settings:**
- Format: MP4
- Video Codec: H.264
- Quality: RF 22-24 (lower = better quality but larger file)
- Frame Rate: 30 fps

### Option 2: FFmpeg (Command Line)

**Best for:** Batch processing, automation

Download: https://ffmpeg.org/

**Command to compress to 720p:**
```bash
ffmpeg -i input.mp4 -vf scale=1280:720 -c:v libx264 -crf 23 -preset medium -c:a aac -b:a 128k output.mp4
```

**Command to compress to 480p (smaller):**
```bash
ffmpeg -i input.mp4 -vf scale=854:480 -c:v libx264 -crf 23 -preset medium -c:a aac -b:a 96k output.mp4
```

**Parameters explained:**
- `-vf scale=1280:720` - Resize to 720p
- `-c:v libx264` - Use H.264 video codec
- `-crf 23` - Quality (18-28, lower = better quality)
- `-preset medium` - Encoding speed (fast/medium/slow)
- `-c:a aac` - Use AAC audio codec
- `-b:a 128k` - Audio bitrate

### Option 3: VLC Media Player (Free, Simple)

**Best for:** Quick compression without installing new software

1. Open VLC
2. Media → Convert/Save
3. Add your video file
4. Click Convert/Save
5. Profile: "Video - H.264 + MP3 (MP4)"
6. Settings → Edit → Video codec:
   - Resolution: Scale to 1280x720 or 854x480
   - Bitrate: 1000-2000 kb/s
   - Frame rate: 30
7. Start conversion

### Option 4: Online Converters

**Best for:** Small files, no installation needed

- **CloudConvert**: https://cloudconvert.com/
- **FreeConvert**: https://www.freeconvert.com/
- **Online-Convert**: https://www.online-convert.com/

⚠️ **Note:** Be cautious with sensitive research data on online services.

## Compression Comparison

| Original | Compressed 720p | Compressed 480p |
|----------|----------------|-----------------|
| 2GB      | ~300-400MB     | ~150-200MB      |
| 1GB      | ~150-200MB     | ~75-100MB       |
| 500MB    | ~75-100MB      | ~40-50MB        |

*Actual sizes vary based on video content and settings*

## Step-by-Step: HandBrake Example

### For Research Videos (Recommended)

1. **Install HandBrake**
   - Download from https://handbrake.fr/
   - Install and open

2. **Load Your Video**
   - Click "Open Source"
   - Select your video file

3. **Choose Preset**
   - In the right sidebar, select "Fast 720p30"
   - Or use "Fast 480p30" for smaller files

4. **Adjust Settings (Optional)**
   - Dimensions tab: Confirm resolution
   - Video tab: Adjust quality slider (20-24 recommended)
   - Audio tab: Select AAC codec, 128 kbps

5. **Set Destination**
   - Click "Browse" to choose output location
   - Name your file (e.g., "session_compressed.mp4")

6. **Start Encoding**
   - Click "Start Encode"
   - Wait for completion (usually 2-10 minutes)

7. **Verify Quality**
   - Play the compressed video
   - Ensure it's still clear enough for your needs

8. **Upload to Platform**
   - Use the compressed video in the EDA platform

## Quality vs Size Guidelines

**For general sessions:**
- 720p @ 1.5 Mbps = Good quality, ~300MB/hour
- 480p @ 1 Mbps = Acceptable quality, ~150MB/hour

**For detailed analysis (facial expressions, fine movements):**
- 1080p @ 2.5 Mbps = High quality, ~500MB/hour
- 720p @ 2 Mbps = Good quality, ~400MB/hour

**For overview/context only:**
- 480p @ 0.5 Mbps = Low quality, ~75MB/hour
- 360p @ 0.3 Mbps = Very low quality, ~50MB/hour

## Batch Processing

If you have multiple videos to compress:

### Windows Batch Script (FFmpeg)
```batch
@echo off
for %%i in (*.mp4) do (
    ffmpeg -i "%%i" -vf scale=1280:720 -c:v libx264 -crf 23 -preset medium -c:a aac -b:a 128k "compressed_%%i"
)
```

### Mac/Linux Bash Script (FFmpeg)
```bash
#!/bin/bash
for file in *.mp4; do
    ffmpeg -i "$file" -vf scale=1280:720 -c:v libx264 -crf 23 -preset medium -c:a aac -b:a 128k "compressed_$file"
done
```

## Troubleshooting

**Video quality is too poor after compression:**
- Decrease CRF value (try 20 instead of 23)
- Increase bitrate (try 2000 kbps instead of 1000)
- Use a higher resolution

**File size is still too large:**
- Increase CRF value (try 26 instead of 23)
- Reduce resolution (720p → 480p)
- Lower frame rate (30fps → 24fps)
- Reduce audio bitrate (128k → 96k)

**Upload still taking too long:**
- Try 480p instead of 720p
- Use "Fast" preset in FFmpeg
- Consider uploading overnight for very large files
- Check your internet upload speed

## Best Practices

1. **Always keep the original** - Save uncompressed videos as backup
2. **Test first** - Compress a short sample to verify settings
3. **Name clearly** - Use descriptive filenames (e.g., "P001_session1_compressed.mp4")
4. **Verify sync** - Check that compressed video still syncs with EDA data
5. **Document settings** - Keep note of compression settings for consistency

## Platform Upload Limits

- **Maximum file size**: 2GB
- **Recommended size**: Under 200MB
- **Upload timeout**: 10 minutes
- **Supported formats**: MP4, WebM, OGG, MOV, AVI

## Need Help?

If videos still won't upload after compression:
1. Check file format (MP4 H.264 most compatible)
2. Verify file size is under 2GB
3. Check internet connection speed
4. Try a different browser
5. Contact support with video details

---

**Quick Tip:** For a 1-hour video, aim for under 300MB. This usually takes 2-5 minutes to upload depending on your connection speed.
