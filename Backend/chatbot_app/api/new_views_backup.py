from django.shortcuts import render, redirect
from .inferenceBart3 import ask_question
from django.http import JsonResponse
import os
from .inferenceYolo import run_inference

from datetime import datetime
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def ClearChathistory(request):
    request.session.clear()
    return redirect('chatbot')


import os
from datetime import datetime
from django.shortcuts import render, redirect
import whisper
import torchaudio
from django.http import HttpResponse

# Set the backend for torchaudio (try using 'soundfile' instead of 'sox_io')
try:
    torchaudio.set_audio_backend("soundfile")  # Switch to 'soundfile' backend
except Exception as e:
    print(f"Error setting torchaudio backend: {e}")

# Load the Whisper model
model_name = "base"  # Use the model that fits your needs (tiny, base, small, etc.)
model = whisper.load_model(model_name)


def preprocess_and_resample_audio(input_path, output_path, target_sr=16000):

    print(torchaudio.info(input_path))
    input_path = os.path.normpath(input_path)
    output_path = os.path.normpath(output_path)
    
    # Load the audio file
    print("Reached Here")
    print(f"Loading audio from: {input_path}")

    # Set the backend explicitly to 'sox_io'
    torchaudio.set_audio_backend("sox_io")
        
    # Check if the backend was set properly
    print(f"Backend set to: {torchaudio.get_audio_backend()}")
    
    waveform, sr = torchaudio.load(input_path)

    # Resample if necessary
    if sr != target_sr:
        print(f"Resampling audio from {sr} Hz to {target_sr} Hz...")
        resampler = torchaudio.transforms.Resample(orig_freq=sr, new_freq=target_sr)
        waveform = resampler(waveform)
    else:
        print("No resampling needed.")

    # Save the resampled audio for later use
    os.makedirs(os.path.dirname(output_path), exist_ok=True)  # Ensure the output directory exists
    torchaudio.save(output_path, waveform, target_sr)
    
    print(f"Resampled audio saved to: {output_path}")
    return output_path



def transcribe_audio(audio_path, custom_context=""):
    try:
        # Check if the file exists
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        print(f"Transcribing audio from: {audio_path}")
        result = model.transcribe(audio_path, initial_prompt=custom_context)
        return result["text"]
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return "Error during transcription"



def chatbot_view(request):
    chat_history = request.session.get('chat_history', [])
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    result_url = request.session.get('result_url')
    detected_objects = request.session.get('detected_objects', [])
    
    if request.method == "POST":
        question = request.POST.get("question")

        if question:
            chat_history.append({"role": "user", "content": question, "timestamp": timestamp})
            
            # Use the detected objects to answer questions related to those objects
            if detected_objects:
                object_name = detected_objects[0]['label']  # Use first detected object as the object name

                try:
                    if any(phrase in question.lower() for phrase in ["thanks", "thank you", "thanks a lot", "thank you so much", "thanks for all your efforts"]):
                        answer = f"You are welcome 😊. Feel free to ask more about {object_name}."
                        
                        chat_history.append({"role": "bot", "content": answer, "timestamp":timestamp})
                    else:    
                        object_name = detected_objects[0]['label']  # Use first detected object as the object name
                        answer = ask_question(question, object_name)  # If object_name matches, use it in the question
                        chat_history.append({"role": "bot", "content": answer, "timestamp":timestamp})
                except Exception as e:
                    error_message = f"An error occurred: {e}"
                    chat_history.append({"role": "bot", "content": error_message})

            else:
                # If no objects are detected, provide a generic response
                answer = "No objects detected to inquire about. Please upload an image"
                chat_history.append({"role": "bot", "content": answer, "timestamp":timestamp})


        # Handle audio file upload and transcription
        if request.FILES.get('audio'):
            audio_file = request.FILES['audio']

            # Check if the uploaded file is a .wav file
            if not audio_file.name.endswith('.wav'):
                return HttpResponse("Error: Only .wav files are allowed.", status=400)

            # Create the correct file path using os.path.join
            audio_file_path = os.path.join('media', 'uploads', audio_file.name)

            # Define output path for resampled audio
            resampled_audio_path = os.path.join('media', 'uploads', 'resampled_' + audio_file.name)
            
            # Ensure the directory exists
            os.makedirs(os.path.dirname(audio_file_path), exist_ok=True)

            # Save the uploaded .wav audio file
            try:
                with open(audio_file_path, 'wb') as f:
                    for chunk in audio_file.chunks():
                        f.write(chunk)
                print(f"Saved audio file to: {audio_file_path}")
            except Exception as e:
                print(f"Error saving audio file: {e}")
                return HttpResponse("Error saving audio file.", status=500)
            
            # Preprocess and resample audio
            resampled_audio_path = preprocess_and_resample_audio(audio_file_path, resampled_audio_path)
            
            if not resampled_audio_path:
                return HttpResponse("Error processing audioooooo.", status=500)

            # Transcribe the audio file with optional custom vocabulary
            custom_context = "Yali, Garuda, Akhi Jhyal, Prayer Wheel"

            # Now call the transcribe_audio function with the absolute path
            transcription = transcribe_audio(resampled_audio_path, custom_context)

            # Process transcription to form a question
            if transcription.strip().endswith("?"):
                question = transcription  

            # Append the transcription to chat history
            chat_history.append({"role": "user", "content": transcription, "timestamp": timestamp})

            # Use the detected objects to answer questions related to those objects
            if detected_objects:
                object_name = detected_objects[0]['label']  # Use first detected object as the object name

                try:
                    if any(phrase in question.lower() for phrase in ["thanks", "thank you", "thanks a lot", "thank you so much", "thanks for all your efforts"]):
                        answer = f"You are welcome 😊. Feel free to ask more about {object_name}."
                        
                        chat_history.append({"role": "bot", "content": answer, "timestamp":timestamp})
                    else:    
                        object_name = detected_objects[0]['label']  # Use first detected object as the object name
                        answer = ask_question(question, object_name)  # If object_name matches, use it in the question
                        chat_history.append({"role": "bot", "content": answer, "timestamp":timestamp})
                except Exception as e:
                    error_message = f"An error occurred: {e}"
                    chat_history.append({"role": "bot", "content": error_message})

            else:
                # If no objects are detected, provide a generic response
                answer = "No objects detected to inquire about. Please upload an image"
                chat_history.append({"role": "bot", "content": answer, "timestamp":timestamp})

        # Save chat history in session
        request.session['chat_history'] = chat_history

    return render(request, "chatbot_app/chat.html", {
        "chat_history": chat_history
    })





