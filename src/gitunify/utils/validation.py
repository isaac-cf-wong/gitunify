"""Utility functions for validation and error logging."""

from __future__ import annotations

import logging

from pydantic import BaseModel, ValidationError

logger = logging.getLogger("gitunify")


def log_validation_errors(error: ValidationError, parameters: type[BaseModel]) -> None:
    """Log detailed validation errors with supported parameters."""
    logger.error("Parameter validation failed for %s:", parameters.__name__)

    # Get list of supported parameters
    supported_params = set(parameters.model_fields.keys())
    received_params = set()
    forbidden_params = set()

    for err in error.errors():
        field = err.get("loc", ("unknown",))[0]
        error_type = err.get("type", "unknown")

        if error_type == "extra_forbidden":
            forbidden_params.add(field)
            received_params.add(field)
        else:
            received_params.add(field)

    if forbidden_params:
        logger.error("  Forbidden parameters: %s", ", ".join(forbidden_params))
        logger.error("  Supported parameters: %s", ", ".join(sorted(supported_params)))

    # Log other errors
    for err in error.errors():
        field = err.get("loc", ("unknown",))[0]
        if field not in forbidden_params:
            error_type = err.get("type", "unknown")
            message = err.get("msg", "Unknown error")
            logger.error("  ❌ %s: %s (type: %s)", field, message, error_type)
