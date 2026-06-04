import re

def parse_sections(pages):
    heading_pattern = re.compile(
        r"^(\d+)\.\s+([A-Z][A-Z\s,\-&]+)$"
    )

    sections = []
    current_section = None

    for page in pages:
        page_num = page["metadata"]["page"]

        lines = page["text"].splitlines()

        for line in lines:
            line = line.strip()

            if not line:
                continue

            match = heading_pattern.match(line)

            if match:
                # Save previous section
                if current_section:
                    current_section["content"] = (
                        current_section["content"].strip()
                    )
                    sections.append(current_section)

                # Start new section
                current_section = {
                    "section_number": match.group(1),
                    "title": match.group(2).strip(),
                    "start_page": page_num,
                    "content": ""
                }

            elif current_section:
                current_section["content"] += line + "\n"

    # Save final section
    if current_section:
        current_section["content"] = (
            current_section["content"].strip()
        )
        sections.append(current_section)

    return sections
