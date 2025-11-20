"""
Flask Web Application for EDA Data Visualization
Structure: Mirrors ASP.NET MVC Pattern
- Routes → Controllers
- render_template → Views
- Data processing → Models/Services
"""

from flask import Flask, render_template, request, jsonify, send_file, send_from_directory, Response
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import os
import re
from werkzeug.utils import secure_filename
from datetime import datetime
import pytz
import json
import mimetypes

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['VIDEO_FOLDER'] = 'static/videos'
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024 * 1024  # 2GB max file size
app.config['ALLOWED_EXTENSIONS'] = {'csv'}
app.config['ALLOWED_VIDEO_EXTENSIONS'] = {'mp4', 'webm', 'ogg', 'mov', 'avi'}

# Ensure upload folder exists
Path(app.config['UPLOAD_FOLDER']).mkdir(exist_ok=True)
Path(app.config['VIDEO_FOLDER']).mkdir(parents=True, exist_ok=True)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def allowed_video(filename):
    """Check if video file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_VIDEO_EXTENSIONS']

def process_eda_file(filepath):
    """
    Process EDA CSV file and extract data
    Similar to a Service/Repository pattern in ASP.NET
    """
    try:
        # First, try to read with headers
        df = pd.read_csv(filepath)
        
        # Check if the file has no headers (all columns are numeric)
        if all(df.columns.astype(str).str.match(r'^\d+\.?\d*$')):
            print("DEBUG: File has no headers, treating as headerless data")
            # Re-read without headers
            df = pd.read_csv(filepath, header=None)
            
            # If there's only one column, assume it's EDA data with metadata in first rows
            if len(df.columns) == 1:
                # Check if first value is a UNIX timestamp (very large number)
                first_val = df.iloc[0, 0]
                
                if first_val > 1000000000:  # Likely a UNIX timestamp
                    print(f"DEBUG: First value is UNIX timestamp: {first_val}")
                    base_timestamp = first_val
                    
                    # Second value might be sampling rate (Hz)
                    sampling_rate = df.iloc[1, 0] if len(df) > 1 else 4.0
                    print(f"DEBUG: Sampling rate: {sampling_rate} Hz")
                    
                    # Skip first 2 rows (metadata)
                    df = df.iloc[2:].reset_index(drop=True)
                    eda_column = 0
                    
                    # Generate timestamps based on sampling rate
                    # Convert Hz to seconds between samples
                    seconds_per_sample = 1.0 / sampling_rate
                    
                    # Create timestamps for each sample
                    timestamps = [base_timestamp + (i * seconds_per_sample) for i in range(len(df))]
                    df['datetime'] = pd.to_datetime(timestamps, unit='s', utc=True)
                    df['datetime'] = df['datetime'].dt.tz_convert('US/Eastern')
                else:
                    # No metadata, just EDA values
                    eda_column = 0
                    # Generate timestamps based on row index (assuming 1-minute intervals)
                    df['datetime'] = pd.date_range(start='2025-01-01 00:00:00', periods=len(df), freq='1min')
                    df['datetime'] = df['datetime'].dt.tz_localize('UTC').dt.tz_convert('US/Eastern')
            else:
                # Multiple columns - assume first is timestamp, second is EDA
                timestamp_column = 0
                eda_column = 1 if len(df.columns) > 1 else 0
                
                # Try to parse first column as timestamp
                try:
                    # Check if it's UNIX timestamp
                    if df[timestamp_column].dtype in ['int64', 'float64']:
                        df['datetime'] = pd.to_datetime(df[timestamp_column], unit='s', utc=True)
                        df['datetime'] = df['datetime'].dt.tz_convert('US/Eastern')
                    else:
                        df['datetime'] = pd.to_datetime(df[timestamp_column], utc=True)
                        df['datetime'] = df['datetime'].dt.tz_convert('US/Eastern')
                except:
                    # If timestamp parsing fails, use index
                    df['datetime'] = pd.date_range(start='2025-01-01 00:00:00', periods=len(df), freq='1min')
                    df['datetime'] = df['datetime'].dt.tz_localize('UTC').dt.tz_convert('US/Eastern')
        else:
            # File has headers - use existing logic
            # Detect EDA column (flexible naming)
            eda_column = None
            possible_columns = ['eda_scl_usiemens', 'eda', 'EDA', 'skin_conductance', 'scl', 'electrodermal']
            
            for col in possible_columns:
                if col in df.columns:
                    eda_column = col
                    break
            
            if not eda_column:
                # Try to find any column with 'eda' in the name
                for col in df.columns:
                    if 'eda' in str(col).lower():
                        eda_column = col
                        break
            
            if not eda_column:
                # Show available columns to help user
                available_cols = ', '.join(df.columns.tolist())
                return None, f"No EDA column found in CSV file. Available columns: {available_cols}"
            
            # Detect timestamp column
            timestamp_column = None
            timestamp_unix_column = None
            possible_ts = ['timestamp_iso', 'timestamp', 'time', 'datetime']
            
            # Check for UNIX timestamp column first
            if 'timestamp_unix' in df.columns:
                timestamp_unix_column = 'timestamp_unix'
            
            for col in possible_ts:
                if col in df.columns:
                    timestamp_column = col
                    break
            
            # Convert timestamps to EST 12-hour format
            est = pytz.timezone('US/Eastern')
            
            if timestamp_unix_column:
                # Convert UNIX timestamps (milliseconds) to datetime in EST
                df['datetime'] = pd.to_datetime(df[timestamp_unix_column], unit='ms', utc=True)
                df['datetime'] = df['datetime'].dt.tz_convert(est)
            elif timestamp_column:
                # Parse ISO or other timestamp formats
                try:
                    df['datetime'] = pd.to_datetime(df[timestamp_column], utc=True)
                    df['datetime'] = df['datetime'].dt.tz_convert(est)
                except:
                    df['datetime'] = pd.to_datetime(df[timestamp_column])
                    # If no timezone info, assume UTC and convert to EST
                    if df['datetime'].dt.tz is None:
                        df['datetime'] = df['datetime'].dt.tz_localize('UTC').dt.tz_convert(est)
            else:
                # Use index as timestamp
                df['datetime'] = pd.date_range(start='2025-01-01 00:00:00', periods=len(df), freq='1min')
                df['datetime'] = df['datetime'].dt.tz_localize('UTC').dt.tz_convert('US/Eastern')
        
        # Format datetime as 12-hour EST time
        if hasattr(df['datetime'].iloc[0], 'strftime'):
            df['time_display'] = df['datetime'].dt.strftime('%I:%M:%S %p EST')
            df['date_display'] = df['datetime'].dt.strftime('%m/%d/%Y')
        else:
            df['time_display'] = df['datetime'].astype(str)
            df['date_display'] = 'N/A'
        
        # Convert EDA to numeric
        df[eda_column] = pd.to_numeric(df[eda_column], errors='coerce')
        
        # Remove missing values
        df_clean = df[df[eda_column].notna()].copy()
        
        if len(df_clean) == 0:
            return None, "No valid EDA data found in file"
        
        # Calculate statistics
        stats = {
            'mean': float(df_clean[eda_column].mean()),
            'std': float(df_clean[eda_column].std()),
            'min': float(df_clean[eda_column].min()),
            'max': float(df_clean[eda_column].max()),
            'count': len(df_clean),
            'missing': len(df) - len(df_clean),
            'start_time': df_clean['time_display'].iloc[0] if len(df_clean) > 0 else 'N/A',
            'end_time': df_clean['time_display'].iloc[-1] if len(df_clean) > 0 else 'N/A',
            'date': df_clean['date_display'].iloc[0] if len(df_clean) > 0 else 'N/A'
        }
        
        # Calculate seconds from start for video sync
        first_datetime = df_clean['datetime'].iloc[0]
        df_clean['seconds_from_start'] = (df_clean['datetime'] - first_datetime).dt.total_seconds()
        
        # Prepare data for plotting
        plot_data = {
            'timestamps': df_clean['time_display'].tolist(),
            'timestamps_raw': df_clean['datetime'].astype(str).tolist(),
            'seconds_from_start': df_clean['seconds_from_start'].tolist(),
            'eda_values': df_clean[eda_column].tolist(),
            'participant_id': df_clean['participant_full_id'].iloc[0] if 'participant_full_id' in df_clean.columns else 'Unknown',
            'first_datetime': first_datetime  # Store for offset calculation
        }
        
        return {'data': plot_data, 'stats': stats}, None
        
    except Exception as e:
        import traceback
        print(f"ERROR in process_eda_file: {traceback.format_exc()}")
        return None, f"Error processing file: {str(e)}"

def create_eda_plot(data, stats, video_url=None, video_offset=0, video_duration=None):
    """
    Create interactive Plotly visualization with optional video sync
    If video is provided, only show EDA data for the video duration window
    Similar to a View Helper in ASP.NET
    """
    timestamps = data['timestamps']  # 12-hour EST formatted strings
    eda_values = data['eda_values']
    seconds_from_start = data['seconds_from_start']
    participant_id = data['participant_id']
    
    # Filter data to video duration if video is uploaded
    if video_url and video_duration:
        # Calculate the time window for the video
        # video_offset is how many seconds the video started after data collection
        video_start_in_data = video_offset  # seconds from data start
        video_end_in_data = video_offset + video_duration
        
        # Filter to only data points within video duration
        filtered_indices = [
            i for i, sec in enumerate(seconds_from_start)
            if video_start_in_data <= sec <= video_end_in_data
        ]
        
        if filtered_indices:
            timestamps = [timestamps[i] for i in filtered_indices]
            eda_values = [eda_values[i] for i in filtered_indices]
            seconds_from_start = [seconds_from_start[i] for i in filtered_indices]
            
            # Update stats for filtered data
            stats = stats.copy()
            stats['mean'] = sum(eda_values) / len(eda_values) if eda_values else 0
            stats['min'] = min(eda_values) if eda_values else 0
            stats['max'] = max(eda_values) if eda_values else 0
            stats['count'] = len(eda_values)
            stats['start_time'] = timestamps[0] if timestamps else 'N/A'
            stats['end_time'] = timestamps[-1] if timestamps else 'N/A'
    
    # Create figure
    fig = go.Figure()
    
    # Add EDA trace
    fig.add_trace(go.Scatter(
        x=timestamps,
        y=eda_values,
        mode='lines',
        name='EDA Signal',
        line=dict(color='steelblue', width=2),
        fill='tozeroy',
        fillcolor='rgba(70, 130, 180, 0.2)',
        customdata=list(range(len(timestamps))),  # Add index for video sync
        hovertemplate='<b>Time:</b> %{x}<br><b>EDA:</b> %{y:.3f} µS<extra></extra>'
    ))
    
    # Add mean line
    fig.add_hline(
        y=stats['mean'],
        line_dash="dash",
        line_color="red",
        annotation_text=f"Mean: {stats['mean']:.3f} µS",
        annotation_position="right"
    )
    
    # Update layout with session info
    title_text = f'Electrodermal Activity - {participant_id}'
    if stats.get('date') and stats['date'] != 'N/A':
        if video_url and video_duration:
            title_text += f"<br><sub>Session: {stats['date']} (Video Duration Window: {stats['start_time']} - {stats['end_time']})</sub>"
        else:
            title_text += f"<br><sub>Session: {stats['date']} ({stats['start_time']} - {stats['end_time']})</sub>"
    
    fig.update_layout(
        title=title_text,
        xaxis_title='Time (EST)',
        yaxis_title='EDA (µSiemens)',
        hovermode='x unified',
        template='plotly_white',
        height=400,
        margin=dict(l=50, r=50, t=100, b=50)
    )
    
    # Configure x-axis to show every Nth label to avoid crowding
    total_points = len(timestamps)
    if total_points > 50:
        # Show approximately 10-15 labels
        tick_interval = max(1, total_points // 12)
        fig.update_xaxes(
            tickmode='linear',
            tick0=0,
            dtick=tick_interval,
            tickangle=-45
        )
    
    # Add range slider
    fig.update_xaxes(rangeslider_visible=True)
    
    # Return HTML with Plotly.js included
    return fig.to_html(full_html=False, include_plotlyjs=True, div_id='plotly-chart')


def parse_video_start_time_from_filename(filename):
    """
    Parse video start time from filename format:
    Example: "SYS1Cam3--2018-05-14_10_22_27_frames_1-9470.mp4"
    Returns: "10:22:27" (HH:MM:SS format) or None if not found
    """
    # Pattern to match YYYY-MM-DD_HH_MM_SS in the filename
    # This handles both underscore and dash separators
    pattern = r'(\d{4})-(\d{2})-(\d{2})[_-](\d{2})[_-](\d{2})[_-](\d{2})'
    match = re.search(pattern, filename)
    
    if match:
        year, month, day, hour, minute, second = match.groups()
        # Return just the time portion in HH:MM:SS format
        time_str = f"{hour}:{minute}:{second}"
        print(f"DEBUG: Parsed video start time from filename '{filename}': {time_str}")
        return time_str
    else:
        print(f"DEBUG: Could not parse video start time from filename '{filename}'")
        return None


# ========== ROUTES (Controllers in ASP.NET) ==========

@app.route('/')
def index():
    """
    Home page - equivalent to HomeController.Index() in ASP.NET
    """
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Handle file upload - equivalent to [HttpPost] action in ASP.NET
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    video_file = request.files.get('video')  # Optional video file
    video_start_time = request.form.get('video_start_time')  # Optional video start time
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Please upload a CSV file.'}), 400
    
    try:
        # Save CSV file securely
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Process the file
        result, error = process_eda_file(filepath)
        
        if error:
            return jsonify({'error': error}), 400
        
        # Handle video upload if provided
        video_url = None
        video_offset_seconds = 0
        video_format_warning = None
        parsed_time = None  # Track if we auto-detected the time
        
        if video_file and video_file.filename != '' and allowed_video(video_file.filename):
            video_filename = secure_filename(video_file.filename)
            video_filename = f"{timestamp}_{video_filename}"
            video_path = os.path.join(app.config['VIDEO_FOLDER'], video_filename)
            video_file.save(video_path)
            video_url = f"/static/videos/{video_filename}"
            print(f"DEBUG: Video saved to {video_path}")
            
            # Try to parse video start time from filename first
            parsed_time = parse_video_start_time_from_filename(video_file.filename)
            if parsed_time and not video_start_time:
                video_start_time = parsed_time
                print(f"DEBUG: Using auto-detected video start time: {video_start_time}")
            elif video_start_time:
                print(f"DEBUG: Using manually provided video start time: {video_start_time}")
            else:
                print(f"DEBUG: No video start time available (neither auto-detected nor manual)")
            
            # Check if video format is browser-compatible
            ext = video_filename.rsplit('.', 1)[1].lower()
            if ext == 'avi':
                video_format_warning = (
                    "⚠️ AVI format has limited browser support. "
                    "If the video doesn't play, try a different browser (Firefox sometimes works better with AVI). "
                    "MP4 format is recommended for best compatibility across all browsers."
                )
            elif ext not in ['mp4', 'webm', 'ogg']:
                video_format_warning = f"⚠️ {ext.upper()} format may not play in all browsers. MP4 is recommended for best compatibility."
            
            # Calculate video offset if start time provided
            if video_start_time and result['data'].get('timestamps_raw'):
                try:
                    # Parse video start time in EST
                    est = pytz.timezone('US/Eastern')
                    
                    # Get the date from the first data point
                    first_data_time_str = result['data']['timestamps_raw'][0]
                    first_data_time = pd.to_datetime(first_data_time_str)
                    
                    # If timezone-naive, localize to EST
                    if first_data_time.tzinfo is None:
                        first_data_time = est.localize(first_data_time)
                    else:
                        # Convert to EST if different timezone
                        first_data_time = first_data_time.astimezone(est)
                    
                    video_date = first_data_time.date()
                    
                    # Parse the video start time (could be HH:MM:SS or HH:MM)
                    if len(video_start_time.split(':')) == 2:
                        video_start_time += ':00'  # Add seconds if not provided
                    
                    # Create a datetime object for video start (timezone-naive first)
                    video_start_dt = datetime.strptime(f"{video_date} {video_start_time}", '%Y-%m-%d %H:%M:%S')
                    # Then localize to EST
                    video_start_dt = est.localize(video_start_dt)
                    
                    # Calculate offset in seconds: how many seconds after data start did video start?
                    # Positive = video started after data collection began
                    # Negative = video started before data collection (unusual)
                    video_offset_seconds = (video_start_dt - first_data_time).total_seconds()
                    
                    print(f"DEBUG: Data start time: {first_data_time}")
                    print(f"DEBUG: Video start time: {video_start_dt}")
                    print(f"DEBUG: Video offset: {video_offset_seconds} seconds ({video_offset_seconds/60:.2f} minutes)")
                    
                except Exception as e:
                    import traceback
                    print(f"WARNING: Could not parse video start time: {e}")
                    print(f"TRACEBACK: {traceback.format_exc()}")
                    video_offset_seconds = 0
        
        # Create visualization - video duration will be determined client-side
        plot_html = create_eda_plot(result['data'], result['stats'], video_url, video_offset_seconds, video_duration=None)
        
        # Debug: Print plot HTML length
        print(f"DEBUG: Plot HTML generated, length: {len(plot_html)} characters")
        print(f"DEBUG: Stats: {result['stats']}")
        print(f"DEBUG: Video URL: {video_url}")
        
        # Prepare response with video info message
        video_info_message = None
        if video_url and parsed_time:
            video_info_message = f"✅ Video start time auto-detected from filename: {parsed_time}"
        elif video_url and video_start_time:
            video_info_message = f"✅ Using manually entered video start time: {video_start_time}"
        
        return jsonify({
            'success': True,
            'stats': result['stats'],
            'plot_html': plot_html,
            'participant_id': result['data']['participant_id'],
            'video_url': video_url,
            'video_offset_seconds': video_offset_seconds,
            'video_info_message': video_info_message,
            'data_points': len(result['data']['timestamps']),
            'timestamps': result['data']['timestamps'],  # Send formatted timestamps
            'timestamps_seconds': result['data']['seconds_from_start'],  # Send seconds for sync
            'eda_values': result['data']['eda_values'],  # Send values for client-side display
            'video_warning': video_format_warning  # Warning about unsupported formats
        })
        
    except Exception as e:
        import traceback
        print(f"ERROR: {traceback.format_exc()}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/about')
def about():
    """
    About page - demonstrates multiple views
    """
    return render_template('about.html')


@app.route('/static/videos/<filename>')
def serve_video(filename):
    """
    Serve video files with proper MIME types and headers for AVI support
    """
    video_path = os.path.join(app.config['VIDEO_FOLDER'], filename)
    
    # Determine MIME type based on file extension
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    mime_types = {
        'mp4': 'video/mp4',
        'webm': 'video/webm',
        'ogg': 'video/ogg',
        'avi': 'video/x-msvideo',
        'mov': 'video/quicktime'
    }
    
    mimetype = mime_types.get(ext, 'application/octet-stream')
    
    # Use send_file with explicit mimetype and support for range requests
    return send_file(
        video_path,
        mimetype=mimetype,
        as_attachment=False,
        conditional=True  # Enables range request support for video seeking
    )


if __name__ == '__main__':
    print("\n" + "="*60)
    print("EDA Visualization Web Application")
    print("="*60)
    print("\nStarting Flask development server...")
    print("Navigate to: http://127.0.0.1:5000")
    print("\nPress CTRL+C to stop the server")
    print("="*60 + "\n")
    
    app.run(debug=True, host='127.0.0.1', port=5000)
