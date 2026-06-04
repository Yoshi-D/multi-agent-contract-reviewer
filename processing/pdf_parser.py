import pymupdf4llm

class PDF_Manager():
    def extract_markdown(self,pdf_path):
        return pymupdf4llm.to_markdown(pdf_path,page_chunks = True)
    def save_markdown_report(self, all_risks, output_file="../risk_report.md"):
        lines = []

        lines.append("# Contract Risk Report\n")

        for section in all_risks:

            lines.append(
                f"## {section['title']}"
            )

            analysis = section["analysis"]

            overall_risk = analysis.get('risk_level')

            lines.append(
                f"**Overall Risk:** {overall_risk}\n"
            )

            risks = analysis.get("risks", [])

            if not risks:
                lines.append(
                    "_No significant risks detected._\n"
                )

            for idx, risk in enumerate(risks, start=1):
                lines.append(
                    f"### Risk {idx}: {risk.get('risk_type', 'Unknown')}"
                )

                lines.append(
                    f"- **Severity:** {risk.get('severity', 'Unknown')}"
                )

                lines.append(
                    f"- **Explanation:** {risk.get('explanation', '')}"
                )

                lines.append("")


            lines.append("---\n")

        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        print(f"Saved markdown report to {output_file}")
        return

