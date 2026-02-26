from django.shortcuts import render,HttpResponse
from datetime import datetime, date,timedelta
from .models import device_logs,deviceconfig
from django.http import JsonResponse
import time
# Create your views here.
import os
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils.timezone import now
from django.shortcuts import render,redirect
from django.db import connection
import re
from GPS_App.context_processors import my_constants
def index(request):
    return render(request, 'index.html')


# teraterm_250318.log
def home(request):
    today_date =  date.today().strftime('%y%m%d')
    today_date_file = f'{today_date}'
    start_time = time.time()
    target_file = f"teraterm_{today_date_file}.log"

    def extract_value(line, key):
        try:
            return line.split(key)[1].split(',')[0].strip()
        except IndexError:
            return ''

    try:
        # Initialize all timing variables
        db_start = time.time()
        db_end = db_start
        file_start = time.time()
        file_end = file_start
        insert_start = time.time()
        insert_end = insert_start

        # Database query time
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT actual_date_time FROM gps_tracker.device_logs
                ORDER BY id DESC LIMIT 1;
            """)
            last_row = cursor.fetchone()
        db_end = time.time()

        if last_row is None:
            print("No data found in device_logs table.")
            last_actual_date_time = None
        else:
            last_data = last_row[0]  # Explicitly use the first (and only) column
            print('last_data:-', last_data)
            if isinstance(last_data, datetime):  # Check if it's already a datetime
                last_actual_date_time = last_data.strftime(
                    '%Y-%m-%d %H:%M:%S') + f".{last_data.microsecond // 1000:03d}"
            else:  # Handle case where it might be a string or other type
                try:
                    last_data = datetime.strptime(str(last_data), '%Y-%m-%d %H:%M:%S.%f')
                    last_actual_date_time = last_data.strftime(
                        '%Y-%m-%d %H:%M:%S') + f".{last_data.microsecond // 1000:03d}"
                except ValueError:
                    print("Error: actual_date_time is not in expected format")
                    last_actual_date_time = None

        # File processing time
        if not os.path.exists(target_file):
            print(f"File {target_file} not found!")
            file_end = time.time()
            return render(request, 'index.html')

        with open(target_file, 'r') as f:
            lines = f.readlines()
            start_index = 0

            if last_actual_date_time:
                for i, line in enumerate(lines):
                    if last_actual_date_time in line:
                        start_index = i + 1
                        break

            remaining_lines = lines[start_index:]
            file_end = time.time()

            # Data insertion time
            insert_start = time.time()
            for remaining_line in remaining_lines:
                if 'New Packet Received' in remaining_line and 'LAT' in remaining_line:
                    timestamp_match = remaining_line.split(']')[0].replace('[', '').strip()

                    current_device = extract_value(remaining_line, 'Current Device is:')
                    current_packet_number = extract_value(remaining_line, 'Current Packet Number is:')
                    device_id = extract_value(remaining_line, 'DEV_ID:')
                    PCKT_ID = extract_value(remaining_line, 'PCKT_ID:')
                    LAT = extract_value(remaining_line, 'LAT:')
                    LONG = extract_value(remaining_line, 'LONG:')
                    PCKT_NO = extract_value(remaining_line, 'PCKT_NO:')

                    raw_date = extract_value(remaining_line, 'DATE:').replace('/', '-')
                    try:
                        DATE = datetime.strptime(raw_date, "%d-%m-%Y").strftime("%Y-%m-%d")
                    except ValueError:
                        DATE = None

                    TIME = extract_value(remaining_line, 'TIME:')

                    with connection.cursor() as cursor:
                        cursor.execute("""
                            SELECT EXISTS (
                                SELECT 1
                                FROM gps_tracker.device_logs
                                WHERE actual_date_time = %s
                                AND device_id = %s
                            )
                        """, [timestamp_match, device_id])
                        exists = cursor.fetchone()[0]

                        if not exists:
                            device_conf, created = deviceconfig.objects.get_or_create(
                                device_id=device_id,
                                defaults={'is_active': True}
                            )

                            if not created:
                                device_conf.updated_at = now()
                                device_conf.save()
                            if PCKT_ID == 'SOS':
                                is_sound_play = 1
                            else:
                                is_sound_play = 0
                            device_logs.objects.create(
                                current_device=current_device,
                                current_packet_number=current_packet_number,
                                device_id=device_id,
                                pckt_id=PCKT_ID,
                                latitude=LAT,
                                longitude=LONG,
                                date=DATE,
                                time=TIME,
                                pckt_no=PCKT_NO,
                                actual_date_time=timestamp_match,
                                is_sound_play=is_sound_play
                            )
            insert_end = time.time()

    except Exception as e:
        print(f"Processing error: {e}")

    end_time = time.time()
    print(f"home execution time: {end_time - start_time:.3f} seconds")
    print(f"Database query time: {db_end - db_start:.3f} seconds")
    print(f"File processing time: {file_end - file_start:.3f} seconds")
    print(f"Data insertion time: {insert_end - insert_start:.3f} seconds")
    return render(request, 'index.html')
def get_device_locations(request):

    device_ids = request.GET.getlist('device_id')  # Get multiple device IDs from request (can be empty)
    date = request.GET.get('date')  # Get selected date
    interval_str = request.GET.get('time_filter')  # Default interval is '1m' (1 minute)

    # Require date, but allow device_ids to be optional
    if not date:
        return JsonResponse({"error": "Date is required."}, status=400)

    try:
        # Extract numeric value and time unit using regex
        match = re.match(r"(\d+)([sm])", interval_str)  # Example: "30s", "1m", "5m"
        if not match:
            return JsonResponse({"error": "Invalid interval format."}, status=400)

        value, unit = int(match.group(1)), match.group(2)

        # Convert to timedelta
        if unit == "s":  # Seconds
            interval = timedelta(seconds=value)
        else:  # Minutes
            interval = timedelta(minutes=value)

        # Base queryset with date filter
        queryset = device_logs.objects.filter(date=date)

        # If device_ids are provided, filter by them
        if device_ids and device_ids != ['']:
            queryset = queryset.filter(device_id__in=device_ids)

        # Check if any data exists
        if not queryset.exists():
            return JsonResponse({"error": f"No data available for the selected date: {date}."}, status=200)

        # Sort data by actual_date_time
        queryset = queryset.order_by('actual_date_time')

        # Grouping data based on the interval
        filtered_data = []
        last_time = None

        for device in queryset:
            actual_time = device.actual_date_time  # Ensure this is a datetime object

            if last_time is None or actual_time >= last_time + interval:
                filtered_data.append({
                    'device_id': device.device_id,
                    'latitude': str(device.latitude),
                    'longitude': str(device.longitude),
                    'id': device.id,
                    'pckt_id': device.pckt_id,
                    'actual_date_time': actual_time.strftime("%Y-%m-%d %H:%M:%S"),  # Convert datetime to string for JSON,
                    'is_marker_show':'True'
                })
                last_time = actual_time  # Update last timestamp
            else:
                filtered_data.append({
                    'device_id': device.device_id,
                    'latitude': str(device.latitude),
                    'longitude': str(device.longitude),
                    'id': device.id,
                    'pckt_id': device.pckt_id,
                    'actual_date_time': actual_time.strftime("%Y-%m-%d %H:%M:%S"),  # Convert datetime to string for JSON
                    'is_marker_show': 'False'
                })
        return JsonResponse(filtered_data, safe=False)

    except Exception as e:
        return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)


def get_device_ids(request):
    device_ids = device_logs.objects.values_list('device_id', flat=True).distinct()
    return JsonResponse(list(device_ids), safe=False)

# View to render the map
def show_map(request):
    constants = my_constants(request)
    username = request.session.get('user')
    if not username:
        return redirect('login')
    # if 'user' not in request.session:
    #     return redirect('login')
    return render(request, 'map.html',{'user': request.session.get('user')})

def get_device_configs(request):
    devices = deviceconfig.objects.all().values('device_id', 'is_active', 'color')
    return JsonResponse(list(devices), safe=False)

@csrf_exempt
def save_device_configs(request):
    if request.method == 'POST':
        try:
            # Check if body is empty
            if not request.body:
                return JsonResponse({
                    'success': False,
                    'error': 'No configuration data provided'
                })

            data = json.loads(request.body)

            # Validate data
            if not isinstance(data, list):
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid data format - list expected'
                })

            if not data:
                return JsonResponse({
                    'success': False,
                    'error': 'Empty configuration list'
                })

            # Process each config
            for config in data:
                # Validate required fields
                if 'device_id' not in config:
                    return JsonResponse({
                        'success': False,
                        'error': 'Device ID is required'
                    })

                if 'is_active' not in config or 'color' not in config:
                    return JsonResponse({
                        'success': False,
                        'error': 'Missing required configuration fields'
                    })

                try:
                    device, created = deviceconfig.objects.get_or_create(
                        device_id=config['device_id']
                    )
                    device.is_active = config['is_active']
                    device.color = config['color']
                    device.save()
                except Exception as e:
                    return JsonResponse({
                        'success': False,
                        'error': f'Error saving device {config["device_id"]}: {"Duplicate color entry"}'
                    })

            return JsonResponse({
                'success': True,
                'message': 'Device configurations saved successfully'
            })

        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'Invalid JSON format'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Unexpected error: {str(e)}'
            })
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method - POST required'
    })
def get_device_emergency_alarms(request):
    # Get today's date (March 9, 2025, based on system date)
    today = date.today()  # This will be 2025-03-09 based on your provided current date

    # Filter SOS alerts for today only, ordered by timestamp (most recent first)
    sos_devices = device_logs.objects.filter(
        pckt_id='sos',
        date=today  # Filter by today's dat
    ).order_by('-actual_date_time') # Limit to last 10 SOS

    sos_data = []
    for device in sos_devices:
        formatted_timestamp = device.actual_date_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        sos_data.append({

            'id': device.id,
            'device_id': device.device_id,
            'latitude': device.latitude,
            'longitude': device.longitude,
            'timestamp': formatted_timestamp,
            'pckt_id': device.pckt_id,
            'is_sound_play':device.is_sound_play
        })

    return JsonResponse(sos_data, safe=False)

def get_device_emergency_alarms_stop(request):
    # Filter SOS alerts for today only, ordered by timestamp (most recent first)
    try:
        device_logs.objects.filter(pckt_id='sos').update(is_sound_play=0)
        return JsonResponse({'success': 'True', 'message': 'SOS sound stopped successfully'})
    except Exception as e:
        return JsonResponse({'success': 'False', 'message': f'{e}'})

