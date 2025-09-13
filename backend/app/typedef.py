#
# typedef.py
#
# @author n1ghts4kura
#

from pydantic import BaseModel, Field

class OutlineAgentOutput(BaseModel):
    """FinderAgent的输出模型"""

    class Level(BaseModel):
        """知识点单层模型 嵌套"""

        name: str = Field(..., description="知识点名称")

        description: str = Field("", description="知识点描述")

        sub_levels: list["OutlineAgentOutput.Level"] = Field(
            default_factory=list, description="子知识点列表"
        )

    root_levels: list[Level] = Field(
        default_factory=list, description="根知识点列表"
    )

class EvaluatorAgentOutput(BaseModel):
    """EvaluatorAgent的输出模型"""

    missing_points: list[str] = Field(..., description="遗漏知识点列表")

    understandability_score: float = Field(..., ge=0, le=10, description="可理解性评分，0-10")

    completeness_score: float = Field(..., ge=0, le=10, description="完整性评分，0-10")

    evaluating_comments: str = Field("", description="评分评语")
