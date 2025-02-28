import json
import os
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Athlete, Coach, VideoStatus

from django.conf import settings
from django.shortcuts import render

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe_publishable_key = settings.STRIPE_PUBLISHABLE_KEY


import logging
logger = logging.getLogger(__name__)


User = get_user_model()

@csrf_exempt
@csrf_exempt
def register(request):
    print("Register view called: ", request)
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            # Create User
            user = User.objects.create_user(
                username=data['email'],
                email=data['email'],
                password=data['password'],
                first_name=data['first_name'],
                last_name=data['last_name']
            )
            user.save()

            # Create Athlete
            athlete = Athlete.objects.create(
                user=user,
                email=data['email'],
                first_name=data['first_name'],
                last_name=data['last_name']
            )
            athlete.save()

            # Create Coach
            coach = Coach.objects.create(
                user=user,
                email=data['email'],
                first_name=data['first_name'],
                last_name=data['last_name']
            )
            coach.save()

            # Create Stripe Checkout Session
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'eur',  # or any other currency
                            'product_data': {
                                'name': 'Yekar',
                            },
                            'unit_amount': 696,  # Price in cents ($20.00)
                        },
                        'quantity': 1,
                    },
                ],
                mode='subscription',  # Use 'subscription' for recurring payments
                success_url='http://localhost:8000/success/',
                cancel_url='http://localhost:8000/cancel/',
            )

            # Return the session ID for frontend redirection
            return JsonResponse({
                'message': 'User, Athlete, and Coach created successfully',
                'sessionId': checkout_session.id  # Stripe session ID
            })

        except KeyError as e:
            return JsonResponse({
                'message': f'Missing required field: {str(e)}',
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'message': f'An error occurred: {str(e)}',
            }, status=500)
    elif request.method == 'GET':
        return render(request, 'front/register.html')
    return JsonResponse({'message': 'Invalid request method'}, status=405)


def get_stripe_key(request):
    return JsonResponse({
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY
    })



@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            form = AuthenticationForm(request, data=data)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                return JsonResponse({'message': 'Login successful', 'redirect_url': '/prototype'})
            else:
                print("Form errors:", form.errors)  # Debug print
                return JsonResponse({'errors': form.errors}, status=400)
        except json.JSONDecodeError:
            print("Invalid JSON")  # Debug print
            return JsonResponse({'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            print("Unexpected error:", str(e))  # Debug print
            return JsonResponse({'message': 'An unexpected error occurred'}, status=500)
    elif request.method == 'GET':
        print("Received GET request")  # Debug print
        return render(request, 'front/login.html')
    else:
        print("Invalid request method")  # Debug print
        return JsonResponse({'message': 'Invalid request method'}, status=405)


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'message': 'Logout successful'})
    return JsonResponse({'message': 'Invalid request method'}, status=405)

@login_required
def get_athlete_id(request):
    user = request.user
    try:
        athlete = user.athlete
        return JsonResponse({'athlete_id': athlete.id})
    except Athlete.DoesNotExist:
        return JsonResponse({'error': 'Athlete not found'}, status=404)
    
@login_required
def get_user_role(request):
    user = request.user
    roles = {
        'is_coach': False,
        'is_athlete': False,
        'coach_id': None,
        'athlete_id': None
    }
    try:
        coach = Coach.objects.get(user=user)
        roles['is_coach'] = True
        roles['coach_id'] = coach.id
    except Coach.DoesNotExist:
        pass

    try:
        athlete = Athlete.objects.get(user=user)
        roles['is_athlete'] = True
        roles['athlete_id'] = athlete.id
    except Athlete.DoesNotExist:
        pass

    return JsonResponse(roles)


