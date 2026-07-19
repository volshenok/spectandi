import os
import requests
from datetime import datetime, timezone
from opentelemetry.sdk.trace.export import SpanExporter, SpanExportResult

class APIExporter(SpanExporter):
    """
    Sends spans to Spectandi's /ingest endpoint over HTTPS, authenticated
    by API key. Replaces ClickHouseExporter, which connected directly to
    the database with shared credentials.
    """

    def __init__(self):
        self.api_url = os.environ.get("SPECTANDI_API_URL", "https://web-production-1baeb.up.railway.app")
        self.api_key = os.environ.get("SPECTANDI_API_KEY", "")
        if not self.api_key:
            print("Warning: SPECTANDI_API_KEY not set. Traces will not be sent.")

    def export(self, spans):
        if not self.api_key:
            return SpanExportResult.FAILURE

        payload_spans = []
        for span in spans:
            attrs = dict(span.attributes or {})

            if span.name not in ("gen_ai.chat", "agent.run",
                                  "agent.step1.understand",
                                  "agent.step2.answer",
                                  "agent.step3.verify"):
                continue

            trace_id = format(span.context.trace_id, "032x")
            span_id = format(span.context.span_id, "016x")
            parent_id = format(span.parent.span_id, "016x") if span.parent else ""
            timestamp = datetime.fromtimestamp(span.start_time / 1e9, tz=timezone.utc).isoformat()

            payload_spans.append({
                "trace_id": trace_id,
                "span_id": span_id,
                "parent_span_id": parent_id,
                "timestamp": timestamp,
                "agent_name": attrs.get("llm.agent_name", ""),
                "session_id": attrs.get("llm.session_id", ""),
                "model": attrs.get("gen_ai.request.model", ""),
                "provider": attrs.get("gen_ai.system", ""),
                "operation": attrs.get("gen_ai.operation.name", "chat"),
                "input_tokens": int(attrs.get("gen_ai.usage.input_tokens", 0)),
                "output_tokens": int(attrs.get("gen_ai.usage.output_tokens", 0)),
                "cost_usd": float(attrs.get("llm.cost_usd", 0.0)),
                "latency_ms": int(attrs.get("llm.latency_ms", 0)),
                "status": attrs.get("llm.status", ""),
                "error": attrs.get("llm.error", ""),
            })

        if not payload_spans:
            return SpanExportResult.SUCCESS

        try:
            response = requests.post(
                f"{self.api_url}/ingest",
                json={"spans": payload_spans},
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=60
            )
            if response.status_code != 200:
                print(f"Failed to send traces: {response.status_code} {response.text}")
                return SpanExportResult.FAILURE
            return SpanExportResult.SUCCESS
        except requests.RequestException as e:
            print(f"Failed to send traces: {e}")
            return SpanExportResult.FAILURE

    def shutdown(self):
        pass
