"""Compare FinTrust customer selfie and identity-document images."""

from __future__ import annotations

from typing import Any


def kyc_verify(
    rekognition_client: Any,
    selfie_bucket: str,
    selfie_key: str,
    id_bucket: str,
    id_key: str,
    threshold: float = 95.0,
) -> dict[str, Any]:
    response = rekognition_client.compare_faces(
        SourceImage={"S3Object": {"Bucket": selfie_bucket, "Name": selfie_key}},
        TargetImage={"S3Object": {"Bucket": id_bucket, "Name": id_key}},
        SimilarityThreshold=threshold,
    )
    matches = response.get("FaceMatches", [])
    if not matches:
        return {
            "match": False,
            "similarity": 0.0,
            "decision": "REJECT",
            "reason": "No face match met the review threshold",
        }

    similarity = max(float(match["Similarity"]) for match in matches)
    decision = "APPROVE" if similarity >= threshold else "MANUAL_REVIEW"
    return {
        "match": True,
        "similarity": round(similarity, 2),
        "decision": decision,
        "reason": f"Face similarity {similarity:.1f}% with a {threshold:.1f}% threshold",
    }
