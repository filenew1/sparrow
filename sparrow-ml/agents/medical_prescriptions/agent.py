from typing import Dict, List, Any
from prefect import flow, task
import base64
import json
from .sparrow_client import SparrowClient
from rich import print


@task(name="detect_doc_structure")
async def detect_doc_structure(input_data: Dict, sparrow_client: SparrowClient) -> Dict:
    """
    Extracts each page type from a document using Sparrow API
    """

    if 'content' not in input_data:
        raise ValueError("Document data is required")

    results = await sparrow_client.extract_type_per_page_sparrow(input_data)

    return results


@task(name="split_document")
async def split_document(document_data: str) -> List[bytes]:
    """
    Splits a base64 encoded document into pages
    """
    # Decode base64 document
    document_bytes = base64.b64decode(document_data)

    # Implementation depends on your document format
    # For example, if it's PDF:
    # from pdf2image import convert_from_bytes
    # pages = convert_from_bytes(document_bytes)

    # Placeholder implementation
    return [document_bytes]  # Return as single page for now


@task(name="extract_data")
async def extract_data(page: bytes, params: Dict, sparrow_client: SparrowClient) -> Dict:
    """
    Extracts data from a page using Sparrow API
    """
    results = {}

    # if params.get('extract_tables', True):
    #     results['table_data'] = await sparrow_client.extract_table(page)
    #
    # if params.get('extract_forms', True):
    #     results['form_data'] = await sparrow_client.extract_form(page)

    return results


class MedicalPrescriptionsAgent:
    """
    Agent for processing medical prescriptions using Sparrow API.
    """

    def __init__(self):
        self.name = "medical_prescriptions"
        self.capabilities = {"document_analysis", "data_extraction"}
        self.sparrow_client = SparrowClient()

    @flow(name="medical_prescriptions_flow")
    async def execute(self, input_data: Dict) -> Dict:
        """
        Main document processing flow
        """
        # Process and validate input
        doc_structure = await detect_doc_structure(input_data, self.sparrow_client)

        # # Split document into pages
        # pages = await split_document(processed_input['document'])
        #
        # # Process each page
        # results = []
        # for page_num, page in enumerate(pages, 1):
        #     page_result = await extract_data(
        #         page,
        #         processed_input,
        #         self.sparrow_client
        #     )
        #
        #     results.append({
        #         'page_number': page_num,
        #         'extractions': page_result
        #     })

        return {
            'filename': input_data['filename'],
            'total_pages': 1,
            'results': doc_structure
        }