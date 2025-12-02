from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_deepseek import ChatDeepSeek
import dotenv
dotenv.load_dotenv()
# Model
model = ChatOllama(
    model="qwen2.5:1.5b",
    temperature=0.7,
)
# model = ChatDeepSeek(
#     model="deepseek-chat",
#     temperature=0.7,
# )

# Parser
parser = StrOutputParser()

# Prompt
translate_prompt = """
将以下文本翻译成 {target_lang}。仅返回翻译后的文本，不要添加其他说明或注释。文本: {text}
"""
translate_prompt = ChatPromptTemplate.from_template(translate_prompt)

analysis_prompt = """
你是一名专业的情感分析师。分析以下文本的情感倾向并简短总结。文本: {translated_text}
"""
analysis_prompt = ChatPromptTemplate.from_template(analysis_prompt)

# Chain
translate_chain = translate_prompt | model | parser
analysis_chain = analysis_prompt | model | parser

# 控制内容导入
__all__ = ["translate_chain", "analysis_chain"]