@login_required
def get_video_status_for_athlete(request, athlete_id):
    athlete = Athlete.objects.get(id=athlete_id)
    video_statuses = VideoStatus.objects.filter(athlete=athlete)

    data = []
    for video_status in video_statuses:
        video_status_data = {
            'id': video_status.id,
            'video_token': video_status.video_token,
            'status': video_status.status,
            'src_path': video_status.src_path,
            'tracks_path': video_status.tracks_path,
            'track_picking_frame_path': video_status.track_picking_frame_path,
            'track_picking_frame_idx': video_status.track_picking_frame_idx,
            'm_per_pixel': video_status.m_per_pixel,
            'processed_path': video_status.processed_path,
            'created_at': video_status.created_at,
            'updated_at': video_status.updated_at,
            'size_kb': video_status.size_kb,
            'video_hash': video_status.video_hash,
            'error_message': video_status.error_message,
            'bar_load': video_status.bar_load,
            'exercise_name': video_status.exercise_name,
            # Include set_info data if it exists
            'set_info': {
                'bar_load': video_status.set_info.bar_load,
                'reps': video_status.set_info.reps,
                'expected_1RM': video_status.set_info.expected_1RM,
                'eccentric_times': video_status.set_info.eccentric_times,
                'pause_times': video_status.set_info.pause_times,
                'concentric_times': video_status.set_info.concentric_times,
                'mean_concentric_speed': video_status.set_info.mean_concentric_speed,
                'percent_lost_concentric_speed_json': video_status.set_info.percent_lost_concentric_speed_json,
                'rom': video_status.set_info.rom,
                'leg_angle_over_time': video_status.set_info.leg_angle_over_time,
                'torso_angle_over_time': video_status.set_info.torso_angle_over_time,
                'bar_positions_x': video_status.set_info.bar_positions_x,
                'bar_positions_y': video_status.set_info.bar_positions_y,
                'hip_positions_x': video_status.set_info.hip_positions_x,
                'hip_positions_y': video_status.set_info.hip_positions_y,
                'knee_positions_x': video_status.set_info.knee_positions_x,
                'knee_positions_y': video_status.set_info.knee_positions_y,
                'shoulder_positions_x': video_status.set_info.shoulder_positions_x,
                'shoulder_positions_y': video_status.set_info.shoulder_positions_y,
                'bar_x_displacement': video_status.set_info.bar_x_displacement,
                'depth_over_time': video_status.set_info.depth_over_time,
                'max_depth': video_status.set_info.max_depth,
                'power_data': video_status.set_info.power_data,
                'created_at': video_status.set_info.created_at,
                'updated_at': video_status.set_info.updated_at,
            } if hasattr(video_status, 'set_info') else None
        }
        data.append(video_status_data)

    return JsonResponse(data, safe=False)

@login_required
def get_video_status_with_token(request, token):
    video_status = VideoStatus.objects.get(video_token=token)
    data = {
        'id': video_status.id,
        'video_token': video_status.video_token,
        'status': video_status.status,
        'src_path': video_status.src_path,
        'tracks_path': video_status.tracks_path,
        'track_picking_frame_path': video_status.track_picking_frame_path,
        'track_picking_frame_idx': video_status.track_picking_frame_idx,
        'm_per_pixel': video_status.m_per_pixel,
        'processed_path': video_status.processed_path,
        'created_at': video_status.created_at,
        'updated_at': video_status.updated_at,
        'size_kb': video_status.size_kb,
        'video_hash': video_status.video_hash,
        'error_message': video_status.error_message,
        'bar_load': video_status.bar_load,
        'exercise_name': video_status.exercise_name,
        'process_fps': video_status.process_fps,
        # Include set_info data if it exists
        'set_info': {
            'bar_load': video_status.set_info.bar_load,
            'reps': video_status.set_info.reps,
            'expected_1RM': video_status.set_info.expected_1RM,
            'eccentric_times': video_status.set_info.eccentric_times,
            'pause_times': video_status.set_info.pause_times,
            'concentric_times': video_status.set_info.concentric_times,
            'mean_concentric_speed': video_status.set_info.mean_concentric_speed,
            'percent_lost_concentric_speed_json': video_status.set_info.percent_lost_concentric_speed_json,
            'rom': video_status.set_info.rom,
            'leg_angle_over_time': video_status.set_info.leg_angle_over_time,
            'torso_angle_over_time': video_status.set_info.torso_angle_over_time,
            'eccentric_starts': video_status.set_info.eccentric_starts,
            'eccentric_ends': video_status.set_info.eccentric_ends,
            'concentric_starts': video_status.set_info.concentric_starts,
            'concentric_ends': video_status.set_info.concentric_ends,
            'bar_positions_x': video_status.set_info.bar_positions_x,
            'bar_positions_y': video_status.set_info.bar_positions_y,
            'hip_positions_x': video_status.set_info.hip_positions_x,
            'hip_positions_y': video_status.set_info.hip_positions_y,
            'knee_positions_x': video_status.set_info.knee_positions_x,
            'knee_positions_y': video_status.set_info.knee_positions_y,
            'shoulder_positions_x': video_status.set_info.shoulder_positions_x,
            'shoulder_positions_y': video_status.set_info.shoulder_positions_y,
            'bar_x_displacement': video_status.set_info.bar_x_displacement,
            'depth_over_time': video_status.set_info.depth_over_time,
            'max_depth': video_status.set_info.max_depth,
            'power_data': video_status.set_info.power_data,
            'created_at': video_status.set_info.created_at,
            'updated_at': video_status.set_info.updated_at,
        } if hasattr(video_status, 'set_info') else None,
        
        'advanced_data': {
            'sticking_mask': video_status.advanced_data.sticking_mask,
            'bar_vertical_rom_percentage': video_status.advanced_data.bar_vertical_rom_percentage,
        } if hasattr(video_status, 'advanced_data') else None
    }
    return JsonResponse(data, safe=False)

@login_required
def get_athletes_for_coach(request, coach_id):
    coach = Coach.objects.get(id=coach_id)
    athletes = coach.athletes.all()
    data = list(athletes.values())
    return JsonResponse(data, safe=False)

def get_athlete(request, athlete_id):
    try:
        athlete = Athlete.objects.get(id=athlete_id)
        athlete_data = {
            'id': athlete.id,
            'user': athlete.user.username,
            'email': athlete.email,
        }
        return JsonResponse(athlete_data)
    except Athlete.DoesNotExist:
        return JsonResponse({'error': 'Athlete not found'}, status=404)

