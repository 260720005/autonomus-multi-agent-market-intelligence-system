from backend.models.report import ReportResult
# chr(10) ka matlab newline: 
def report_to_document(report: ReportResult) -> str:
    """
    Convert the final ReportResult into a clean text document
    that can be later chunked, embedded and stored in a vector database.

    """
    document = f"""
Title: {
    report.title
}

Executive Summary: {
    report.executive_summary
}


Market Analysis: { 
    chr(10).join("-" + item for item in report.market_analysis) 
}

Competitive Landscape:{
    chr(10).join("- " + item for item in report.competitive_landscape)
}

Trend Analysis:{
    chr(10).join("- " + item for item in report.trend_analysis)
}

Growth Drivers:{
    chr(10).join("- " + item for item in report.growth_drivers)
}

Risks:{
    chr(10).join("- " + item for item in report.risks)
}

Opportunities:{
    chr(10).join("- " + item for item in report.opportunities)
}

Strategic Outlook:
{report.strategic_outlook}
"""
    return document.strip() # Strip removes extra spaces
