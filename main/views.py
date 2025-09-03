from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password  # if you store hashed passwords
from gradio_client import Client, handle_file
import json

from main.models import User, Items, Refund

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

@csrf_exempt
def handle_login(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  
            username = data.get("username")
            password = data.get("password")
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return JsonResponse({"error": "Invalid username or password", "status": False}, status=401)

            if user.password == password:
                return JsonResponse({"message": "Login successful", "username": user.username, "occupation": user.status, "id": user.id, "status": True})
            else:
                return JsonResponse({"error": "Invalid username or password", "status":False}, status=401)

        except Exception as e:
            return JsonResponse({"error": str(e), "status": False}, status=400)

    return JsonResponse({"error": "Only POST allowed", "status": False}, status=405)   

@csrf_exempt
def get_total(request):
    if request.method == "PATCH":
        try:
            data = json.loads(request.body)  
            id = data.get("id")
            try:
                user = User.objects.get(id=id)
            except User.DoesNotExist:
                return JsonResponse({"error": "Invalid id", "status":False}, status=401)
            return JsonResponse({"total": user.total_refund, "status": True})
        except Exception as e:
            return JsonResponse({"error": str(e), "status": False}, status=400)
    return JsonResponse({"error": "Only POST allowed", "status": False}, status=405)    

@csrf_exempt
def get_all_item(request):
    if request.method == "PATCH":
        try:
            data = json.loads(request.body)  
            id = data.get("merchant_id")

            item = list(Items.objects.filter(merchant_id=id).values())
            return JsonResponse({"items": item, "status": True})
        except Exception as e:
            return JsonResponse({"error": str(e), "status": False}, status=400)
    return JsonResponse({"error": "Only POST allowed", "status": False}, status=405)     

@csrf_exempt
def get_item(request):
    if request.method == "PATCH":
        try:
            data = json.loads(request.body)  
            id = data.get("item_id")

            item = Items.objects.get(id=id)
            item_data = {
                "id": str(item.id),
                "image": item.image,
                "merchant_id": str(item.merchant_id),
                "name": item.name,
                "price": item.price,
            }
            return JsonResponse({"item": item_data, "status": True})
        except Exception as e:
            return JsonResponse({"error": str(e), "status": False}, status=400)
    return JsonResponse({"error": "Only POST allowed", "status": False}, status=405)       

@csrf_exempt
def manage_refund(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  
            main = data.get("main")
            review = data.get("review")
            caption = data.get("caption") 

            merchant_id = data.get("merchant")
            user_id = data.get("user")

            user = User.objects.get(id=user_id)
            merchant = User.objects.get(id=merchant_id) 

            refund = Refund.objects.create(
                main=main,
                review=review,
                caption=caption,
                user=user.username,
                merchant=merchant.username,
                verdict="Pending",
                status=False
            )

            client = Client("cavalierplance/gradio-refund-predicter")
            result = client.predict(
                    image_main=handle_file(main),
                    image_review=handle_file(review),
                    caption=caption,
                    api_name="/predict"
            )

            if "0" in result:
                refund.verdict = "Valid"
            else:
                refund.verdict = "Invalid"
            refund.save()
            return JsonResponse({"result": result, "status": True})
        except Exception as e:
            return JsonResponse({"error": str(e), "status": False}, status=400)
    return JsonResponse({"error": "Only POST allowed", "status": False}, status=405)   

@csrf_exempt
def get_all_refund(request):
    if request.method == "PATCH":
        try:
            data = json.loads(request.body)  
            user_id = data.get("user_id")
            merchant_id = data.get("merchant_id") 

            if merchant_id != None:
                item = list(Refund.objects.filter(merchant=merchant_id).values())
            else:
                item = list(Refund.objects.filter(user=user_id).values())

            return JsonResponse({"refund": item, "status": True})
        except Exception as e:
            return JsonResponse({"error": str(e), "status": False}, status=400)
    return JsonResponse({"error": "Only POST allowed", "status": False}, status=405)       

@csrf_exempt
def get_refund(request):
    if request.method == "PATCH":
        try:
            data = json.loads(request.body)  
            id = data.get("id")

            item = Refund.objects.get(id=id)

            refund = {
                "id": item.id,
                "main_image": item.main,
                "review_image": item.review,
                "caption": item.caption,
                "item_id": item.item_id,
                "status": item.status
            }

            return JsonResponse({"refund": refund, "status": True})
        except Exception as e:
            return JsonResponse({"error": str(e), "status": False}, status=400)
    return JsonResponse({"error": "Only POST allowed", "status": False}, status=405)       

@csrf_exempt
def update_status_refund(request):
    if request.method == "PATCH":
        try:
            data = json.loads(request.body)  
            id = data.get("id")
            verdict = data.get("verdict")

            item = Refund.objects.get(id=id)
            item.verdict = verdict
            item.status = True
            item.save()

            return JsonResponse({"status": True})
        except Exception as e:
            return JsonResponse({"error": str(e), "status": False}, status=400)
    return JsonResponse({"error": "Only POST allowed", "status": False}, status=405)       
