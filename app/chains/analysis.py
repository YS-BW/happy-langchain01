from functools import partial
from glob import translate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser,PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_deepseek import ChatDeepSeek
from langchain_core.runnables import RunnablePassthrough,RunnableParallel
from app.models.analysis import SentimentAnalysisOutput
import os
dotenv_file = ".env"
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL_NAME", "qwen2.5:1.5b") # 附带默认值
OLLAMA_TEMP = float(os.environ.get("OLLAMA_TEMPERATURE", 0.7))
OLLAMA_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
# Model
sentiment_model = ChatOllama(
    model=OLLAMA_MODEL,
    temperature=OLLAMA_TEMP,
    format = "json",
    base_url=OLLAMA_URL
)
translate_model = ChatOllama(
    model=OLLAMA_MODEL,
    temperature=OLLAMA_TEMP,
    base_url=OLLAMA_URL
)


# Parser
str_parser = StrOutputParser()
analysis_parser = PydanticOutputParser(pydantic_object=SentimentAnalysisOutput)
# Prompt
translate_prompt = """
将以下文本翻译成 {target_lang}。仅返回翻译后的文本，不要添加其他说明或注释。文本: {text}
"""
translate_prompt = ChatPromptTemplate.from_template(translate_prompt)

analysis_prompt_template = """
你是一名专业的情感分析师。分析以下文本的情感倾向并简短总结。

文本: {translated_text}

---
请严格遵循以下 JSON 格式指令输出结果：
{format_instructions} 
---
"""
# 重新赋值给 analysis_prompt 变量 (注意这里使用了 analysis_prompt_template)
analysis_prompt = ChatPromptTemplate.from_template(
    analysis_prompt_template,
    partial_variables={"format_instructions": analysis_parser.get_format_instructions()}
)
# Chain
translate_chain = translate_prompt | translate_model | str_parser
analysis_chain = (analysis_prompt 
                  | sentiment_model.with_retry(stop_after_attempt=3) 
                  | analysis_parser)

# 并行运行
finnal_chain = (
    (RunnablePassthrough.assign(translated_text=translate_chain))
    |(RunnablePassthrough.assign(sentiment=analysis_chain.with_config(run_name="sentiment")))
    |(RunnableParallel(
        original_text = lambda x: x["text"],
        translated_text = lambda x: x["translated_text"],
        sentiment = lambda x: x["sentiment"].json(),
    ))
)

