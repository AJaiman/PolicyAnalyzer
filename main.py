from pipeline import PolicyPipeline, LLMProvider

pipeline = PolicyPipeline(LLMProvider.GOOGLE, "policies.xlsx", "Policy Analysis")
policyLink = "https://www.uhcprovider.com/content/dam/provider/docs/public/policies/comm-medical-drug/ablative-treatment-spinal-pain.pdf"
pipeline.runPipeline(policyLink)
