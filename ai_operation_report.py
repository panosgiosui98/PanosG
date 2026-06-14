import os
from anthropic import Anthropic

def generate_ai_report(input_data):
    # 1. Έλεγχος αν υπάρχει το API Key στο περιβάλλον
    if not os.environ.get("ANTHROPIC_API_KEY"):
        return "Σφάλμα: Δεν βρέθηκε το ANTHROPIC_API_KEY στο περιβάλλον σου."

    # 2. Αρχικοποίηση του Anthropic Client
    client = Anthropic()

    # 3. Ορισμός του System Prompt (ο ρόλος του Claude)
    system_instruction = (
        "Είσαι ένας έμπειρος Data Analyst και Operations Manager. "
        "Ανάλυσε τα δεδομένα που θα σου δώσει ο χρήστης, εντόπισε τα 3 σημαντικότερα προβλήματα/bottlenecks "
        "και πρότεινε πρακτικές, actionable λύσεις. "
        "Η απάντησή σου πρέπει να είναι στα Ελληνικά, σύντομη, με bullet points και strict business ύφος."
    )

    print("📡 Αποστολή δεδομένων στο Claude API...")

    try:
        # 4. Κλήση του API (Χρησιμοποιούμε το Claude Sonnet 4.6)
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1000,
            temperature=0.3,  # Χαμηλό temperature για πιο σοβαρές/σταθερές απαντήσεις
            system=system_instruction,
            messages=[
                {"role": "user", "content": f"Ορίστε τα δεδομένα για ανάλυση:\n\n{input_data}"}
            ]
        )

        # Επιστροφή του κειμένου που παρήγαγε το Claude
        return message.content[0].text

    except Exception as e:
        return f"Προέκυψε σφάλμα κατά την κλήση του API: {e}"

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    # Παράδειγμα δεδομένων (π.χ. logs από καθυστερήσεις/παράπονα σε μια αποθήκη ή project)
    sample_data = """
    - 08:30: Το φορτηγό Α άργησε 45 λεπτά να ξεφορτώσει λόγω έλλειψης χώρου στη ράμπα.
    - 11:00: Ο Kostas έχασε 20 λεπτά ψάχνοντας τα σωστά barcodes για τα προϊόντα Χ.
    - 14:00: Παραλαβή 50 κιβωτίων χωρίς συνοδευτικό τιμολόγιο, κολλήσαμε στη γραφειοκρατία.
    - 15:30: Το σύστημα inventory έκανε update και έπεσε για 15 λεπτά.
    """

    # Τρέχουμε την ανάλυση
    report = generate_ai_report(sample_data)

    # Αποθήκευση του Report σε αρχείο
    output_filename = "ai_operation_report.md"
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"✅ Το report δημιουργήθηκε με επιτυχία και αποθηκεύτηκε στο: {output_filename}")
