# AVI Video Playback Guide

## Understanding AVI Limitations

AVI (Audio Video Interleave) is an older video container format that **has limited support in modern web browsers**. The HTML5 `<video>` tag used in web applications primarily supports:

✅ **MP4** (H.264/H.265) - Best support  
✅ **WebM** (VP8/VP9) - Good support  
✅ **OGG** (Theora) - Limited support  
⚠️ **AVI** - Very limited/no support in most browsers

---

## Why AVI Doesn't Play in Browsers

1. **No Native Codec Support**: Most browsers don't include the codecs needed to decode AVI files
2. **Security Restrictions**: Browsers limit which codecs they support for security reasons
3. **Container Format Issues**: AVI can contain many different codecs, and browsers can't handle them all
4. **HTML5 Video Spec**: The HTML5 video specification doesn't require AVI support

---

## Solutions for Using AVI Files

### Option 1: Try Different Browsers (May Work)

Some browsers have better codec support than others:

1. **Firefox** - Sometimes has better AVI support through system codecs
2. **Microsoft Edge** - May use Windows Media codecs
3. **Chrome/Chromium** - Usually poorest AVI support

**Try this first**: Open the application in Firefox or Edge instead of Chrome.

---

### Option 2: Use VLC Web Plugin (Advanced)

Install VLC media player and the VLC web plugin (deprecated but may work on some systems).

⚠️ **Not recommended**: Most browsers have removed plugin support for security reasons.

---

### Option 3: Download and Play Locally

If the web player doesn't work:

1. Right-click on the black video box
2. Select "Save video as..." or "Download"
3. Open the downloaded AVI file in VLC Media Player or Windows Media Player
4. Use the timestamps from the EDA chart to manually sync

**Manual Sync Steps:**
- Note the timestamp you want to view (e.g., "02:30:15 PM EST")
- Calculate the time from video start (use the offset shown in the app)
- Seek to that time in VLC/Media Player

---

### Option 4: Server-Side Conversion (Automated)

We can add a server-side video conversion feature using FFmpeg:

**Requirements:**
- Install FFmpeg on the server
- Add automatic conversion when AVI is uploaded
- This will take time (2-5 minutes for large files)

**Pros:**
- Fully automatic
- Works for all users
- No client-side software needed

**Cons:**
- Requires FFmpeg installation
- Increases server load
- Slower upload processing

Would you like me to implement this feature?

---

### Option 5: Streaming Server (Best for Large Files)

Use a dedicated media server that can transcode on-the-fly:

**Solutions:**
- **Jellyfin** (Free, open-source)
- **Plex** (Free tier available)
- **Emby** (Paid)

These can:
- Stream AVI files by converting them in real-time
- Handle large video files efficiently
- Work with the web app via embedding

---

## Quick Test: Can Your Browser Play AVI?

Open your browser's developer console (F12) and run:

```javascript
var video = document.createElement('video');
var canPlayAVI = video.canPlayType('video/x-msvideo');
console.log('AVI support:', canPlayAVI);
// Returns: "" (no support), "maybe", or "probably"
```

If it returns `""` (empty string), your browser **cannot** play AVI files.

---

## Recommended Solution

**For best results**, I recommend one of these approaches:

### For Immediate Use:
1. Try opening the app in **Firefox** - it has the best chance of playing AVI
2. If that doesn't work, download and play locally in VLC

### For Long-term Use:
1. Convert future videos to MP4 before uploading (see `CONVERT_VIDEO.md`)
2. OR let me implement server-side auto-conversion with FFmpeg

---

## Checking Your Current Setup

**What browser are you using?**
- Chrome/Edge (Chromium): AVI very unlikely to work
- Firefox: Best chance for AVI playback
- Safari: No AVI support

**Do you have VLC installed?**
- Yes → You can play downloaded AVI files locally
- No → Download VLC (free): https://www.videolan.org/

**Can you install FFmpeg?**
- Yes → I can implement auto-conversion
- No → Use online converters or Firefox

---

## Video File Information

The uploaded AVI file:
- **Filename**: `SYS1Cam3--2018-05-14_10_22_27_frames_1-9470.avi`
- **Status**: Uploaded successfully to server
- **Location**: `webapp/static/videos/`
- **Accessible**: Yes, file is being served correctly
- **Playable in browser**: Depends on browser codec support

---

## Need Help?

If none of these solutions work, let me know:
1. What browser you're using
2. Whether you can install FFmpeg
3. If you prefer automatic server-side conversion

I can implement an auto-conversion feature if needed!
