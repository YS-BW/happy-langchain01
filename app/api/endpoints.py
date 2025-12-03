from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.chains.analysis import analysis_chain, finnal_chain, translate_chain
from app.models.analysis import AnalysisRequest, AnalysisResponse


router = APIRouter()

@router.post("/translate_and_analysis",response_model=AnalysisResponse)
async def translate_and_analysis(request: AnalysisRequest):

    response_data = await finnal_chain.ainvoke(
        {
            "text": request.text,
            "target_lang": request.target_lang
        }
    )

    return AnalysisResponse(
        **response_data
    )
@router.post("/translate_stream",response_model=AnalysisResponse)
async def translate_stream(request: AnalysisRequest):
    response_stream = translate_chain.astream(
        {
            "text": request.text,
            "target_lang": request.target_lang
        }
    )
    async def stream_generator():
        async for chunk in response_stream:
            yield chunk
    return StreamingResponse(stream_generator(), media_type="text/explain")

