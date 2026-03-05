import requests
import json

# 测试去水印API
def test_watermark_removal_api():
    # API基础URL
    base_url = "http://localhost:8001/api/v1/multimedia"
    
    # 测试数据 - 使用一个示例图像URL
    # 注意：在实际测试中，你需要一个有效的图像URL
    test_data = {
        "image_url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==",  # 一个最小的透明PNG
        "technique": "auto"
    }
    
    print("正在测试去水印API...")
    
    try:
        response = requests.post(
            f"{base_url}/remove-watermark",
            headers={"Content-Type": "application/json"},
            data=json.dumps(test_data)
        )
        
        if response.status_code == 200:
            result = response.json()
            print("API测试成功!")
            print(f"状态: {result.get('status')}")
            print(f"任务ID: {result.get('job_id')}")
            print(f"处理时间: {result.get('processing_time')}秒")
            print(f"技术: {result.get('technique_used')}")
            
            # 检查是否返回了结果图像
            if result.get('result_image'):
                print("✓ 成功返回处理后的图像")
            else:
                print("⚠ 未返回处理后的图像")
                
        else:
            print(f"API请求失败，状态码: {response.status_code}")
            print(f"响应: {response.text}")
            
    except Exception as e:
        print(f"测试过程中发生错误: {str(e)}")

if __name__ == "__main__":
    test_watermark_removal_api()