import memory

if __name__ == "__main__":
    memory.init_db()

    from agents.classifier.classifier_agent import ClassifierAgent
    from agents.email.email_agent import EmailAgent
    from agents.json.json_agent import JSONAgent
    from agents.pdf.pdf_agent import PDFAgent

    classifier = ClassifierAgent()
    email_agent = EmailAgent()
    json_agent = JSONAgent()
    pdf_agent = PDFAgent()

    # Test Email file
    filepath_email = "inputs/sample_email.txt"
    entry_id_email, filetype_email = classifier.process(filepath_email)
    if filetype_email == "Email":
        email_agent.process(entry_id_email)

    # Test JSON file
    filepath_json = "inputs/sample_invoice.json"
    entry_id_json, filetype_json = classifier.process(filepath_json)
    if filetype_json == "JSON":
        json_agent.process(entry_id_json)

    # Test PDF file
    filepath_pdf = "inputs/sample_document.pdf"
    entry_id_pdf, filetype_pdf = classifier.process(filepath_pdf)
    if filetype_pdf == "PDF":
        pdf_agent.process(entry_id_pdf)
