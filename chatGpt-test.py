from openai import OpenAI

client = OpenAI(
  api_key="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"
)

response = client.responses.create(
  model="gpt-5-nano",
  input="write a haiku about ai",
  store=True,
)

print(response.output_text)
