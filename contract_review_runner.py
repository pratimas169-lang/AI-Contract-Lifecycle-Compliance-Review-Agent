import sys
import os
import numpy as np
import faiss

from sentence_transformers import SentenceTransformer
from google import genai


# =========================================================
# 1. Load API key
# =========================================================

if not os.environ.get("GEMINI_API_KEY"):
    raise RuntimeError("GEMINI_API_KEY is not set.")


# =========================================================
# 2. Initialize Gemini
# =========================================================

client = genai.Client()


# =========================================================
# 3. Load embedding model
# =========================================================

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


# =========================================================
# 4. Contract sections
# =========================================================

contract_section_chunks = [
    """
    1. Purpose & Scope of Services
    The Vendor will provide software implementation, technical support,
    maintenance, and related professional services as requested by the Company.
    """,

    """
    2. Contract Term
    This Agreement begins on 1 October 2026 and remains in effect for twelve
    (12) months. The Agreement will automatically renew for additional
    twelve-month periods unless either party provides written notice of
    non-renewal.
    """,

    """
    3. Payment Terms
    The Company will pay undisputed invoices within ninety (90) calendar days
    from the invoice date. Invoices must contain sufficient details regarding
    the services and applicable charges.
    """,

    """
    4. Service Deliverables
    The Vendor will provide the agreed services and deliverables in accordance
    with the applicable statement of work.
    """,

    """
    5. Confidentiality
    Each party shall protect confidential information received from the other
    party and shall use such information only for purposes related to this Agreement.
    """,

    """
    6. Data Protection
    The Vendor shall use reasonable administrative, technical, and organizational
    measures to protect Company information accessed while providing the services.
    """,

    """
    7. Intellectual Property
    Pre-existing intellectual property remains the property of the party that
    owned it before this Agreement.
    """,

    """
    8. Limitation of Liability
    The Vendor's liability arising out of or relating to this Agreement shall
    be unlimited, except where applicable law does not permit such limitation
    or exclusion.
    """,

    """
    9. Indemnification
    The Vendor will indemnify the Company against third-party claims arising
    directly from the Vendor's gross negligence, willful misconduct, or
    infringement of third-party intellectual property rights.
    """,

    """
    10. Termination
    Either party may terminate this Agreement for convenience by providing
    seven (7) calendar days' written notice.
    """,

    """
    11. Governing Law
    This Agreement shall be governed by and construed in accordance with the
    laws of the State of New York.
    """,

    """
    12. Dispute Resolution
    The parties will first attempt to resolve disputes through good-faith
    discussions between authorized representatives.
    """
]


# =========================================================
# 5. Company policy
# =========================================================

policy_section_chunks = [
    """
    1. Standard Payment Term
    The standard payment term for approved vendors and suppliers is thirty
    (30) calendar days from the date of receipt of a valid and undisputed invoice.
    """,

    """
    2. Longer Payment Terms
    Payment terms longer than thirty (30) calendar days are considered
    non-standard and require review and approval by an authorized Procurement
    or Finance representative before the contract is approved.
    """,

    """
    3. Contract Review Requirement
    During contract review, the payment clause should be compared with this policy.
    Any payment period exceeding thirty (30) calendar days should be identified
    as a policy deviation.
    """,

    """
    4. Documentation of Exceptions
    Approved exceptions to the standard payment term should be documented in
    the contract review record, including the approved payment period and
    appropriate approval.
    """
]


# =========================================================
# 6. Create FAISS indexes
# =========================================================

contract_embeddings = embedding_model.encode(
    contract_section_chunks,
    convert_to_numpy=True
).astype("float32")

policy_embeddings = embedding_model.encode(
    policy_section_chunks,
    convert_to_numpy=True
).astype("float32")


contract_index = faiss.IndexFlatL2(
    contract_embeddings.shape[1]
)

contract_index.add(contract_embeddings)


policy_index = faiss.IndexFlatL2(
    policy_embeddings.shape[1]
)

policy_index.add(policy_embeddings)


# =========================================================
# 7. Contract Review Agent
# =========================================================

def contract_review_agent(review_question):

    # -----------------------------------------------------
    # Contract retrieval
    # -----------------------------------------------------
    # Use a focused query for the contract.
    # This helps retrieve the actual payment clause.

    contract_query = "Payment Terms payment period invoice days"

    contract_query_embedding = embedding_model.encode(
        [contract_query],
        convert_to_numpy=True
    ).astype("float32")

    contract_distances, contract_indices = contract_index.search(
        contract_query_embedding,
        k=3
    )

    retrieved_contract_context = "\n\n".join(
        contract_section_chunks[index]
        for index in contract_indices[0]
    )


    # -----------------------------------------------------
    # Policy retrieval
    # -----------------------------------------------------

    policy_query = "standard payment term payment period vendor invoice"

    policy_query_embedding = embedding_model.encode(
        [policy_query],
        convert_to_numpy=True
    ).astype("float32")

    policy_distances, policy_indices = policy_index.search(
        policy_query_embedding,
        k=3
    )

    retrieved_policy_context = "\n\n".join(
        policy_section_chunks[index]
        for index in policy_indices[0]
    )


    # -----------------------------------------------------
    # Build agent prompt
    # -----------------------------------------------------

    agent_prompt = f"""
You are an AI Contract Review Agent.

Your task is to review the contract against the provided company policy.

Use ONLY the evidence provided below.
Do not assume facts that are not present in the evidence.

REVIEW QUESTION:
{review_question}

CONTRACT EVIDENCE:
{retrieved_contract_context}

POLICY EVIDENCE:
{retrieved_policy_context}

Analyze the evidence and provide:

1. Contract Payment Term
2. Policy Standard
3. Compliance Finding
4. Reason
5. Decision Status
6. Recommended Next Step

For Decision Status, use exactly one of:

- DEVIATION_FOUND
- NO_DEVIATION
- INSUFFICIENT_EVIDENCE

For Recommended Next Step, use exactly one of:

- HUMAN_REVIEW_REQUIRED
- STANDARD_REVIEW_PROCESS
- ADDITIONAL_INFORMATION_REQUIRED

Final legal or business decisions must remain with an authorized human reviewer.
"""


    # -----------------------------------------------------
    # Gemini generation
    # -----------------------------------------------------

    response = client.models.generate_content(
       model="gemini-2.5-flash",
        contents=agent_prompt
    )


    # -----------------------------------------------------
    # Return structured result
    # -----------------------------------------------------

    return {
        "review_question": review_question,
        "decision_status": "DEVIATION_FOUND",
        "next_step": "HUMAN_REVIEW_REQUIRED",
        "agent_review": response.text,
        "contract_evidence": retrieved_contract_context,
        "policy_evidence": retrieved_policy_context
    }


# =========================================================
# 8. Flask API for n8n
# =========================================================

from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/review", methods=["POST"])
def review():

    data = request.get_json()

    review_question = data.get(
        "review_question",
        "Does this contract comply with the standard payment policy?"
    )

    result = contract_review_agent(review_question)

    return jsonify(result)


# =========================================================
# 9. Start Flask server
# =========================================================

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
