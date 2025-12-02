from pydantic import BaseModel, Field

# 请求数据模型
class AnalysisRequest(BaseModel):
    """"用于接收客户端而请求的数据模型"""
    text: str = Field(..., description="待分析的文本")
    target_lang: str=  Field("zh-CN", description="目标语言")

# 响应数据模型
class AnalysisResponse(BaseModel):
    """用于返回给客户端的数据模型"""
    orignal_text: str = Field(..., description="原始文本")
    translated_text: str = Field(..., description="翻译后语言")
    sentiment: str = Field(..., description="情感")
    
    