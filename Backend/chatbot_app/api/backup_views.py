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



def chatbot_view(request):
    chat_history = request.session.get('chat_history', [])
    result_url = request.session.get('result_url')
    detected_objects = request.session.get('detected_objects', [])

    if request.method == "POST":
        question = request.POST.get("question")

        if question:
            chat_history.append({"role": "user", "content": question, "timestamp":timestamp})
            
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

            # Update session with new chat history
            request.session['chat_history'] = chat_history

    return render(request, "chatbot_app/chat.html", {
        "chat_history": chat_history,
        "result_url": result_url,
        "detected_objects": detected_objects
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




from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
import os
import torchaudio

def preprocess_and_resample_audio(input_path, output_path, target_sr=16000):
    waveform, sr = torchaudio.load(input_path)
    if sr != target_sr:
        resampler = torchaudio.transforms.Resample(orig_freq=sr, new_freq=target_sr)
        waveform = resampler(waveform)
    torchaudio.save(output_path, waveform, target_sr)
    return output_path

def upload_audio(request):
    if request.method == "POST" and request.FILES.get("audio"):
        audio_file = request.FILES["audio"]
        input_path = os.path.join(settings.MEDIA_ROOT, audio_file.name)
        output_path = os.path.join(settings.MEDIA_ROOT, "processed_" + audio_file.name)

        # Save uploaded audio
        with open(input_path, "wb+") as destination:
            for chunk in audio_file.chunks():
                destination.write(chunk)

        # Preprocess and resample audio
        preprocess_and_resample_audio(input_path, output_path)
        return HttpResponse(f"Audio uploaded and processed: {output_path}")

    return render(request, "upload.html")




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















