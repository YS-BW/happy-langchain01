from fastapi import APIRouter

from app.chains.analysis import analysis_chain, translate_chain
from app.models.analysis import AnalysisRequest, AnalysisResponse


router = APIRouter()

@router.post("/translate_and_analysis",response_model=AnalysisResponse)
async def translate_and_analysis(request: AnalysisRequest):
    """
    接收请求,调用LCEL Chain进行翻译和情感分析
    """
    translate_text = await translate_chain.ainvoke(
        {
            "text": request.text,
            "target_lang": request.target_lang
        }
    )
    """
    情感化分析
    """
    sentiment = await analysis_chain.ainvoke(
        {
            "translated_text": translate_text
        }
    )
    return AnalysisResponse(
        orignal_text=request.text,               # 关键字参数 1
        translated_text=translate_text,          # 关键字参数 2
        sentiment=sentiment    # 关键字参数 3
    )