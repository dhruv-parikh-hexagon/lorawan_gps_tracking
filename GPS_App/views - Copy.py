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


# def home(request):
#     # Define file paths
#     source_file = "FTD 05JAN 25 1120"
#     target_file = r"C:\Users\Admin\Desktop\Dhruv\GPS_Tracking\FTD 05JAN 25 1120 New"
#
#     def extract_value(line, key):
#         try:
#             return line.split(key)[1].split(',')[0].strip()
#         except IndexError:
#             return ''
#
#     # Step 1: Transfer all lines from source to target
#     try:
#         with open(source_file, "r") as source, open(target_file, "a") as target:
#             lines_transferred = 0
#             for line in source:
#                 timestamp_match = line.split(']')[0].replace('[', '').strip()
#                 device_id = extract_value(line, 'DEV_ID:')
#
#                 # Raw SQL query replacing .exists()
#                 with connection.cursor() as cursor:
#                     cursor.execute("""
#                         SELECT EXISTS (
#                             SELECT 1
#                             FROM gps_tracker.device_logs
#                             WHERE actual_date_time = %s
#                             AND device_id = %s
#                         )
#                     """, [timestamp_match, device_id])
#                     last_data = cursor.fetchone()[0]
#
#
#                 if not last_data:  # Changed from last_data == False
#                     target.write(line)
#                     # target.truncate(0)
#
#                 lines_transferred += 1
#
#     except Exception as e:
#         print(f"Error transferring lines: {e}")
#
#     # Step 2: Process the target file
#     try:
#         with open(target_file, 'r') as f:
#             lines = f.readlines()
#
#         new_lines = []
#         for line in lines:
#             try:
#                 if 'Discarding' in line:
#                     new_lines.append(line)
#                     continue
#
#                 if "New Packet Received" in line:
#                     timestamp_match = line.split(']')[0].replace('[', '').strip()
#
#                 # Extract values
#                 current_device = extract_value(line, 'Current Device is:')
#                 current_packet_number = extract_value(line, 'Current Packet Number is:')
#                 device_id = extract_value(line, 'DEV_ID:')
#                 PCKT_ID = extract_value(line, 'PCKT_ID:')
#                 LAT = extract_value(line, 'LAT:')
#                 LONG = extract_value(line, 'LONG:')
#                 PCKT_NO = extract_value(line, 'PCKT_NO:')
#
#
#                 # Date Parsing
#                 raw_date = extract_value(line, 'DATE:').replace('/', '-')
#                 try:
#                     DATE = datetime.strptime(raw_date, "%d-%m-%Y").strftime("%Y-%m-%d")
#                 except ValueError:
#                     DATE = None
#
#                 TIME = extract_value(line, 'TIME:')
#
#                 # Raw SQL query replacing .exists()
#                 with connection.cursor() as cursor:
#                     cursor.execute("""
#                         SELECT EXISTS (
#                             SELECT 1
#                             FROM gps_tracker.device_logs
#                             WHERE actual_date_time = %s
#                             AND device_id = %s
#                         )
#                     """, [timestamp_match, device_id])
#                     last_data = cursor.fetchone()[0]
#
#
#                 if not last_data:  # Changed from last_data == False
#                     # Get or create device configuration
#                     device_conf, created = deviceconfig.objects.get_or_create(
#                         device_id=device_id,
#                         defaults={
#                             'is_active': True,  # Set as active when first seen
#
#                         }
#                     )
#
#                     # If the device already exists, update the updated_at field
#                     if not created:
#                         device_conf.updated_at = now()
#                         device_conf.save()
#
#                     # Insert into Django model
#                     device_logs.objects.create(
#                         current_device=current_device,
#                         current_packet_number=current_packet_number,
#                         device_id=device_id,
#                         pckt_id=PCKT_ID,
#                         latitude=LAT,
#                         longitude=LONG,
#                         date=DATE,
#                         time=TIME,
#                         pckt_no=PCKT_NO,
#                         actual_date_time=timestamp_match
#                     )
#             except Exception as e:
#                 print("Insert Error:", e)
#                 new_lines.append(line)
#
#         # Step 3: Write back unprocessed lines
#         with open(target_file, 'r+') as f:
#             f.truncate(0)
#
#     except Exception as e:
#         print(f"Processing error: {e}")
#
#     return render(request, 'index.html')


def home(request):
    # Define file paths
    source_file = r"C:\Users\DELL\AppData\Local\teraterm5\teraterm.log"
    target_file = r"FTD 05JAN 25 1120 New"

    def extract_value(line, key):
        try:
            return line.split(key)[1].split(',')[0].strip()
        except IndexError:
            return ''

    # Step 1: Transfer lines from source to target (limited to new entries)
    try:
        with open(source_file, "r") as source, open(target_file, "a") as target:
            for line in source:
                timestamp_match = line.split(']')[0].replace('[', '').strip()
                device_id = extract_value(line, 'DEV_ID:')

                if device_id:
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
                        target.write(line)
                        break  # Only process one line at a time

    except Exception as e:
        print(f"Error transferring lines: {e}")

    # Step 2: Process one line from target file and delete it
    try:
        with open(target_file, 'r') as f:
            lines = f.readlines()

        if lines:  # Check if there are any lines to process
            line = lines[0]  # Take only the first line

            try:
                if 'Discarding' in line:
                    pass  # Skip discarded lines
                elif "New Packet Received" in line:
                    timestamp_match = line.split(']')[0].replace('[', '').strip()

                    current_device = extract_value(line, 'Current Device is:')
                    current_packet_number = extract_value(line, 'Current Packet Number is:')
                    device_id = extract_value(line, 'DEV_ID:')
                    PCKT_ID = extract_value(line, 'PCKT_ID:')
                    LAT = extract_value(line, 'LAT:')
                    LONG = extract_value(line, 'LONG:')
                    PCKT_NO = extract_value(line, 'PCKT_NO:')

                    raw_date = extract_value(line, 'DATE:').replace('/', '-')
                    try:
                        DATE = datetime.strptime(raw_date, "%d-%m-%Y").strftime("%Y-%m-%d")
                    except ValueError:
                        DATE = None

                    TIME = extract_value(line, 'TIME:')

                    # Verify if record doesn't exist
                    with connection.cursor() as cursor:
                        cursor.execute("""
                            SELECT EXISTS (
                                SELECT 1 
                                FROM gps_tracker.device_logs 
                                WHERE actual_date_time = %s 
                                AND device_id = %s
                            )
                        """, [timestamp_match, device_id])
                        last_data = cursor.fetchone()[0]

                    if not last_data:
                        # Insert one record
                        device_conf, created = deviceconfig.objects.get_or_create(
                            device_id=device_id,
                            defaults={'is_active': True}
                        )

                        if not created:
                            device_conf.updated_at = now()
                            device_conf.save()

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
                            actual_date_time=timestamp_match
                        )

            except Exception as e:
                print("Insert Error:", e)

            # Delete the processed line by rewriting file with remaining lines
            with open(target_file, 'w') as f:
                f.writelines(lines[1:])  # Write all lines except the first one

    except Exception as e:
        print(f"Processing error: {e}")

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
        date=today  # Filter by today's date
    ).order_by('-actual_date_time') # Limit to last 10 SOS

    sos_data = []
    for device in sos_devices:
        sos_data.append({
            'id': device.id,
            'device_id': device.device_id,
            'latitude': device.latitude,
            'longitude': device.longitude,
            'timestamp': device.actual_date_time,
            'pckt_id': device.pckt_id
        })

    return JsonResponse(sos_data, safe=False)