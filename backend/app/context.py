#
# context.py
#
# @author n1ghts4kura
#

from agents import function_tool

import typedef

current_stage = 1 # 1: 大纲生成，2: 用户自述+系统评分与反馈，3: 学习完成
current_retell_count = 0 # 当前复述轮次
knowledge_domain: str = "" # 当前学习的知识领域
knowledge_outline: typedef.OutlineAgentOutput | None = None # 知识大纲
evaluating_rounds: list[typedef.EvaluatorAgentOutput] = [] # 评分结果列表

@function_tool
def get_current_stage() -> int:
    """获取当前学习阶段"""
    global current_stage
    return current_stage

@function_tool
def set_current_stage(stage: int):
    """
    设置当前学习阶段
    1: 大纲生成
    2: 用户自述+系统评分与反馈
    3: 学习完成
    """
    global current_stage
    current_stage = stage

@function_tool
def get_current_retell_count() -> int:
    """获取当前复述轮次"""
    global current_retell_count
    return current_retell_count

@function_tool
def increase_current_retell_count():
    """增加当前复述轮次"""
    global current_retell_count
    current_retell_count += 1

@function_tool
def get_knowledge_domain() -> str:
    """获取当前知识领域"""
    global knowledge_domain
    return knowledge_domain

# @function_tool
def set_knowledge_domain(domain: str):
    """设置当前知识领域"""
    global knowledge_domain
    knowledge_domain = domain

@function_tool
def get_knowledge_outline() -> typedef.OutlineAgentOutput | None:
    """获取当前知识大纲"""
    global knowledge_outline
    return knowledge_outline

# @function_tool
def set_knowledge_outline(outline: typedef.OutlineAgentOutput):
    """设置当前知识大纲"""
    global knowledge_outline
    knowledge_outline = outline

@function_tool
def get_evaluating_rounds() -> list[typedef.EvaluatorAgentOutput]:
    """获取评分结果列表"""
    global evaluating_rounds
    return evaluating_rounds

@function_tool
def add_evaluating_round(evaluation: typedef.EvaluatorAgentOutput):
    """添加评分结果"""
    global evaluating_rounds
    evaluating_rounds.append(evaluation)

__all__ = [
    "get_current_stage",
    "set_current_stage",
    "get_knowledge_outline",
    "set_knowledge_outline"
]