def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        # Save uploaded image
        uploaded_file = request.FILES['image']
        upload_dir = os.path.join('media/uploads')
        os.makedirs(upload_dir, exist_ok=True)
        upload_path = os.path.join(upload_dir, uploaded_file.name)

        with open(upload_path, 'wb') as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)

        # Perform YOLO inference
        result_dir = os.path.join('media/results')
        result_image_path, detected_objects = run_inference(upload_path, result_dir)

        # Prepare URL and objects
        result_url = f"/media/results/{os.path.basename(result_image_path)}"
        detected_objects_list = [obj['label'] for obj in detected_objects]

        # Append image result to chat history
        chat_history = request.session.get('chat_history', [])
        chat_history.append({
            "role": "user",
            "content": f'<img src="{upload_path}" alt="Uploaded Image" style="max-width: 150px; height: auto;"><br>',
            "timestamp":timestamp
        })

        # Check if detected_objects_list is empty
        if detected_objects_list:
            # Append detected objects and image URL if objects are found
            first_detected_object = detected_objects_list[0]

            chat_history.append({
                "role": "bot",
                "content": (
                    f"Detected objects: <strong>{first_detected_object}</strong><br>"
                    f"You can ask questions related to: {first_detected_object}<br>"
                    f'<img src="{result_url}" alt="YOLO Result" style="max-width: 150px; height: auto;"><br>'
                ), "timestamp":timestamp
            })
        else:
            # Append a message when no objects are detected
            chat_history.append({
                "role": "bot",
                "content": (
                    "No objects detected in the image.<br>"
                ), "timestamp":timestamp
            })
            

        # Save updated chat history and result data in session
        request.session['chat_history'] = chat_history
        request.session['result_url'] = result_url
        request.session['detected_objects'] = detected_objects
        # request.session.clear()

    return redirect('chatbot')  # Redirect back to the chat view






'''
def chatbot_view(request):
    chat_history = request.session.get('chat_history', [])
    if request.method == "POST":
        question = request.POST.get("question")
        object_name = request.POST.get("object_name", "")
        if question:
            chat_history.append({"role": "user", "content": question})
            try:
                answer = ask_question(question, object_name)
                chat_history.append({"role": "bot", "content": answer})
            except Exception as e:
                answer = f"An error occurred: {e}"
                chat_history.append({"role": "bot", "content": answer})
            request.session['chat_history'] = chat_history
    return render(request, "chatbot_app/chat.html", {"chat_history": chat_history})
    # return JsonResponse({"chat_history": chat_history})



#------------------------------------------------------------------------------------------
def upload_image(request):
    result_url = None
    detected_objects = []

    if request.method == 'POST' and request.FILES['image']:
        # Save uploaded image
        uploaded_file = request.FILES['image']
        upload_dir = os.path.join('media/uploads')
        os.makedirs(upload_dir, exist_ok=True)
        upload_path = os.path.join(upload_dir, uploaded_file.name)

        with open(upload_path, 'wb') as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)

        # Perform YOLO inference
        result_dir = os.path.join('media/results')
        result_image_path, detected_objects = run_inference(upload_path, result_dir)

        # Get the URL for the result
        result_url = f"/media/results/{os.path.basename(result_image_path)}"

    return render(request, 'chatbot_app/chat.html', {
        'result_url': result_url,
        'detected_objects': detected_objects
    })
'''















