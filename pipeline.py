"""
Arav Jaiman

This program will be a pipeline to extract structured data
from health insurance policies.

Link -> LLM -> JSON -> Excel
"""
from langchain_core.prompts import ChatPromptTemplate
from enum import Enum
from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from openpyxl import load_workbook

load_dotenv()

class LLMProvider(Enum):
    GOOGLE = 1
    OPENAI = 2
    ANTHROPIC = 3

class PolicyAnalysis(BaseModel):
    """Health Insurance Policy Analysis"""

    payer_name: str = Field(
        description="The name of the payer or insurance provider responsible for the policy."
    )
    policy_name: str = Field(
        description="The official title or name of the insurance policy."
    )
    policy_type: str = Field(
        description="The category or classification of the policy (e.g., medical, dental, vision)."
    )
    latest_approval_date: str = Field(
        description="The most recent date the policy was formally approved."
    )
    latest_effective_date: str = Field(
        description="The date when the most recent changes to the policy became effective."
    )
    brief_summary: str = Field(
        description="A concise two-sentence summary of the policy."
    )
    number_of_covered_hcpcs_codes: int = Field(
        description="The total number of HCPCS (Healthcare Common Procedure Coding System) codes covered by the policy. If none explicitly listed, the number inferred from context."
    )
    number_of_noncovered_hcpcs_codes: int = Field(
        description="The total number of HCPCS codes explicitly not covered by the policy."
    )
    modifiers_used: list[str] = Field(
        description="A list of HCPCS or CPT modifiers mentioned in the policy. Assume modifiers are covered unless explicitly excluded."
    )
    service_summary: str = Field(
        description="A two-sentence overview of the services addressed in the policy."
    )
    reimbursement_detail: str = Field(
        description="A two-sentence explanation of how reimbursement is handled under the policy."
    )
    non_reimbursement_detail: str = Field(
        description="A two-sentence explanation of services or cases where reimbursement is not provided."
    )
    notes: str = Field(
        description="Additional two-sentence notes that provide any clarifications or important context about the policy."
    )


class PolicyPipeline:

    systemPrompt = """
        You are a Health Insurance Policy Analyst AI specializing in
        searching policy documentation for specific information and
        you follow all instructions perfectly.
        You will perform a complete policy analysis on the policy
        document that is provided to you as a link.
        """

    promptTemplate = ChatPromptTemplate(
        [("system", systemPrompt), ("user", "{link}")]
    )

    def __init__(self, provider: LLMProvider, workbook, sheetname):
        self.provider = provider
        self.model = self.setModel()
        self.workbookName = workbook
        self.workbook = load_workbook(workbook)
        self.worksheet = self.workbook[sheetname]

    def runPipeline(self, link):
        prompt = self.promptTemplate.invoke({"link": link})
        analysis = self.model.invoke(prompt)
        dataDict = analysis.dict()
        modifiers = ""
        for modifier in dataDict['modifiers_used']:
            modifiers = modifiers + modifier + ","
        modifiers = modifiers[:-1]
        dataDict['modifiers_used'] = modifiers
        self.worksheet.append(list(dataDict.values()))
        self.workbook.save(self.workbookName)

    def setProvider(self, newProvider: LLMProvider):
        self.provider = newProvider
        self.model = self.setModel()

    def setModel(self):
        if self.provider == LLMProvider.GOOGLE:
            model = init_chat_model("gemini-2.0-flash", model_provider="google_genai")
        elif self.provider == LLMProvider.ANTHROPIC:
            model = init_chat_model("claude-2-5-sonnet-latest", model_provider="anthropic")
        else:
            model = init_chat-model("gpt-4o-mini", model_provider="openai")

        return model.with_structured_output(PolicyAnalysis)
