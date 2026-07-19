import time
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.resources import Resource
from anthropic import Anthropic
from dotenv import load_dotenv

from ._exporter import APIExporter

load_dotenv()

COST_PER_1K = {
    "claude-sonnet-4-6": 0.003,
    "claude-haiku-4-5": 0.00025,
    "gpt-4o": 0.005,
    "gpt-4o-mini": 0.00015,
}

_tracer = None
_client = None


def _get_tracer():
    global _tracer
    if _tracer is None:
        resource = Resource.create({"service.name": "spectandi"})
        provider = TracerProvider(resource=resource)
        provider.add_span_processor(SimpleSpanProcessor(APIExporter()))
        trace.set_tracer_provider(provider)
        _tracer = trace.get_tracer("spectandi", "0.1.0")
    return _tracer


def _get_client():
    global _client
    if _client is None:
        _client = Anthropic()
    return _client


def tracked_chat(prompt, model="claude-sonnet-4-6", max_tokens=500,
                 agent_name=None, session_id=None, user_id=None):
    tracer = _get_tracer()
    client = _get_client()

    with tracer.start_as_current_span("gen_ai.chat") as span:
        span.set_attribute("gen_ai.system", "anthropic")
        span.set_attribute("gen_ai.request.model", model)
        span.set_attribute("gen_ai.request.max_tokens", max_tokens)
        span.set_attribute("gen_ai.operation.name", "chat")
        if agent_name:
            span.set_attribute("llm.agent_name", agent_name)
        if session_id:
            span.set_attribute("llm.session_id", session_id)
        if user_id:
            span.set_attribute("llm.user_id", user_id)

        start = time.time()

        try:
            response = client.messages.create(
                model=model,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}]
            )
            latency_ms = round((time.time() - start) * 1000)
            tokens_in = response.usage.input_tokens
            tokens_out = response.usage.output_tokens
            cost = round((tokens_in + tokens_out) / 1000 * COST_PER_1K.get(model, 0.003), 8)

            span.set_attribute("gen_ai.usage.input_tokens", tokens_in)
            span.set_attribute("gen_ai.usage.output_tokens", tokens_out)
            span.set_attribute("llm.cost_usd", cost)
            span.set_attribute("llm.latency_ms", latency_ms)
            span.set_attribute("llm.status", "success")

            return response.content[0].text

        except Exception as e:
            span.set_attribute("llm.status", "error")
            span.set_attribute("llm.error", str(e))
            span.record_exception(e)
            raise
