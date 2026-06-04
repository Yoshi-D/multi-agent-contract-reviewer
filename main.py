from processing.pdf_parser import PDF_Manager
from processing.section_parser import parse_sections
from agents.risk_agent import RiskAgent
from agents.qa_agent import QAAgent
from vector_db.vector_store import ContractVectorStore

GEMINI_API_KEY = "f4ke_4pi_k3y"

def main():

    pdf_path = "sample_contracts/vendor_contract.pdf"
    pdf_manager = PDF_Manager()

    print("Extracting PDF...")
    pages = pdf_manager.extract_markdown(pdf_path)

    print(f"Extracted {len(pages)} pages")

    print("Parsing sections...")
    sections = parse_sections(pages)

    print(f"Found {len(sections)} sections")

    vector_store = ContractVectorStore()
    vector_store.clear()
    vector_store.add_sections(sections)

    for section in sections:
        print(
            f"Section {section['section_number']}: "
            f"{section['title']} "
            f"(Page {section['start_page']})"
        )

    api_key = GEMINI_API_KEY

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY environment variable not found"
        )

    risk_agent = RiskAgent(api_key)

    print("\nRunning risk analysis...\n")

    all_risks = []

    for section in sections:

        print(
            f"Analyzing Section "
            f"{section['section_number']} - "
            f"{section['title']}"
        )
        if len(section["content"])<200:
            print(f"Skipping {section['title']} because it is lesser than 200 characters.")
            continue

        result = risk_agent.analyze_section(section)

        all_risks.append({
            "section_number": section["section_number"],
            "title": section["title"],
            "page": section["start_page"],
            "analysis": result
        })

    pdf_manager.save_markdown_report(all_risks)

    qa_agent = QAAgent(api_key, vector_store)

    while True:
        question = input("Enter your query or exit: ")
        if question=="exit":
            break
        else:
            answer = qa_agent.answer(question)
            print(answer)


if __name__ == "__main__":
    main()