@require_POST
@login_required
def delete_video(request, athlete_id, video_id):
    try:
        athlete = Athlete.objects.get(id=athlete_id)
        video = VideoStatus.objects.get(id=video_id, athlete=athlete)
        video.delete()
        return JsonResponse({'message': 'Video deleted successfully'})
    except Athlete.DoesNotExist:
        return JsonResponse({'error': 'Athlete not found'}, status=404)
    except VideoStatus.DoesNotExist:
        return JsonResponse({'error': 'Video not found'}, status=404)



@login_required
def get_depth_frames(request, athlete_id, video_id):
    logger.info(f"Depth frames request, video id: {video_id}")

    try:
        video = VideoStatus.objects.get(id=video_id, athlete=athlete_id)
        logger.info(f"Video: {video}")
        
        processed_dir = os.path.dirname(video.processed_path)
        processed_filename = os.path.basename(video.processed_path)
        logger.info(f"Processed dir: {processed_dir}")
        logger.info(f"Processed filename: {processed_filename}")

        base_filename = processed_filename.replace('_processed.mp4', '')
        
        depth_frames = []
        i = 0
        while True:
            depth_frame_path = os.path.join(processed_dir, f"{base_filename}_depth_{i}.png")
            logger.info(f"Looking for depth frame: {depth_frame_path}")
            if os.path.exists(depth_frame_path):
                relative_path = os.path.relpath(depth_frame_path, settings.MEDIA_ROOT)
                depth_frame_url = f"{settings.MEDIA_URL}{relative_path}"
                depth_frames.append({
                    'url': depth_frame_url,
                    'rep': i
                })
                logger.info(f"Found depth frame: {depth_frame_url}")
                i += 1
            else:
                logger.info(f"No more depth frames found after {i} frames")
                break

        if not depth_frames:
            logger.warning("No depth frames found for this video")
            return JsonResponse({'error': 'No depth frames found for this video'}, status=404)

        logger.info(f"Returning {len(depth_frames)} depth frames")
        return JsonResponse({
            'frames': depth_frames
        })
    except VideoStatus.DoesNotExist:
        logger.error(f"Video not found: athlete_id={athlete_id}, video_id={video_id}")
        return JsonResponse({'error': 'Video not found'}, status=404)
    except Exception as e:
        logger.exception(f"Error processing depth frames: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)
    
    
@csrf_exempt
@require_POST
def set_max_depths(request, athlete_id, video_id):
    logger.info(f"Set max depths request, athlete_id: {athlete_id}, video_id: {video_id}")

    try:
        data = json.loads(request.body)
        depths = data.get('depths', [])

        if not depths:
            logger.warning("No depth data provided in the request")
            return JsonResponse({'error': 'No depth data provided'}, status=400)

        video_status = VideoStatus.objects.get(id=video_id, athlete_id=athlete_id)
        set_info = video_status.set_info

        updated_frames = 0
        for depth in depths:
            frame_id = depth.get('frame_id')
            depth_value = depth.get('depth')
            
            if depth_value == 9999:
                logger.info(f"Skipping frame {frame_id} with uncalculated depth 9999")
                continue  # Skip frames with depth 9999 (uncalculated)

            if frame_id is None or depth_value is None:
                logger.warning(f"Skipping invalid entry: frame_id={frame_id}, depth_value={depth_value}")
                continue  # Skip invalid entries

            # Convert depth from centimeters to meters
            depth_value_meters = depth_value / 100.0

            # Update max_depth
            while len(set_info.max_depth) <= frame_id:
                set_info.max_depth.append(None)  # Extend the list if necessary
            
            try:
                old_max_depth = set_info.max_depth[frame_id]
                set_info.max_depth[frame_id] = depth_value_meters

                # Update depth_over_time
                if old_max_depth is not None and len(set_info.depth_over_time) > frame_id:
                    old_depth_index = set_info.depth_over_time.index(old_max_depth)
                    set_info.depth_over_time[old_depth_index] = depth_value_meters
            except Exception as e:
                logger.error(f"Error updating depth_over_time: {str(e)}")

            updated_frames += 1

        set_info.save()
        logger.info(f"Successfully updated {updated_frames} frame depths")

        return JsonResponse({
            'message': f'Successfully updated {updated_frames} frame depths',
            'updated_frames': updated_frames
        })

    except VideoStatus.DoesNotExist:
        logger.error(f"Video status not found for athlete {athlete_id} and video {video_id}")
        return JsonResponse({'error': f'Video status not found for athlete {athlete_id} and video {video_id}'}, status=404)
    except json.JSONDecodeError:
        logger.error("Invalid JSON in request body")
        return JsonResponse({'error': 'Invalid JSON in request body'}, status=400)
    except Exception as e:
        logger.exception(f"Unexpected error: {str(e)}")
        return JsonResponse({'error': f'Unexpected error: {str(e)}'}, status=500)