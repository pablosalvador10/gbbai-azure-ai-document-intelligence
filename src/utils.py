from typing import Any, Dict


def clean_json_string(json_string: str) -> str:
    """
    Cleans a JSON string by removing unwanted characters.

    :param json_string: The JSON string to be cleaned.
    :return: The cleaned JSON string.
    """
    cleaned_string = (
        json_string.replace("```json\n", "").replace("\n", "").replace("```", "")
    )
    return cleaned_string


def compare_invoices(
    invoice_document_intelligence: Dict[str, Any],
    invoice_gpt4_vision: Dict[str, Any],
    ground_truth: Dict[str, Any],
) -> Dict[str, Dict[str, Any]]:
    """
    Compares key invoice details from two sources against the ground truth.

    :param invoice_document_intelligence: The invoice details extracted by Document Intelligence.
    :param invoice_gpt4_vision: The invoice details extracted by GPT-4 Vision.
    :param ground_truth: The actual invoice details.
    :return: A dictionary with the comparison results.
    """

    keys_to_compare = ["TotalTax", "InvoiceTotal", "InvoiceId", "InvoiceDate"]

    return {
        key: {
            "invoice_document_intelligence": invoice_document_intelligence.get(
                key, {}
            ).get("content"),
            "invoice_gpt4_vision": invoice_gpt4_vision.get(key, {}).get("content"),
            "ground_truth": ground_truth.get(key),
        }
        for key in keys_to_compare
    }
