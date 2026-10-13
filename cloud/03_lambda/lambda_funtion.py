import json

def lambda_handler(event, context):
    try:
    
        # 콘솔 테스트용: dict 바로 받는 경우
        if "body" not in event:
            name = event.get("name", "World")
        else:
            # API Gateway 요청일 경우
            body = json.loads(event.get("body", "{}"))
            name = body.get("name", "World")
        
        return {
            "statusCode": 200,
            "headers": {
            "Content-Type": "application/json"
            },
            "body": json.dumps({"message": f"Hello, {name}! ZIP으로 압축해서 Lambda 사용!"}, ensure_ascii=False)
        }
    
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}, ensure_ascii=False)
        }