import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def summarize_view(request):
    if request.method == "POST":
        body = json.loads(request.body)
        user_input = body.get("text", "")
        lambda_url = "https://lyxy0cdb39.execute-api.ap-northeast-2.amazonaws.com/summarizer_lambda" # 실제 Lambda API Gateway 주소로 교체
        
        try:
            response = requests.post(
                lambda_url,
                json={"text": user_input},
                headers={"Content-Type": "application/json"}
            )
            result = response.json()
            return JsonResponse({"summary": result.get("summary", "")})
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "POST only"}, status=405)